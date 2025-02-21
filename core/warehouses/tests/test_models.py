from django.core.exceptions import ValidationError
from django.test import TestCase

from core.custom_user.tests.factories import UserFactory
from core.products.models import ProductVariant
from core.products.tests import factories as product_factories
from core.warehouses.models import Stock, StockTransfer, Warehouse, WarehouseUser


class TestWarehouseModel(TestCase):
    def setUp(self):
        self.author = UserFactory()
        self.warehouse = Warehouse.objects.create(
            author=self.author,
            name="Main Storage",
            location="123 Warehouse St",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.warehouse), "Main Storage")

    def test_slug_generation(self):
        warehouse = Warehouse.objects.create(author=self.author, name="Backup Storage")
        self.assertEqual(warehouse.slug, "backup-storage")

    def test_slug_uniqueness(self):
        warehouse1 = Warehouse.objects.create(
            author=self.author, name="Duplicate Storage"
        )
        warehouse2 = Warehouse.objects.create(
            author=self.author, name="Duplicate Storage"
        )
        warehouse3 = Warehouse.objects.create(
            author=self.author, name="Duplicate Storage"
        )

        self.assertEqual(warehouse1.slug, "duplicate-storage")
        self.assertEqual(warehouse2.slug, "duplicate-storage-1")
        self.assertEqual(warehouse3.slug, "duplicate-storage-2")


class TestWarehouseUserModel(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.warehouse = Warehouse.objects.create(author=self.user, name="Warehouse A")
        self.warehouse_user = WarehouseUser.objects.create(
            user=self.user, warehouse=self.warehouse, role="MANAGER"
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.warehouse_user), f"{self.user} - MANAGER at {self.warehouse}"
        )


class TestStockModel(TestCase):
    def setUp(self):
        self.author = UserFactory()
        self.warehouse = Warehouse.objects.create(
            author=self.author, name="Central Warehouse"
        )
        self.product_variant = product_factories.ProductVariantFactory(
            author=self.author
        )
        self.stock = Stock.objects.create(
            warehouse=self.warehouse, product_variant=self.product_variant, quantity=50
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.stock), f"{self.product_variant} - 50 in {self.warehouse}"
        )


class TestStockTransferModel(TestCase):
    def setUp(self):
        self.author = UserFactory()
        self.from_warehouse = Warehouse.objects.create(
            author=self.author, name="Source Warehouse"
        )
        self.to_warehouse = Warehouse.objects.create(
            author=self.author, name="Destination Warehouse"
        )

        self.product_variant = product_factories.ProductVariantFactory(
            author=self.author
        )

        self.product_variant = product_factories.ProductVariantFactory(
            author=self.author
        )
        self.stock = Stock.objects.create(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant,
            quantity=100,
        )
        self.transfer = StockTransfer(
            author=self.author,
            product_variant=self.product_variant,
            from_warehouse=self.from_warehouse,
            to_warehouse=self.to_warehouse,
            quantity=20,
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.transfer),
            f"Transfer 20 of {self.product_variant} from {self.from_warehouse} "
            f"to {self.to_warehouse}.",
        )

    def test_stock_transfer_validation(self):
        # Ensure same warehouse transfer is invalid
        self.transfer.to_warehouse = self.from_warehouse
        with self.assertRaises(ValidationError):
            self.transfer.clean()

        # Ensure insufficient stock validation
        self.transfer.to_warehouse = self.to_warehouse
        self.transfer.quantity = 200
        with self.assertRaises(ValidationError):
            self.transfer.clean()

    def test_stock_transfer_execution(self):
        initial_from_stock = self.stock.quantity
        self.transfer.save()
        self.stock.refresh_from_db()
        to_stock = Stock.objects.get(
            warehouse=self.to_warehouse, product_variant=self.product_variant
        )

        self.assertEqual(
            self.stock.quantity, initial_from_stock - self.transfer.quantity
        )
        self.assertEqual(to_stock.quantity, self.transfer.quantity)

    def test_stock_transfer_zero_or_negative_quantity(self):
        # Ensure zero quantity transfer is invalid
        self.transfer.quantity = 0
        with self.assertRaises(ValidationError):
            self.transfer.clean()

        # Ensure negative quantity transfer is invalid
        self.transfer.quantity = -10
        with self.assertRaises(ValidationError):
            self.transfer.clean()
