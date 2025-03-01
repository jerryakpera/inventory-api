"""
Serializers for the products app.
"""

from rest_framework import serializers

from core.custom_user.models import User
from core.custom_user.serializers import UserSerializer

from .models import (
    Product,
    ProductCategory,
    ProductPriceHistory,
    ProductUnit,
    ProductVariant,
)


class ProductUnitSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductUnit model.
    """

    class Meta:
        model = ProductUnit
        fields = "__all__"

        extra_kwargs = {
            "author": {"required": False},
            "slug": {"required": False},
        }


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        write_only=True,
    )
    unit = serializers.PrimaryKeyRelatedField(queryset=ProductUnit.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all()
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )
    variant_count = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        """
        Add the number of variants associated with the product.

        Parameters
        ----------
        instance : Product
            The product instance.

        Returns
        -------
        dict
            The serialized product instance.
        """
        instance.variant_count = instance.variants.count()

        return super().to_representation(instance)

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "author": {"required": False},
            "is_active": {"required": False},
            "slug": {"required": False, "read_only": True},
        }


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductCategory model.
    """

    product_count = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

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
            "author": {"required": False},
        }


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
            "author": {"required": False},
        }


class ProductPriceHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductPriceHistory model.
    """

    class Meta:
        model = ProductPriceHistory
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

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
    )

    class Meta:
        model = ProductVariant
        fields = "__all__"
        extra_kwargs = {
            "sku": {"required": False},
            "slug": {"required": False},
            "author": {"required": False},
        }


class ProductVariantDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductVariant model.
    """

    class Meta:
        model = ProductVariant
        fields = "__all__"

        depth = 2
