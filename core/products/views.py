"""
Views for the `products` app.
"""

from rest_framework import authentication, permissions, viewsets

from . import models as product_models
from . import serializers as product_serializers


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Product model.
    """

    queryset = product_models.Product.objects.all()
    serializer_class = product_serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductCategory model.
    """

    queryset = product_models.ProductCategory.objects.all()
    serializer_class = product_serializers.ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]


class ProductUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductUnit model.
    """

    queryset = product_models.ProductUnit.objects.all()
    serializer_class = product_serializers.ProductUnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductVariant model.
    """

    queryset = product_models.ProductVariant.objects.all()
    serializer_class = product_serializers.ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]


class ProductPriceHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductPriceHistory model.
    """

    queryset = product_models.ProductPriceHistory.objects.all()
    serializer_class = product_serializers.ProductPriceHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]
