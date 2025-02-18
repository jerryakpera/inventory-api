"""
This module contains the views for the inventory API.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.api.utils import log_this


@api_view(["GET"])
def health_check(request):
    """
    View for health check endpoint.

    Parameters
    ----------
    request : HttpRequest
        The request object.

    Returns
    -------
    Response
        JSON response with status "ok".
    """
    return Response(
        {"status": "ok"},
    )
