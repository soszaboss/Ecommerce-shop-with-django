from django.contrib import admin
from .models import Product, AttributeVariant, Variant


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id' ,'product_name', 'description', 'price', 'stock', 'is_available', 'modified_at')
    prepopulated_fields = {"slug": ("product_name",)}


class AttributeVariantAdmin(admin.ModelAdmin):
    list_display = ('id' ,'product', 'variant', 'attribut_variant_name', 'is_available', 'modified_at')
    list_editable = ('is_available',)


# Register your models here.
admin.site.register(Product, CategoryAdmin)
admin.site.register(Variant)
admin.site.register(AttributeVariant, AttributeVariantAdmin)
# admin.site.register(ProductVariant)
