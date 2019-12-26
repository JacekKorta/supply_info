from django.urls import path

from . import views

app_name = 'supply_info'

urlpatterns = [
    path('', views.index, name='index'),
    path('machine_list/', views.machine_list, name='machine_list'),
    path('update_product_info/', views.update_product_info, name='update_product_info'),
    path('update_product_availability/', views.update_product_availability, name='update_product_availability'),
    path('search_product/', views.search_product, name='search_product'),
    path('api/products/', views.ApiProductList.as_view()),
    path('api/products/<code>', views.ApiProductDetail.as_view()),
    path('api/availability/', views.ApiAvailabilityList.as_view()),
    path('api/availability/<product_code>', views.ApiAvailabilityDetail.as_view()),
]