"""
Views for the `products` app.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models as product_models
from . import serializers as product_serializers


@api_view(["GET"])
def list_products(request):
    """
    DRF View for listing products.

    Parameters
    ----------
    request : HttpRequest
        The request object.

    Returns
    -------
    HttpResponse
        The response object.
    """
    return Response(
        {"message": "Listing products"},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_product(request, product_id):
    """
    DRF View for getting a product.

    Parameters
    ----------
    request : HttpRequest
        The request object.
    product_id : int
        The ID of the product.

    Returns
    -------
    HttpResponse
        The response object.
    """

    try:
        instance = product_models.ProductVariant.objects.get(pk=product_id)
    except product_models.ProductVariant.DoesNotExist:
        return Response(
            {
                "data": {},
                "message": "Product not found",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = product_serializers.ProductVariantSerializer(instance)
    data = serializer.data

    return Response(
        {
            "data": data,
            "message": "Product retrieved successfully",
        },
        status=status.HTTP_200_OK,
    )
