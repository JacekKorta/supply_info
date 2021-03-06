"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.contrib.auth import views

admin.site.site_header = "Panel administracyjny - Stany magazynowe JANOME"
admin.site.site_title = "Panel administracyjny - Stany magazynowe JANOME"
admin.site.index_title = "Stany magazynowe JANOME"

urlpatterns = [
    path('', include('info_channel.urls')),
    path('', include('payments.urls')),
    path('', include('serial_numbers.urls')),
    path('', include('shipments.urls')),
    path('', include('supply_info.urls')),
    path('', include('warranty_parts.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout', views.LogoutView.as_view(next_page='/'), name='logout'),
]
