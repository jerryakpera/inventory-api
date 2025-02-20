"""
URL configuration for core project.
"""

from decouple import config
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.products.urls")),
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
