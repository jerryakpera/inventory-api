"""
Admin configuration for the products app.
"""

from django.contrib import admin

from .models import Product, ProductCategory, ProductUnit, ProductVariant

admin.site.register(ProductUnit)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductCategory model.
    """

    prepopulated_fields = {
        "slug": ("name",),
    }

    search_fields = ("name",)
    list_display = ("name", "slug")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    """

    prepopulated_fields = {
        "slug": ("name",),
    }

    def get_tags(self, obj):
        """
        Return the tags of the product.

        Parameters
        ----------
        obj : Product
            The product instance.

        Returns
        -------
        str
            The tags of the product.
        """
        return ", ".join(obj.tags.names())

    raw_id_fields = ["author"]
    date_hierarchy = "created"
    ordering = ["name", "category"]
    list_filter = ("category", "unit")
    search_fields = ("name", "category__name")
    list_display = ("name", "category", "unit", "get_tags")

    show_facets = admin.ShowFacets.ALWAYS


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductVariant model.
    """

    raw_id_fields = ["product"]
    list_display = ("product", "price", "stock")
    list_filter = ("product",)
    search_fields = ("product__name",)
    ordering = [
        "product",
    ]
    show_facets = admin.ShowFacets.ALWAYS
