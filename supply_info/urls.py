from django.urls import path

from supply_info import api_views, views

app_name = 'supply_info'

urlpatterns = [
    path('', views.index, name='index'),
    path('alerty/<only_active>', views.alerts_list_view, name='alerts_list_view'),
    path('edytuj-alert/<int:alert_pk>', views.alert_edit_view, name='alert_edit_view'),
    path('dodaj-alert/<int:product_pk>', views.alert_add_view, name='alert_add_view'),
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