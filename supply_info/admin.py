from django.contrib import admin

from supply_info.models import ActiveProductList, PriceList, Product, ProductAvailability, Alert


class ActiveProductInLine(admin.StackedInline):
    model = ActiveProductList
    extra = 0


class PriceListInLine(admin.TabularInline):
    model = PriceList
    extra = 0


class ProductAvailabilityInLine(admin.TabularInline):
    model = ProductAvailability
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['code', 'name', 'next_shipment','additional_info']}),
        ('Dodatkowe informacje:', {'fields': ['manufacturer', 'site_address'], 'classes': ['collapse']}),
        ('Grupy:', {'fields': ['type', 'sub_type', 'mark'], 'classes': ['collapse']}),

    ]
    inlines = [ActiveProductInLine, PriceListInLine, ProductAvailabilityInLine]

    list_display = ('code', 'name', )
    search_fields = ['code', 'name']
    list_filter = ['type', 'sub_type']

    actions = ['change_activity_status']

    def change_activity_status(self, request, queryset):
        print(type(queryset[0]))
        print(queryset[0].code)
        for product_in_query in queryset:
            a = ActiveProductList.objects.filter(product_code__code=product_in_query)
            if a:
                new_status = (not a[0].is_active)
                a[0].change_activity(new_status)
        pass


class ActiveProductListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['product_code', 'is_active']}),
        ]
    list_display = ('product_code', 'is_active')
    list_filter = ['is_active']
    search_fields = ['product_code']


class ProductsAlertsAdmin(admin.ModelAdmin):

    def change_status_to_inactive(self, request, queryset):
        queryset.update(is_active=False)

    raw_id_fields = ('product', 'user')
    change_status_to_inactive.short_description = 'Deaktywuj alerty'

    fieldsets = [
        (None, {'fields': ['user', 'product', 'less_or_equal', 'qty_alert_lvl', 'is_active', 'created', 'updated']}),
        ]
    readonly_fields = ['created', 'updated']
    list_display = ('user', 'product', 'less_or_equal', 'qty_alert_lvl', 'created', 'updated', 'is_active')
    list_filter = ('user', 'is_active')
    actions = [change_status_to_inactive,]
    search_fields = ['product__code']


admin.site.register(Product, ProductAdmin)
admin.site.register(ActiveProductList, ActiveProductListAdmin )
admin.site.register(Alert, ProductsAlertsAdmin)

