from django.contrib import admin
from shipments.models import Shipment, ShipmentDetail

class ShipmentInLineAdmin(admin.TabularInline):
    model = ShipmentDetail
    raw_id_fields = ('product',)
    extra = 1


class ShipmentAdmin(admin.ModelAdmin):
    fields = ['shipment_number', 'estimated_time_arrival', 'shipment_status', 'country_of_origin']
    list_display = ['shipment_number', 'country_of_origin', 'estimated_time_arrival', 'shipment_status', ]
    list_filter = ['country_of_origin', 'estimated_time_arrival', 'shipment_status', ]
    date_hierarchy = 'estimated_time_arrival'
    inlines = [ShipmentInLineAdmin]

admin.site.register(Shipment, ShipmentAdmin)
#admin.site.register(ShipmentDetail, ShipmentDetailAdmin)