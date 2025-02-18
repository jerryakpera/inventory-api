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


def generate_data(no):
    """
    Generate sample data for testing purposes.

    Parameters
    ----------
    no : int
        Number of objects to generate.
    """

    UserFactory.create_batch(no)

    # Generate Product Units
    product_units = ProductUnitFactory.create_batch(no)

    # Generate Product Categories
    product_categories = ProductCategoryFactory.create_batch(no)

    # Generate Products
    products = ProductFactory.create_batch(no)

    # Generate Product Variants
    product_variants = ProductVariantFactory.create_batch(no)

    print(f"Created {len(product_units)} Product Units")
    print(f"Created {len(product_categories)} Product Categories")
    print(f"Created {len(products)} Products")
    print(f"Created {len(product_variants)} Product Variants")
