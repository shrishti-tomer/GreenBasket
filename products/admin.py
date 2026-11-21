

from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class StockStatusFilter(admin.SimpleListFilter):
    title = 'Stock Status'
    parameter_name = 'stock_status'

    def lookups(self, request, model_admin):
        return [
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'in_stock':
            return queryset.filter(stock_quantity__gt=10)

        if self.value() == 'low_stock':
            return queryset.filter(
                stock_quantity__gt=0,
                stock_quantity__lte=10
            )

        if self.value() == 'out_of_stock':
            return queryset.filter(stock_quantity=0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'stock_quantity',
        'stock_status',
    )

    list_filter = ('category', StockStatusFilter)
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity')
    ordering = ('name',)

    @admin.display(description='Stock Status')
    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return "Out of Stock"
        elif obj.stock_quantity <= 10:
            return "Low Stock"
        return "In Stock"
