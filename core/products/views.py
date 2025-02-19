"""
Views for the `products` app.
"""

from rest_framework import generics, mixins

from core.api.utils import log_this

from . import models as product_models
from . import serializers as product_serializers


class ProductMixinView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    A view for the `Product` model that supports all CRUD operations.
    """

    lookup_field = "pk"
    queryset = product_models.Product.objects.all()
    serializer_class = product_serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """
        pk = kwargs.get("pk")

        if pk:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """

        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """
        return self.destroy(request, *args, **kwargs)


class ProductCategoryMixinView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    A view for the `ProductCategory` model that supports all CRUD operations.
    """

    lookup_field = "pk"
    queryset = product_models.ProductCategory.objects.all()
    serializer_class = product_serializers.ProductCategorySerializer

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """
        pk = kwargs.get("pk")

        if pk:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """

        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """
        return self.destroy(request, *args, **kwargs)


class ProductUnitMixinView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    A view for the `ProductUnit` model that supports all CRUD operations.
    """

    lookup_field = "pk"
    queryset = product_models.ProductUnit.objects.all()
    serializer_class = product_serializers.ProductUnitSerializer

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """
        pk = kwargs.get("pk")

        if pk:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """

        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object.
        *args : list
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        rest_framework.response.Response
            The response object.
        """
        return self.destroy(request, *args, **kwargs)
