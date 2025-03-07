"""
URL configuration for core project.
"""

from decouple import config
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.custom_user import views as custom_user_views
from core.products import views as product_views
from core.suppliers import views as supplier_views
from core.warehouses import views as warehouse_views

router = DefaultRouter()

router.register(r"products", product_views.ProductViewSet)
router.register(r"categories", product_views.ProductCategoryViewSet)
router.register(r"units", product_views.ProductUnitViewSet)
router.register(r"variants", product_views.ProductVariantViewSet)
router.register(r"price-histories", product_views.ProductPriceHistoryViewSet)

router.register(r"warehouses", warehouse_views.WarehouseViewSet)
router.register(r"stocks", warehouse_views.StockViewSet)
router.register(r"stock-transfers", warehouse_views.StockTransferViewSet)
router.register(r"stock-adjustments", warehouse_views.StockAdjustmentViewSet)
router.register(r"stock-audits", warehouse_views.StockAuditViewSet)
router.register(r"stock-alert", warehouse_views.StockAlertViewSet)

router.register(r"suppliers", supplier_views.SupplierViewSet)
router.register(r"supplier-products", supplier_views.SupplierProductViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/token/logout/",
        custom_user_views.LogoutView.as_view(),
    ),
    path("api/v1/users/me/", custom_user_views.get_current_user),
    path("api/v1/", include(router.urls)),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/",
        custom_user_views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        custom_user_views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]

if settings.DEBUG:
    # If in production
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

admin.site.site_title = config(
    "ADMIN_SITE_SITE_TITLE",
    "Django administration",
)
admin.site.index_title = config(
    "ADMIN_SITE_INDEX_TITLE",
    "Site administration",
)
admin.site.site_header = config(
    "ADMIN_SITE_SITE_HEADER",
    "Django administration",
)
