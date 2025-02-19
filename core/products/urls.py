"""
URL configuration for the products app in the inventory API.
"""

from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path(
        "<int:pk>/",
        views.ProductMixinView.as_view(),
    ),
    path(
        "",
        views.ProductMixinView.as_view(),
    ),
    path(
        "categories/<int:pk>/",
        views.ProductCategoryMixinView.as_view(),
    ),
    path(
        "categories/",
        views.ProductCategoryMixinView.as_view(),
    ),
]
