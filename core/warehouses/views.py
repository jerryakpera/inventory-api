"""
Views for the `warehouses` app.
"""

from django.db.utils import IntegrityError
from rest_framework import authentication, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.products.pagination import StandardPagination

from . import models as warehouse_models
from . import serializers as warehouse_serializers


class WarehouseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Warehouse model.
    """

    pagination_class = StandardPagination
    queryset = warehouse_models.Warehouse.objects.all().order_by("id")
    serializer_class = warehouse_serializers.WarehouseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    def perform_create(self, serializer):
        """
        Set the current authenticated user as the owner when creating a warehouse.

        Parameters
        ----------
        serializer : WarehouseSerializer
            The serializer instance.
        """
        try:
            serializer.save(owner=self.request.user)
        except IntegrityError as e:
            if "warehouses_warehouse_slug_key" in str(e):
                raise ValidationError(
                    {
                        "slug": [
                            "A warehouse with this slug already exists.",
                        ],
                    }
                )
            raise ValidationError({"error": "An unexpected database error occurred."})


class StockViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Stock model.
    """

    pagination_class = StandardPagination
    queryset = warehouse_models.Stock.objects.all().order_by("id")
    serializer_class = warehouse_serializers.StockSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    def perform_create(self, serializer):
        """
        Handle unique constraint violations properly when creating stock records.

        Parameters
        ----------
        serializer : StockSerializer
            The serializer instance.
        """
        try:
            serializer.save()
        except IntegrityError as e:
            if "warehouses_stock_unique_constraint" in str(e):
                raise ValidationError(
                    {
                        "detail": "Stock record already exists for this product in the warehouse."
                    }
                )
            raise ValidationError({"error": "An unexpected database error occurred."})


class StockTransferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the StockTransfer model.
    """

    pagination_class = StandardPagination
    queryset = warehouse_models.StockTransfer.objects.all().order_by("id")
    serializer_class = warehouse_serializers.StockTransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    def perform_create(self, serializer):
        """
        Set the current authenticated user as the initiator when creating a stock transfer.

        Parameters
        ----------
        serializer : StockTransferSerializer
            The serializer instance.
        """

        try:
            serializer.save(initiated_by=self.request.user)
        except IntegrityError as e:
            if "warehouses_stocktransfer_unique_constraint" in str(e):
                raise ValidationError(
                    {
                        "detail": "A stock transfer with these details already exists.",
                    }
                )
            raise ValidationError({"error": "An unexpected database error occurred."})
