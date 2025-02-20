from django.test import TestCase

from core.custom_user.tests.factories import UserFactory
from core.products.models import ProductVariant
from core.products.tests import factories


class TestProductUnitFactory(TestCase):
    def test_factory(self):
        """
        Test the ProductUnitFactory.
        """
        product_unit = factories.ProductUnitFactory()

        self.assertTrue(product_unit)
        self.assertTrue(product_unit.name)
        self.assertTrue(product_unit.symbol)
        self.assertEqual(str(product_unit), product_unit.name)


class TestProductCategoryFactory(TestCase):
    def test_factory(self):
        """
        Test the ProductCategoryFactory.
        """
        product_category = factories.ProductCategoryFactory()

        self.assertTrue(product_category)
        self.assertTrue(product_category.name)
        self.assertTrue(product_category.description)


class TestProductFactory(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = factories.ProductFactory()

    def test_factory(self):
        """
        Test the ProductFactory.
        """

        self.assertTrue(self.product)
        self.assertTrue(self.product.author)
        self.assertTrue(self.product.name)
        self.assertTrue(self.product.category)
        self.assertTrue(self.product.description)
        self.assertTrue(self.product.slug)
        self.assertTrue(self.product.unit)


class TestProductVariantFactory(TestCase):
    def setUp(self):
        self.product = factories.ProductFactory()
        self.product_variant = factories.ProductVariantFactory(product=self.product)

    def test_factory(self):
        """
        Test the ProductVariantFactory.
        """

        self.assertTrue(self.product_variant)
        self.assertTrue(self.product_variant.product)
        self.assertTrue(self.product_variant.author)
        self.assertTrue(self.product.description)
        self.assertTrue(self.product_variant.price)
        self.assertTrue(self.product_variant.size)
