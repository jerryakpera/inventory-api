"""
Logic for paginating products.
"""

from rest_framework.pagination import LimitOffsetPagination


class StandardPagination(LimitOffsetPagination):
    """
    Standard pagination for the `products` app.
    """

    default_limit = 10
    limit_query_param = "limit"
    offset_query_param = "offset"
