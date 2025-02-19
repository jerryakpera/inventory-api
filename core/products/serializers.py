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

    class Meta:
        model = ProductCategory
        fields = "__all__"


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
    """

    unit = serializers.CharField(source="product.unit.symbol", read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "product",
            "id",
            "unit",
            "price",
            "created",
            "updated",
            "readable_name",
        ]
