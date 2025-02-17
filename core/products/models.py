"""
This file is used to define the models for the products app.
"""

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

from core.custom_user.models import User


class ProductUnit(models.Model):
    """
    Represents a unit of a product.
    """

    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        """
        Return the name of the unit.

        Returns
        -------
        str
            The name of the unit.
        """
        return self.name


class Product(models.Model):
    """
    Represents a base product.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=100)

    category = models.ForeignKey(
        "ProductCategory",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
    )

    tags = TaggableManager(
        help_text="Use tags to add health benefits, Hair growth, etc.",
    )

    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=250)

    unit = models.ForeignKey(
        ProductUnit,
        on_delete=models.CASCADE,
        related_name="products",
    )

    # The product is considered active if it can be ordered
    is_active = models.BooleanField(
        default=True,
        help_text="Is the product available for purchase?",
    )

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        """
        Return the name of the product.

        Returns
        -------
        str
            The name of the product.
        """
        return self.name


class ProductVariant(models.Model):
    """
    Represents a variant of a product with specific attributes like size and flavor.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="product_variants",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    size = models.CharField(max_length=50, blank=True, null=True)
    flavor = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    stock = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField(
        help_text=(
            "The minimum stock level at which the product "
            "is considered to be low in stock."
        ),
    )

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    slug = models.SlugField(unique=True, max_length=250, editable=False)

    image = models.ImageField(
        upload_to="product_variants/",
        null=True,
        blank=True,
        help_text="An image of the product.",
    )

    class Meta:
        # A product variant is unique by product, size, and flavor
        unique_together = ("product", "size", "flavor")
        ordering = ["product", "size", "flavor"]
        indexes = [models.Index(fields=["product", "size", "flavor"])]

    def __str__(self):
        """
        Return a string representation of the product variant.

        Returns
        -------
        str
            The string representation of the product variant.
        """
        details = []
        if self.size:
            details.append(f"{self.size}{self.product.unit.symbol}")

        if self.flavor:
            details.append(self.flavor)

        return f"{self.product.name} ({', '.join(details)})"

    def save(self, *args, **kwargs):
        """
        Save the product variant and generate a slug if it does not exist.

        Parameters
        ----------
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.
        """
        super().save(*args, **kwargs)

        if not self.slug:
            slug_base = f"{self.product.name}-{self.size or ''}-{self.flavor or ''}"
            self.slug = slugify(slug_base)
        super().save(*args, **kwargs)


class ProductCategory(models.Model):
    """
    Represents a category of products.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    slug = models.SlugField(unique=True, max_length=250)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Product categories"

    def __str__(self):
        """
        Return the name of the category.

        Returns
        -------
        str
            The name of the category.
        """
        return self.name
