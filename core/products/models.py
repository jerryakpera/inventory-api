"""
This file is used to define the models for the products app.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils.text import slugify
from simple_history.models import HistoricalRecords
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


class ProductCategory(models.Model):
    """
    Represents a category of products.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="categories/",
        null=True,
        blank=True,
        help_text="An image of the category.",
    )

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    slug = models.SlugField(unique=True, max_length=250)

    class Meta:
        ordering = ["id", "name"]
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

    # Create a save method that sets the slug if it does not exist
    def save(self, *args, **kwargs):
        """
        Save the product category and generate a slug if it does not exist.

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
        blank=True,
    )

    tags = TaggableManager(
        help_text="Use tags to add health benefits, Hair growth, etc.",
    )

    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=250)

    unit = models.ForeignKey(
        ProductUnit,
        on_delete=models.CASCADE,
        related_name="products",
    )

    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True,
        help_text="An image of the product.",
    )

    # The product is considered active if it can be ordered
    is_active = models.BooleanField(
        default=True,
        help_text="Is the product available for purchase?",
    )

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    history = HistoricalRecords()

    def __str__(self):
        """
        Return the name of the product.

        Returns
        -------
        str
            The name of the product.
        """
        return self.name

    # Create a save method that sets the slug if it does not exist
    def save(self, *args, **kwargs):
        """
        Save the product and generate a slug if it does not exist.

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


class ProductPriceHistory(models.Model):
    """
    Stores the historical prices of product variants.
    """

    product_variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.CASCADE,
        related_name="price_history",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        """
        Return a string representation of the price history.

        Returns
        -------
        str
            The string representation of the price history.
        """
        return f"{self.product_variant} - {self.price} ({self.timestamp.strftime('%Y-%m-%d')})"


class ProductVariant(models.Model):
    """
    Represents a variant of a product with specific attributes like size and flavor.
    """

    sku = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        db_index=True,
        help_text="Stock Keeping Unit for inventory tracking.",
    )

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

    brand = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(null=True, blank=True)

    size = models.DecimalField(
        default=0.0,
        max_digits=10,
        decimal_places=2,
        help_text="The size of the product.",
    )
    flavor = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )
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

    # The product is considered active if it can be ordered
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Is this product available for purchase?",
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Has this product been deleted?",
    )

    updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    slug = models.SlugField(
        unique=True,
        max_length=250,
        editable=False,
        db_index=True,
    )

    image = models.ImageField(
        upload_to="variants/",
        null=True,
        blank=True,
        help_text="An image of the category.",
    )

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "brand", "size", "flavor"],
                name="unique_product_variant",
                condition=~models.Q(flavor=None),
            ),
            CheckConstraint(check=Q(size__gte=0), name="size_non_negative"),
        ]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active"]),
        ]

    def delete(self, *args, **kwargs):
        """
        Delete the product variant and set the `is_deleted` flag to `True`.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """
        self.is_deleted = True
        self.save()

    def readable_name(self):
        """
        Return a human-readable name for the product variant.

        Returns
        -------
        str
            The human-readable name for the product variant.
        """
        return str(self)

    def __str__(self):
        """
        Return a string representation of the product variant.

        Returns
        -------
        str
            The string representation of the product variant.
        """
        details = []

        if self.brand:
            details.append(self.brand)

        if self.size:
            details.append(f"{self.size}{self.product.unit.symbol}")

        if self.flavor:
            details.append(self.flavor)

        return f"{self.product.name} ({', '.join(details)})"

    def generate_sku(self):
        """
        Generate a unique SKU based on product attributes.

        Returns
        -------
        str
            The generated SKU.
        """
        base_sku = slugify(self.product.name)[:6].upper()
        brand_part = f"{self.brand}" if self.brand else "NA"
        size_part = f"{int(self.size)}" if self.size else "NA"
        flavor_part = slugify(self.flavor)[:3].upper() if self.flavor else "NA"

        return f"{base_sku}-{brand_part}-{size_part}-{flavor_part}"

    def save(self, *args, **kwargs):
        """
        Save the product variant and generate an SKU if it does not exist.
        Track price changes and store them in `ProductPriceHistory`.

        Parameters
        ----------
        *args : tuple
            The positional arguments.
        **kwargs : dict
            The keyword arguments.
        """
        if not self.sku:
            self.sku = self.generate_sku()

            # Ensure SKU is unique
            counter = 1
            while ProductVariant.objects.filter(
                sku=self.sku
            ).exists():  # pragma: no cover
                self.sku = f"{self.generate_sku()}-{counter}"
                counter += 1

        if not self.slug:
            slug_base = f"{self.product.name}-{self.size or ''}-{self.flavor or ''}"
            self.slug = slugify(slug_base)

        # Check if the price has changed before saving
        if self.pk:
            previous = ProductVariant.objects.filter(pk=self.pk).first()
            if previous and previous.price != self.price:
                ProductPriceHistory.objects.create(
                    product_variant=self,
                    price=previous.price,
                )

        super().save(*args, **kwargs)
