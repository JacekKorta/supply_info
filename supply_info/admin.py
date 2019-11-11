from django.contrib import admin
from .models import ActiveProductList, PriceList, Product

class ActiveProductInLine(admin.StackedInline):
    model = ActiveProductList
    extra = 0


class PriceListInLine(admin.TabularInline):
    model = PriceList
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['code', 'name', 'additional_info']}),
        ('Dodatkowe informacje:', {'fields': ['manufacturer', 'site_address'], 'classes': ['collapse']}),
        ('Grupy:', {'fields': ['type', 'sub_type', 'mark'], 'classes': ['collapse']}),

    ]
    inlines = [ActiveProductInLine, PriceListInLine]

    list_display = ('code', 'name', )


class ActiveProductListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['product_code', 'is_active']}),
        ]
    list_display = ('product_code', 'is_active')
    list_filter = ['is_active']



admin.site.register(Product, ProductAdmin)
admin.site.register(ActiveProductList, ActiveProductListAdmin )

