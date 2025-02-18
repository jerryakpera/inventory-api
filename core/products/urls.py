"""
URL configuration for the products app in the inventory API.
"""

from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path(
        "",
        views.list_products,
        name="list-products",
    ),
    path(
        "<int:product_id>/",
        views.get_product,
        name="get-product",
    ),
]
