from django.urls import path

from . import views

app_name = 'supply_info'

urlpatterns = [
    path('', views.index, name='index'),
    path('lista-maszyn/', views.machines_list, name='machines_list'),
    path('lista-produktow/<sub_type>', views.product_list, name='products_list'),
    path('zasil-baze-produktow/', views.update_product_info, name='update_product_info'),
    path('uaktualnij-stany/', views.update_product_availability, name='update_product_availability'),
    path('wyszukaj-produkt/', views.search_product, name='search_product'),
    path('konto/zmien-haslo/', views.change_password, name='change_password'),
    path('api/products/', views.ApiProductList.as_view()),
    path('api/products/<code>', views.ApiProductDetail.as_view()),
    path('api/availability/', views.ApiAvailabilityList.as_view()),
    path('api/availability/<product_code>', views.ApiAvailabilityDetail.as_view()),
]