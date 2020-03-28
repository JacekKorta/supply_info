from django.urls import path
from info_channel import views


app_name = 'info_channel'

urlpatterns = [
    # post views
    path('', views.PostListView.as_view(), name='post_list'),
    path('informacje/<category>/', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    ]