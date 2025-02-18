"""
URL configuration for the inventory API.
"""

from django.urls import include, path

from . import views

app_name = "api"

urlpatterns = [
    path(
        "health-check/",
        views.health_check,
        name="health-check",
    ),
    path(
        "products/",
        include("core.products.urls"),
    ),
]
