from django.urls import path

from . import views

app_name = 'supply_info'

urlpatterns = [
    path('', views.index, name='index'),
    path('machine_list/', views.machine_list, name='machine_list'),
    path('update_product_info/', views.update_product_info, name='update_product_info'),

]