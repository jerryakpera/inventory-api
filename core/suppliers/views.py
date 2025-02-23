"""
Views for the `suppliers` app.
"""

from django.db.utils import IntegrityError
from rest_framework import authentication, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.products.pagination import StandardPagination

from . import models as supplier_models
from . import serializers as supplier_serializers


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Supplier model.
    """

    pagination_class = StandardPagination
    queryset = supplier_models.Supplier.objects.all().order_by("id")
    serializer_class = supplier_serializers.SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    def perform_create(self, serializer):
        """
        Set the current authenticated user as the author when creating a supplier.
        Handle unique constraint violations properly.

        Parameters
        ----------
        serializer : SupplierSerializer
            The serializer instance used to create the supplier.
        """
        try:
            serializer.save(author=self.request.user)
        except IntegrityError as e:
            if "suppliers_supplier_slug_key" in str(e):
                raise ValidationError(
                    {
                        "slug": [
                            "A supplier with this slug already exists.",
                        ],
                    }
                )
            raise ValidationError({"error": "An unexpected database error occurred."})


class SupplierProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the SupplierProduct model.
    """

    pagination_class = StandardPagination
    queryset = supplier_models.SupplierProduct.objects.all().order_by("id")
    serializer_class = supplier_serializers.SupplierProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    def perform_create(self, serializer):
        """
        Set the current authenticated user as the author when creating a supplier product.
        Handle unique constraint violations properly.

        Parameters
        ----------
        serializer : SupplierProductSerializer
            The serializer instance used to create the supplier product.
        """
        try:
            serializer.save()
        except IntegrityError as e:
            if "suppliers_supplierproduct_supplier_id_product_id_key" in str(e):
                raise ValidationError(
                    {
                        "non_field_errors": [
                            "This supplier already supplies this product.",
                        ],
                    }
                )
            raise ValidationError(
                {
                    "error": "An unexpected database error occurred.",
                },
            )
