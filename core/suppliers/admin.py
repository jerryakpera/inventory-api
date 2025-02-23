"""
Admin configuration for the suppliers app.
"""

from django.contrib import admin

from .models import Supplier, SupplierProduct


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Supplier model.
    """

    search_fields = (
        "business_name",
        "contact_person",
        "email",
        "phone",
        "country",
        "city",
    )
    list_display = (
        "business_name",
        "contact_person",
        "email",
        "phone",
        "country",
        "city",
        "created",
        "updated",
    )
    list_filter = ("country", "city")
    ordering = ("business_name",)
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SupplierProduct model.
    """

    search_fields = ("supplier__business_name", "product_variant__product__name")
    list_display = ("supplier", "product_variant", "price", "created", "updated")
    list_filter = ("supplier", "product_variant")
    ordering = ("supplier", "product_variant")
    raw_id_fields = ("supplier", "product_variant")
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS
