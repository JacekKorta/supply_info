from django.urls import path

from warranty_parts import views

app_name = 'warranty_parts'

urlpatterns = [
    path('nowe_zgloszenie/', views.add_issue, name='add_issue')
               ]