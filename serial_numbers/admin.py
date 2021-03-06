from django.contrib import admin

from serial_numbers.models import Customer, Machine, ShipmentToCustomer
from serial_numbers.sn_modules.admin_addons import AdminAddons

class ShipmentToCustomerInLineAdmin(admin.TabularInline):
    model = ShipmentToCustomer
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'user_name', 'tax_number', 'email']}),
        ]
    list_display = ['name', 'user_name', 'tax_number', 'email']
    search_fields = ['name', 'tax_number', 'email']


class MachineAdmin(admin.ModelAdmin):
    def get_delivery_note_number(self, obj):
        shipment = ShipmentToCustomer.objects.filter(item=obj)
        if shipment.exists():
            return shipment.first().delivery_note_number
        else:
            return None

    def get_sales_date(self, obj):
        shipment = ShipmentToCustomer.objects.filter(item=obj)
        if shipment.exists():
            return shipment.first().shipment_date
        else:
            return None

    fieldsets = [
        (None, {'fields': ['code', 'serial_number', 'delivery_date']}),
        ]
    inlines = [ShipmentToCustomerInLineAdmin]

    list_display = ['code',
                    'serial_number',
                    'delivery_date',
                    'get_delivery_note_number',
                    'get_sales_date']

    get_delivery_note_number.short_description = 'Dokument wydania'
    get_delivery_note_number.admin_order_field = 'id'
    get_sales_date.short_description = 'Data wydania'
    get_sales_date.admin_order_field = 'id'
    search_fields = ['code',
                     'serial_number',
                     'shipmenttocustomer__shipment_date',
                     'shipmenttocustomer__delivery_note_number']

    list_filter = ['shipmenttocustomer__shipment_date', 'code',]


class ShipmentAdmin(admin.ModelAdmin):
    readonly_fields = ('shipment_date',)
    fieldsets = [
        (None, {'fields': ['shipment_date']}),
        (None, {'fields': ['delivery_note_number', 'customer', 'item']})
        ]

    def get_machine_sn(self, obj):
        return obj.item.serial_number

    get_machine_sn.admin_order_field = 'item__serial_number'
    get_machine_sn.short_description = 'Numer seryjny'
    date_hierarchy = 'shipment_date'

    list_display = ['delivery_note_number',
                    'customer',
                    'item',
                    'get_machine_sn',
                    'shipment_date']

    search_fields = ['delivery_note_number',
                     'item_id__code',
                     'item_id__serial_number',
                     'shipment_date',
                     'customer__name']
    list_filter = ['shipment_date', 'item_id__code',]

    AdminAddons.create_csv_report_serial_numbers.short_description = 'Pobierz raport'

    actions = [AdminAddons.create_csv_report_serial_numbers,]

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(ShipmentToCustomer, ShipmentAdmin)