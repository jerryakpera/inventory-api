"""
Serializers for the products app.
"""

from rest_framework import serializers

from core.custom_user.models import User

from .models import (
    Product,
    ProductCategory,
    ProductPriceHistory,
    ProductUnit,
    ProductVariant,
)


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductCategory model.
    """

    product_count = serializers.SerializerMethodField()

    def get_product_count(self, obj):
        """
        Return the number of products associated with this category.

        Parameters
        ----------
        obj : ProductCategory
            The product category instance.

        Returns
        -------
        int
            The number of products associated with this category.
        """
        return obj.products.count()

    class Meta:
        model = ProductCategory
        fields = "__all__"
        extra_kwargs = {
            "slug": {"required": False},
        }


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        required=False,
    )

    unit = serializers.PrimaryKeyRelatedField(
        queryset=ProductUnit.objects.all(),
        required=False,
    )

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )

    variant_count = serializers.SerializerMethodField()

    def get_variant_count(self, obj):
        """
        Return the number of product variants associated with this product.

        Parameters
        ----------
        obj : Product
            The product instance.

        Returns
        -------
        int
            The number of product variants associated with this product.
        """
        return obj.variants.count()

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "slug": {"required": False},
            "author": {"required": False},
            "is_active": {"required": True},
        }
        depth = 1


class ProductPriceHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductPriceHistory model.
    """

    class Meta:
        model = ProductPriceHistory
        fields = "__all__"


class ProductUnitSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductUnit model.
    """

    class Meta:
        model = ProductUnit
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductVariant model.
    Merges necessary details from the Product model.
    """

    name = serializers.CharField(
        source="product.name",
        read_only=True,
    )
    description = serializers.CharField(
        source="product.description",
        read_only=True,
    )
    category = serializers.CharField(
        source="product.category.name",
        read_only=True,
    )
    unit = serializers.CharField(
        source="product.unit.name",
        read_only=True,
    )

    # size = serializers.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     coerce_to_string=False,
    # )
    # price = serializers.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     coerce_to_string=False,
    # )

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
    )

    class Meta:
        model = ProductVariant
        fields = "__all__"
        extra_kwargs = {
            "slug": {"required": False},
            "flavor": {"required": False},
        }
