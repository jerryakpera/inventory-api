from decimal import Decimal

from django.test import TestCase

from core.custom_user.tests.factories import UserFactory
from core.products.models import (
    Product,
    ProductCategory,
    ProductPriceHistory,
    ProductUnit,
    ProductVariant,
)


class TestProductUnitModel(TestCase):
    def setUp(self):
        self.unit = ProductUnit.objects.create(name="Kilogram", symbol="kg")

    def test_string_representation(self):
        self.assertEqual(str(self.unit), "Kilogram")


class TestProductCategoryModel(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(
            name="Fruits", description="A category of fruits.", slug="fruits"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.category), "Fruits")

    def test_slug_generation(self):
        category = ProductCategory.objects.create(name="Dried Fruits")
        self.assertEqual(category.slug, "dried-fruits")


class TestProductModel(TestCase):
    def setUp(self):
        self.unit = ProductUnit.objects.create(name="Kilogram", symbol="kg")
        self.category = ProductCategory.objects.create(name="Fruits", slug="fruits")
        self.author = UserFactory()
        self.product = Product.objects.create(
            author=self.author, name="Apple", category=self.category, unit=self.unit
        )

    def test_string_representation(self):
        self.assertEqual(str(self.product), "Apple")

    def test_slug_generation(self):
        product = Product.objects.create(
            author=self.author, name="Banana", unit=self.unit
        )
        self.assertEqual(product.slug, "banana")


class TestProductVariantModel(TestCase):
    def setUp(self):
        self.unit = ProductUnit.objects.create(name="Gram", symbol="g")
        self.category = ProductCategory.objects.create(name="Fruits", slug="fruits")
        self.author = UserFactory()
        self.product = Product.objects.create(
            author=self.author, name="Apple", category=self.category, unit=self.unit
        )
        self.variant = ProductVariant.objects.create(
            author=self.author,
            product=self.product,
            description="A green apple.",
            price=1.99,
            size=10,
            stock=100,
            flavor="Green",
            low_stock_threshold=10,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.variant), "Apple (10g, Green)")

    def test_readable_name(self):
        """Test the readable_name method of ProductVariant."""
        self.assertEqual(self.variant.readable_name(), "Apple (10g, Green)")

    def test_slug_generation(self):
        self.assertEqual(self.variant.slug, "apple-10-green")

    def test_price_history_creation(self):
        old_price = self.variant.price
        self.variant.price = Decimal("2.50")
        self.variant.save()

        price_history = ProductPriceHistory.objects.filter(
            product_variant=self.variant,
        )

        self.assertTrue(price_history.exists())
        self.assertEqual(price_history.first().price, Decimal(str(old_price)))


class TestProductPriceHistoryModel(TestCase):
    def setUp(self):
        self.unit = ProductUnit.objects.create(name="Gram", symbol="g")
        self.category = ProductCategory.objects.create(
            name="Fruits",
            slug="fruits",
        )
        self.author = UserFactory()
        self.product = Product.objects.create(
            author=self.author, name="Apple", category=self.category, unit=self.unit
        )
        self.variant = ProductVariant.objects.create(
            author=self.author,
            product=self.product,
            description="A green apple.",
            price=Decimal("1.99"),
            size=Decimal("10"),
            stock=100,
            flavor="Green",
            low_stock_threshold=10,
        )
        self.price_history = ProductPriceHistory.objects.create(
            product_variant=self.variant,
            price=Decimal("1.99"),
        )

    def test_string_representation(self):
        """Test the __str__ method of ProductPriceHistory."""
        expected_str = (
            f"{self.variant} - 1.99 "
            f"({self.price_history.timestamp.strftime('%Y-%m-%d')})"
        )
        self.assertEqual(str(self.price_history), expected_str)
