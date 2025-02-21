"""
Serializer definitions for the `Warehouses` app.
"""

from rest_framework import serializers

from core.custom_user.models import User
from core.products.models import ProductVariant

from .models import Stock, StockTransfer, Warehouse, WarehouseUser


class WarehouseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Warehouse model.
    """

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        write_only=True,
    )
    stock_count = serializers.SerializerMethodField()
    user_roles = serializers.SerializerMethodField()

    def get_stock_count(self, obj):
        """
        Return the number of stock items associated with this warehouse.

        Parameters
        ----------
        obj : Warehouse
            The warehouse instance.

        Returns
        -------
        int
            The number of stock items.
        """
        return obj.stocks.count()

    def get_user_roles(self, obj):
        """
        Return a list of users and their roles in the warehouse.

        Parameters
        ----------
        obj : Warehouse
            The warehouse instance.

        Returns
        -------
        list
            A list of dictionaries containing the user ID and role.
        """
        return [
            {
                "user_id": user.user.id,
                "role": user.role,
            }
            for user in obj.users.all()
        ]

    class Meta:
        model = Warehouse
        fields = "__all__"
        extra_kwargs = {
            "slug": {"required": False, "read_only": True},
            "author": {"required": False},
            "is_active": {"required": False},
        }


class WarehouseUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the WarehouseUser model.
    """

    class Meta:
        model = WarehouseUser
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Stock model.
    """

    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    product_variant = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all()
    )

    class Meta:
        model = Stock
        fields = "__all__"


class StockTransferSerializer(serializers.ModelSerializer):
    """
    Serializer for the StockTransfer model.
    """

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        write_only=True,
    )
    product_variant = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all()
    )
    from_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all()
    )
    to_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
    )

    class Meta:
        model = StockTransfer
        fields = "__all__"
        extra_kwargs = {
            "reference_code": {"read_only": True},
        }
