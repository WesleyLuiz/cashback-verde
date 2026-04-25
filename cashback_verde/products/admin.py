from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'item_type',
        'category',
        'city',
        'price',
        'cashback_percentage',
    )
    list_filter = ('item_type', 'category', 'city')
    search_fields = ('name', 'description')
