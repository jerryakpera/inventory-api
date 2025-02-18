"""
Views for the `products` app.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
