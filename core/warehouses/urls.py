"""
URL configuration for the warehouses app in the inventory API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "warehouses"

router = DefaultRouter()

router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"stock-transfers", views.StockTransferViewSet)
router.register(r"stock-adjustments", views.StockAdjustmentViewSet)
router.register(r"stock-audits", views.StockAuditViewSet)
router.register(r"stock-alert", views.StockAlertViewSet)
router.register(r"stocks", views.StockViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
