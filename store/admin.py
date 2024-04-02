from django.contrib import admin
from .models import Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'description', 'price', 'stock', 'is_available', 'modified_at')
    prepopulated_fields = {"slug": ("product_name",)}


# Register your models here.
admin.site.register(Product, CategoryAdmin)
