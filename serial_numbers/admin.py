from django.contrib import admin
from .models import Customer, Machine, ShipmentToCustomer


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'tax_number']}),
        ]


class MachineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['code', 'serial_number', 'delivery_date']}),
        ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Machine, MachineAdmin)