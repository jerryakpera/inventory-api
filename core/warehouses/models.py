"""
Model definitions for `warehouses` app.
"""

from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.text import slugify

from core.custom_user.models import User
from core.products.models import ProductVariant


class Warehouse(models.Model):
    """
    Represents a physical or virtual warehouse location.
    """

    TYPE_CHOICES = [
        ("STORAGE", "Storage"),
        ("SHOP", "Shop"),
    ]

    VISIBILITY_CHOICES = [
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private"),
    ]

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="STORAGE",
        help_text="The type of warehouse.",
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="PRIVATE",
        help_text="Determines if the warehouse is visible to the public.",
    )

    author = models.ForeignKey(
        "custom_user.User",
        on_delete=models.CASCADE,
        related_name="warehouses",
    )
    name = models.CharField(max_length=100)
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
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Warehouse.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class WarehouseUser(models.Model):
    """
    Represent the relationship between users and warehouses with assigned roles.
    """

    ROLE_CHOICES = [
        ("MANAGER", "Manager"),
        ("STAFF", "Staff"),
    ]

    class RoleChoices:
        """
        Provide a class-based interface for role choices.
        """

        MANAGER = "MANAGER"
        STAFF = "STAFF"

    user = models.ForeignKey(
        "custom_user.User",
        on_delete=models.CASCADE,
        related_name="warehouse_users",
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="users",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="STAFF",
        help_text="The role of the user at the warehouse.",
    )

    class Meta:
        unique_together = ("user", "warehouse")

    def __str__(self):
        """
        Return a string representation of the warehouse user.

        Returns
        -------
        str
            The string representation.
        """
        return f"{self.user} - {self.role} at {self.warehouse}"


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

    def save(self, *args, **kwargs):
        """
        Override save method to check for low stock and trigger alerts.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """
        super().save(*args, **kwargs)

        if self.quantity <= self.low_stock_threshold:
            # Check if an active alert already exists
            active_alert = StockAlert.objects.filter(stock=self, is_active=True).first()

            if active_alert:
                return

            # Trigger low stock alert
            StockAlert.objects.create(
                stock=self,
                alert_type="LOW_STOCK" if self.quantity > 0 else "OUT_OF_STOCK",
            )


class StockAlert(models.Model):
    """
    Stores stock alerts for low stock and out-of-stock notifications.
    """

    ALERT_TYPES = [
        ("LOW_STOCK", "Low Stock"),
        ("OUT_OF_STOCK", "Out of Stock"),
    ]

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="alerts",
    )
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Return a string representation of the stock alert.

        Returns
        -------
        str
            The string representation.
        """
        return f"{self.stock.product_variant} - {self.get_alert_type_display()}"


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
        "Warehouse", on_delete=models.CASCADE, related_name="outgoing_transfers"
    )
    to_warehouse = models.ForeignKey(
        "Warehouse", on_delete=models.CASCADE, related_name="incoming_transfers"
    )
    quantity = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        """
        Return a string representation of the stock transfer.

        Returns
        -------
        str
            The string representation.
        """

        return (
            f"Transfer {self.quantity} of {self.product_variant} "
            f"from {self.from_warehouse} to {self.to_warehouse}."
        )

    def clean(self):
        """
        Ensure that `from_warehouse` and `to_warehouse` are different,
        and validate stock availability.
        """
        if self.from_warehouse == self.to_warehouse:
            raise ValidationError(
                {
                    "to_warehouse": (
                        "Destination warehouse must be "
                        "different from source warehouse."
                    )
                }
            )

        if self.quantity <= 0:
            raise ValidationError(
                {"quantity": "Transfer quantity must be greater than zero."}
            )

        # Check available stock
        from_stock = Stock.objects.filter(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant,
        ).first()

        if not from_stock or from_stock.quantity < self.quantity:
            raise ValidationError(
                {"quantity": "Insufficient stock in the source warehouse."}
            )

    def save(self, *args, **kwargs):
        """
        Override save to ensure stock modification is done safely.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """
        self.clean()

        with transaction.atomic():
            # Lock stock row for update to prevent race conditions
            from_stock = (
                Stock.objects.select_for_update()
                .filter(
                    warehouse=self.from_warehouse,
                    product_variant=self.product_variant,
                )
                .first()
            )

            if (
                not from_stock or from_stock.quantity < self.quantity
            ):  # pragma: no cover
                raise ValidationError(
                    {
                        "quantity": "Insufficient stock in the source warehouse.",
                    }
                )

            from_stock.quantity -= self.quantity
            from_stock.save()

            to_stock, _ = Stock.objects.select_for_update().get_or_create(
                warehouse=self.to_warehouse,
                product_variant=self.product_variant,
            )
            to_stock.quantity += self.quantity
            to_stock.save()

            super().save(*args, **kwargs)


class StockAudit(models.Model):
    """
    Represents a stock audit for a specific product variant in a warehouse.
    """

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="stock_audits",
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="stock_audits",
    )
    counted_quantity = models.PositiveIntegerField(
        help_text="The quantity of stock counted during the audit.",
    )
    recorded_quantity = models.PositiveIntegerField(
        help_text="The expected quantity in the system before the audit.",
    )
    discrepancy = models.IntegerField(
        help_text="The difference between recorded and counted stock.",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stock_audits",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Calculate the discrepancy before saving.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """

        self.discrepancy = self.counted_quantity - self.recorded_quantity

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the stock audit.

        Returns
        -------
        str
            The string representation.
        """
        return (
            f"Audit for {self.product_variant} in {self.warehouse} "
            f"on {self.created_at.strftime('%Y-%m-%d')}"
        )


class StockAdjustment(models.Model):
    """
    Represents a manual stock adjustment due to damage, loss, or expiration.
    """

    REASON_CHOICES = [
        ("DAMAGE", "Damaged"),
        ("LOSS", "Lost"),
        ("EXPIRY", "Expired"),
        ("AUDIT_CORRECTION", "Audit Correction"),
    ]

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="stock_adjustments",
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="stock_adjustments",
    )
    adjustment_quantity = models.IntegerField(
        help_text="Positive to add stock, negative to reduce stock.",
    )
    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES,
        default="LOSS",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stock_adjustments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Adjust the product variant's stock quantity before saving.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """
        with transaction.atomic():
            inventory = Stock.objects.get(
                warehouse=self.warehouse,
                product_variant=self.product_variant,
            )
            inventory.quantity += self.adjustment_quantity
            inventory.save()

        if (
            self.adjustment_quantity < 0
            and abs(self.adjustment_quantity) > self.stock.quantity
        ):
            raise ValidationError("Insufficient stock for adjustment.")

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the stock adjustment.

        Returns
        -------
        str
            The string representation.
        """
        return (
            f"Adjustment of {self.adjustment_quantity} for "
            f"{self.product_variant} in {self.warehouse}"
        )
