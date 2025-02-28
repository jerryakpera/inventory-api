"""
Views for the `products` app.
"""

from django.db.utils import IntegrityError
from rest_framework import authentication, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import models as product_models
from . import serializers as product_serializers
from .pagination import StandardPagination


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Product model.
    """

    pagination_class = StandardPagination
    queryset = product_models.Product.objects.all().order_by("id")
    serializer_class = product_serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    filter_backends = [SearchFilter]
    search_fields = ["name", "slug", "category__name", "description"]

    def perform_create(self, serializer):
        """
        Set the current authenticated user as the author when creating a product.
        Handle unique constraint violations properly.

        Parameters
        ----------
        serializer : ProductSerializer
            The serializer instance used to create the product.
        """
        try:
            serializer.save(author=self.request.user)
        except IntegrityError as e:
            if "products_product_slug_key" in str(e):
                raise ValidationError(
                    {
                        "slug": ["A product with this slug already exists."],
                    }
                )
            raise ValidationError(
                {"error": "An unexpected database error occurred."},
            )


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductCategory model.
    """

    pagination_class = StandardPagination
    queryset = product_models.ProductCategory.objects.all()
    serializer_class = product_serializers.ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    filter_backends = [SearchFilter]
    search_fields = ["name", "slug", "description"]

    def perform_create(self, serializer):
        """
        Set the current authenticated user as the author when
        creating a product category.

        Handle unique constraint violations properly.

        Parameters
        ----------
        serializer : ProductSerializer
            The serializer instance used to create the product category.
        """
        try:
            serializer.save()
        except IntegrityError as e:
            if "products_productcategory_slug_key" in str(e):
                raise ValidationError(
                    {
                        "slug": ["A product category with this slug already exists."],
                    }
                )
            raise ValidationError(
                {"error": "An unexpected database error occurred."},
            )


class ProductUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductUnit model.
    """

    pagination_class = StandardPagination
    queryset = product_models.ProductUnit.objects.all()
    serializer_class = product_serializers.ProductUnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductVariant model.
    """

    pagination_class = StandardPagination
    queryset = product_models.ProductVariant.objects.all().order_by("id")
    serializer_class = product_serializers.ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]

    filter_backends = [SearchFilter]
    search_fields = ["name", "slug", "product__name", "description", "flavor", "brand"]

    def perform_create(self, serializer):
        """
        Set the current authenticated user as the author
        when creating a product variant.

        Handle unique constraint violations properly.

        Parameters
        ----------
        serializer : ProductSerializer
            The serializer instance used to create the product variant.
        """
        try:
            serializer.save(author=self.request.user)
        except IntegrityError as e:
            if "products_productvariant_slug_key" in str(e):
                raise ValidationError(
                    {
                        "slug": ["A product variant with this slug already exists."],
                    }
                )
            raise ValidationError(
                {"error": "An unexpected database error occurred."},
            )


class ProductPriceHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ProductPriceHistory model.
    """

    pagination_class = StandardPagination
    queryset = product_models.ProductPriceHistory.objects.all()
    serializer_class = product_serializers.ProductPriceHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        JWTAuthentication,
    ]
