"""
Admin configuration for the `warehouses` app.
"""

from django.contrib import admin

from .models import Stock, StockTransfer, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the `Warehouse` model.
    """

    raw_id_fields = ("author",)
    list_display = ("name", "location", "is_active", "created", "updated")
    search_fields = ("name", "location")
    list_filter = ("is_active", "created", "updated")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created",)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """
    Admin configuration for the `Stock` model.
    """

    list_display = ("warehouse", "product_variant", "quantity", "low_stock_threshold")
    search_fields = ("warehouse__name", "product_variant__name")
    list_filter = ("warehouse",)
    ordering = ("warehouse", "product_variant")


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    """
    Admin configuration for the `StockTransfer` model.
    """

    list_display = (
        "reference_code",
        "product_variant",
        "from_warehouse",
        "to_warehouse",
        "quantity",
        "created",
    )
    search_fields = (
        "reference_code",
        "from_warehouse__name",
        "to_warehouse__name",
        "product_variant__name",
    )
    list_filter = ("created", "from_warehouse", "to_warehouse")
    ordering = ("-created",)
