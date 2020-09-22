from django.urls import path

from payments import views

app_name = 'payments'

urlpatterns = [
    path('read_invoices_data/', views.read_invoices_data, name='read_invoices_data'),
    path('delayed_invoices/', views.delayed_invoices_handle, name='delayed_invoices'),
    ]