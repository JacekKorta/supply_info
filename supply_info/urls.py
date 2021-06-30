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
    path('wyszukaj-produkt/', views.search_product, name='search_product'),
    path('konto/zmien-haslo/', views.change_password, name='change_password'),
    path('api/products/', api_views.ApiProductList.as_view()),
    path('api/codes/', api_views.ApiProductCodeList.as_view()),
    path('data/', views.download_file, name='download_file'),
]