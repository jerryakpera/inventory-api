"""
Views for the `products` app.
"""

from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
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

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    filterset_fields = ["category", "unit", "is_active"]
    search_fields = ["name", "slug", "category__name", "description"]
    ordering_fields = ["name", "category", "unit", "is_active", "updated", "created"]

    ordering = ["id"]

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
                        "slug": ["A similar product already exists."],
                    }
                )
            raise ValidationError(
                {"error": "An unexpected database error occurred."},
            )

    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        """
        Custom action to delete multiple products at once.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        product_ids = request.data.get("ids", [])

        if not isinstance(product_ids, list) or not product_ids:
            return Response(
                {"error": "Please provide a list of product IDs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_count, _ = product_models.Product.objects.filter(
            id__in=product_ids
        ).delete()
        return Response(
            {
                "message": f"Successfully deleted {deleted_count} products.",
            },
            status=status.HTTP_200_OK,
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

    filter_backends = [SearchFilter, OrderingFilter]

    ordering_fields = ["name", "updated"]
    search_fields = ["name", "slug", "description"]

    ordering = ["id"]

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the request type.

        Returns
        -------
        ProductCategorySerializer or ProductCategoryDetailSerializer
            The appropriate serializer based on the request type.
        """
        if self.action == "retrieve":
            return product_serializers.ProductCategoryDetailSerializer

        return product_serializers.ProductCategorySerializer

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

    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        """
        Custom action to delete multiple categories at once.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        categories_ids = request.data.get("ids", [])

        if not isinstance(categories_ids, list) or not categories_ids:
            return Response(
                {"error": "Please provide a list of category IDs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_count, _ = product_models.ProductCategory.objects.filter(
            id__in=categories_ids
        ).delete()
        return Response(
            {
                "message": f"Successfully deleted {deleted_count} categories.",
            },
            status=status.HTTP_200_OK,
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

    filter_backends = [SearchFilter, OrderingFilter]

    ordering_fields = ["name", "product", "flavor", "brand", "is_active", "updated"]
    search_fields = ["name", "slug", "product__name", "description", "flavor", "brand"]

    ordering = ["id"]

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
