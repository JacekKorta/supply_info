from django.urls import path
from shipments import views


app_name = 'shipments'

urlpatterns = [
    # shipment views
    path('dostawy/', views.shipments_view, name='shipments_view'),
    path('dostawy/nowa', views.add_new_shipment, name='add_new_shipment'),
    ]