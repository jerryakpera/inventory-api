"""
URL configuration for the warehouses app in the inventory API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "warehouses"

router = DefaultRouter()

router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"stocks", views.StockViewSet)
router.register(r"stock-transfers", views.StockTransferViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
