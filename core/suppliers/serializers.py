"""
Serializers for the suppliers app.
"""

from rest_framework import serializers

from core.custom_user.models import User
from core.products.models import ProductVariant

from .models import Supplier, SupplierProduct


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.
    """

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        write_only=True,
    )
    product_count = serializers.SerializerMethodField()

    def get_product_count(self, obj):
        """
        Return the number of products associated with this supplier.

        Parameters
        ----------
        obj : Supplier
            The supplier instance.

        Returns
        -------
        int
            The number of products associated with this supplier.
        """
        return obj.products.count()

    class Meta:
        model = Supplier
        fields = "__all__"
        extra_kwargs = {
            "author": {"required": False},
        }


class SupplierProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the SupplierProduct model.
    """

    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    product_variant = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all()
    )

    class Meta:
        model = SupplierProduct
        fields = "__all__"


class SupplierProductDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the SupplierProduct model.
    Includes product and supplier details.
    """

    supplier = SupplierSerializer(read_only=True)
    product_variant = serializers.CharField(
        source="product_variant.product.name",
        read_only=True,
    )

    class Meta:
        model = SupplierProduct
        fields = "__all__"
        depth = 1
