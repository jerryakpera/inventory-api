"""
Views for the `products` app.
"""

from rest_framework import authentication, generics, mixins, permissions

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

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.SessionAuthentication]

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


class ProductVariantMixinView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    A view for the `ProductVariant` model that supports all CRUD operations.
    """

    lookup_field = "pk"
    queryset = product_models.ProductVariant.objects.all()

    def get_serializer_class(self):
        """
        Return different serializers based on the request type.

        Returns
        -------
        rest_framework.serializers.ModelSerializer
            The serializer class to use.
        """
        if self.request.method == "GET" and self.kwargs.get("pk"):
            return product_serializers.ProductVariantDetailSerializer

        return product_serializers.ProductVariantSerializer

    def perform_create(self, serializer):
        """
        Override perform_create to set a default author if not provided.

        Parameters
        ----------
        serializer : rest_framework.serializers.ModelSerializer
            The serializer instance.
        """
        if not serializer.validated_data.get("author"):
            serializer.save(author_id=1)
        else:
            serializer.save()

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


class ProductPriceHistoryMixinView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    A view for the `ProductPriceHistory` model that supports all CRUD operations.
    """

    lookup_field = "pk"
    queryset = product_models.ProductPriceHistory.objects.all()
    serializer_class = product_serializers.ProductPriceHistorySerializer

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
