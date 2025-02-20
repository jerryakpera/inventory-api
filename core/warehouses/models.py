"""
Model definitions for `warehouses` app.
"""

from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Warehouse(models.Model):
    """
    Represents a physical or virtual warehouse location.
    """

    author = models.ForeignKey(
        "custom_user.User",
        on_delete=models.CASCADE,
        related_name="warehouses",
    )
    name = models.CharField(max_length=100, unique=True)
    location = models.TextField(
        blank=True,
        help_text="Address or location description",
    )
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=250)
    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        """
        Return a string representation of the warehouse.

        Returns
        -------
        str
            The string representation.
        """

        return self.name

    def save(self, *args, **kwargs):
        """
        Save the warehouse and generate a slug if it does not exist.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Stock(models.Model):
    """
    Tracks the inventory of product variants at different warehouse locations.
    """

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="stocks",
    )
    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="stocks",
    )
    quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(
        default=10,
        help_text="When the stock quantity is below this value, the warehouse will be notified.",
    )

    class Meta:
        unique_together = ("warehouse", "product_variant")

    def __str__(self):
        """
        Return a string representation of the stock.

        Returns
        -------
        str
            The string representation.
        """
        return f"{self.product_variant} - {self.quantity} in {self.warehouse}"


class StockTransfer(models.Model):
    """
    Represents a transfer of product stock from one warehouse to another.
    """

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    author = models.ForeignKey(
        "custom_user.User",
        on_delete=models.CASCADE,
        related_name="transfers",
    )
    reference_code = models.CharField(
        max_length=20,
        default=uuid4,
        unique=True,
        editable=False,
        help_text="Unique reference for this transfer.",
    )

    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="transfers",
    )
    from_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="outgoing_transfers"
    )
    to_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="incoming_transfers"
    )
    quantity = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        """
        Return a string representation of the transfer.

        Returns
        -------
        str
            The string representation.
        """
        return (
            f"Transfer {self.quantity} of {self.product_variant}"
            f" from {self.from_warehouse} to {self.to_warehouse}."
        )

    def clean(self):
        """
        Ensure that the `from_warehouse` and `to_warehouse` are different.
        """
        if self.from_warehouse == self.to_warehouse:
            raise ValidationError(
                {
                    "to_warehouse": (
                        "Destination warehouse must be different "
                        "from source warehouse."
                    )
                }
            )

        if self.quantity <= 0:
            raise ValidationError(
                {
                    "quantity": "Transfer quantity must be greater than zero.",
                }
            )

        # Check available stock
        from_stock = Stock.objects.filter(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant,
        ).first()

        if not from_stock or from_stock.quantity < self.quantity:
            raise ValidationError(
                {
                    "quantity": "Insufficient stock in the source warehouse.",
                }
            )

    def save(self, *args, **kwargs):
        """
        Override save to call `clean()` before saving.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """
        self.clean()

        # Deduct stock from from_warehouse
        from_stock, _ = Stock.objects.get_or_create(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant,
        )
        from_stock.quantity -= self.quantity
        from_stock.save()

        # Add stock to to_warehouse
        to_stock, _ = Stock.objects.get_or_create(
            warehouse=self.to_warehouse,
            product_variant=self.product_variant,
        )
        to_stock.quantity += self.quantity
        to_stock.save()

        super().save(*args, **kwargs)
