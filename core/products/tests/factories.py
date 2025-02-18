"""
Factories for the products app.
"""

import factory
from faker import Faker

from core.custom_user.tests.factories import UserFactory
from core.products.models import Product, ProductCategory, ProductUnit, ProductVariant

fake = Faker()


class ProductUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductUnit

    name = factory.LazyAttribute(lambda _: fake.word()[:10])

    symbol = factory.Sequence(lambda n: f"{fake.word()[:10]}_{n}")


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    author = factory.SubFactory(UserFactory)
    name = factory.Faker("word")
    category = factory.SubFactory(ProductCategoryFactory)
    description = factory.Faker("sentence")
    slug = factory.Faker("slug")
    unit = factory.SubFactory(ProductUnitFactory)


class ProductVariantFactory(factory.django.DjangoModelFactory):  # pragma: no cover
    class Meta:
        model = ProductVariant

    author = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    size = factory.Faker(
        "random_int",
        min=1,
        max=100,
    )
    price = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
    )
    stock = factory.Faker("random_int", min=5, max=100)
    low_stock_threshold = factory.Faker("random_int", min=1, max=10)
    flavor = factory.Faker("word")
