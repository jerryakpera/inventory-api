"""
Admin configuration for the products app.
"""

from django.contrib import admin

from .models import (
    Product,
    ProductCategory,
    ProductUnit,
    ProductVariant,
    ProductVariantImage,
)

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


class ProductVariantImageInline(admin.TabularInline):
    """
    Inline configuration for the ProductVariantImage model.
    """

    model = ProductVariantImage
    extra = 1
    max_num = 3


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductVariant model.
    """

    inlines = [ProductVariantImageInline]

    def get_default_image(self, obj):
        """
        Return the default image of the product variant.

        Parameters
        ----------
        obj : ProductVariant
            The product variant instance.

        Returns
        -------
        str
            The default image of the product variant.
        """

        return obj.get_default_image()

    get_default_image.short_description = "Default Image"

    raw_id_fields = ["product", "author"]
    list_display = ("product", "price", "stock", "get_default_image")
    list_filter = ("product",)
    search_fields = ("product__name",)
    ordering = [
        "product",
    ]
    show_facets = admin.ShowFacets.ALWAYS
