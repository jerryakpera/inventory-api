from django.test import TestCase

from core.custom_user.tests.factories import UserFactory
from core.products.models import Product, ProductCategory, ProductUnit, ProductVariant
from core.products.tests.factories import ProductFactory


class TestProductUnitModel(TestCase):
    def setUp(self):
        self.unit = ProductUnit.objects.create(
            name="Kilogram",
            symbol="kg",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.unit), "Kilogram")


class TestProductCategoryModel(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(
            name="Fruits",
            description="A category of fruits.",
            slug="fruits",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.category), "Fruits")


class TestProductModel(TestCase):
    def setUp(self):
        self.unit = ProductUnit.objects.create(
            name="Kilogram",
            symbol="kg",
        )

        self.category = ProductCategory.objects.create(
            name="Fruits",
            description="A category of fruits.",
            slug="fruits",
        )

        self.product = Product.objects.create(
            author=UserFactory(),
            name="Apple",
            description="A red apple.",
            category=self.category,
            unit=self.unit,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.product), "Apple")


class TestProductVariantModel(TestCase):
    def setUp(self):
        self.unit = ProductUnit.objects.create(
            name="Gram",
            symbol="g",
        )

        self.category = ProductCategory.objects.create(
            name="Fruits",
            description="A category of fruits.",
            slug="fruits",
        )

        self.product = Product.objects.create(
            author=UserFactory(),
            name="Apple",
            description="Fresh and savoury apples.",
            category=self.category,
            unit=self.unit,
        )

        self.variant = ProductVariant.objects.create(
            author=UserFactory(),
            product=self.product,
            description="A green apple.",
            price=1.99,
            size=10,
            stock=100,
            flavor="Green",
            low_stock_threshold=10,
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.variant), f"Apple ({self.variant.size}g, {self.variant.flavor})"
        )
