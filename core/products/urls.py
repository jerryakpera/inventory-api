"""
URL configuration for the products app in the inventory API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "products"

router = DefaultRouter()

router.register(r"products", views.ProductViewSet)
router.register(r"units", views.ProductUnitViewSet)
router.register(r"variants", views.ProductVariantViewSet)
router.register(r"categories", views.ProductCategoryViewSet)
router.register(r"price-histories", views.ProductPriceHistoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
