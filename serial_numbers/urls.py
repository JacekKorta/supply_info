from django.urls import path

from serial_numbers import views

app_name = 'serial_numbers'

urlpatterns = [
    path('save_shipment/', views.save_shipment, name='save_shipment'),
    path('register_machines/', views.register_machines_in_warehouse, name='register_machines_in_warehouse')
]