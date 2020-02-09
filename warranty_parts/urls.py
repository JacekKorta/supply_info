from django.urls import path

from warranty_parts import views

app_name = 'warranty_parts'

urlpatterns = [
    path('nowe-zgloszenie/', views.add_issue, name='add_issue'),
    path('dodaj-komentarz/<int:issue_id>/', views.add_comment, name='add_comment'),
               ]