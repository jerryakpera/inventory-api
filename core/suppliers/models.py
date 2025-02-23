"""
Models for the `suppliers` app.
"""

from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from core.custom_user.models import User
from core.products.models import ProductVariant


class Supplier(models.Model):
    """
    Represents a supplier who provides products to the warehouse.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_suppliers",
    )

    business_name = models.CharField(
        max_length=255,
        help_text="Name of the business or company",
    )
    contact_person = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Name of the contact person",
    )
    email = models.EmailField(
        null=True,
        blank=True,
        help_text="Email address of the supplier",
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        help_text="Phone number of the supplier",
    )

    country = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Country where the business/person is located",
    )
    city = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="City where the business/person is located",
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    history = HistoricalRecords()

    def __str__(self):
        """
        Return a string representation of the object.

        Returns
        -------
        str
            A string representation of the object.
        """
        return self.business_name


class SupplierProduct(models.Model):
    """
    Links a supplier to the products they provide.
    """

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="products",
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="suppliers",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = ("supplier", "product_variant")

    def __str__(self):
        """
        Return a string representation of the object.

        Returns
        -------
        str
            A string representation of the object.
        """
        return f"{self.supplier.name} - {self.product_variant}"
