"""
Generate sample data for testing purposes.
"""

from core.custom_user.tests.factories import UserFactory
from core.products.tests.factories import (
    ProductCategoryFactory,
    ProductFactory,
    ProductUnitFactory,
    ProductVariantFactory,
)

from . import models as product_models


def generate_data(no):
    """
    Generate sample data for testing purposes.

    Parameters
    ----------
    no : int
        Number of objects to generate.
    """

    product_units_count = product_models.ProductUnit.objects.count()
    product_categories_count = product_models.ProductCategory.objects.count()
    products_count = product_models.Product.objects.count()
    product_variants_count = product_models.ProductVariant.objects.count()

    UserFactory.create_batch(no)

    if product_units_count < no:
        no = no - product_units_count

        # Generate Product Units
        product_units = ProductUnitFactory.create_batch(no)
        print(f"Created {len(product_units)} Product Units")

    if product_categories_count < no:
        no = no - product_categories_count

        # Generate Product Categories
        product_categories = ProductCategoryFactory.create_batch(no)
        print(f"Created {len(product_categories)} Product Categories")

    if products_count < no:
        no = no - products_count

        # Generate Products
        products = ProductFactory.create_batch(no)
        print(f"Created {len(products)} Products")

    if product_variants_count < no:
        no = no - product_variants_count

        # Generate Product Variants
        product_variants = ProductVariantFactory.create_batch(no)
        print(f"Created {len(product_variants)} Product Variants")
