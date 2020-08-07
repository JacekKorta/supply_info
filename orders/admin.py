from django.contrib import admin

from orders.models import Order, OrderDetail


class OrderDetailInLineAdmin(admin.TabularInline):
    model = OrderDetail
    raw_id_fields = ('product',)
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    fields = ['customer_id', 'order_date', 'order_status', 'sell_date']
    inlines = [OrderDetailInLineAdmin]



# class OrderDetailAdmin(admin.ModelAdmin):
  #   fields = ['order', 'product', 'quantity']


admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderDetail, OrderDetailAdmin)
