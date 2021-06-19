import logging

from django.contrib import admin

from supply_info.models import Product, Alert

logger = logging.getLogger(__name__)


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['code', 'name', 'next_shipment','additional_info', 'is_active', 'synchronize']}
         ),
        ('Ceny:',
         {'fields': ['price_a', 'price_b', 'price_c', 'price_d']}),
        ('Grupy:',
         {'fields': ['type', 'sub_type', 'mark']}),
        ('Dodatkowe informacje:',
         {'fields': ['manufacturer', 'site_address']}
         ),
        ('Dostepność:',
         {'fields': ['availability', 'not_enough', 'unavailable']})
    ]

    list_display = ('code', 'name', 'type', 'sub_type', 'is_active', 'synchronize', 'mark')
    search_fields = ['code', 'name', 'type', 'sub_type']
    list_filter = ['type', 'sub_type', 'is_active', 'synchronize', 'mark']

    actions = ['change_activity_status', 'change_synchronize_status']

    @admin.action(description='Zmień status aktywności produktu')
    def change_activity_status(self, request, queryset):
        logger.debug(type(queryset[0]))
        logger.debug(queryset[0].code)
        for product_in_query in queryset:
            new_status = (not product_in_query.is_active)
            product_in_query.change_activity(new_status)
        pass

    @admin.action(description='Zmień status synchronizacji produktu')
    def change_synchronize_status(self, request, queryset):
        logger.debug(type(queryset[0]))
        logger.debug(queryset[0].code)
        for product_in_query in queryset:
            new_status = (not product_in_query.synchronize)
            product_in_query.change_synchronize(new_status)
        pass


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
admin.site.register(Alert, ProductsAlertsAdmin)

