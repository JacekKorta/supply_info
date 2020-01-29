from django.urls import path

from . import views, api_views

app_name = 'supply_info'

urlpatterns = [
    path('', views.index, name='index'),
    path('lista-maszyn/', views.machines_list, name='machines_list'),
    path('lista-produktow/<sub_type>', views.product_list, name='products_list'),
    path('zasil-baze-produktow/', views.update_product_info, name='update_product_info'),
    path('uaktualnij-stany/', views.update_product_availability, name='update_product_availability'),
    path('wyszukaj-produkt/', views.search_product, name='search_product'),
    path('konto/zmien-haslo/', views.change_password, name='change_password'),
    path('api/products/', api_views.ApiProductList.as_view()),
    path('api/products/<code>', api_views.ApiProductDetail.as_view()),
    path('api/availability/', api_views.ApiAvailabilityList.as_view()),
    path('api/availability/<product_code>', api_views.ApiAvailabilityDetail.as_view()),
]