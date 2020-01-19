from django.urls import path

from . import views

app_name = 'serial_numbers'

urlpatterns = [
    path('update_shipment/', views.saveShippment, name='update_shipment'),
]