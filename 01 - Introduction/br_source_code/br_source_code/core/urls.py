"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    DashboardView, 
    AboutView, 
    change_theme, 
    chart_data, 
    login_view, 
    otp_view, 
    logout_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('otp/', otp_view, name='otp'),
    path('about/', AboutView.as_view(), name='about'),
    path('chart-data/', chart_data, name='data'),
    path('switch/', change_theme, name='change'),
    path('books/', include('books.urls', namespace='books')),
    path('rentals/', include('rentals.urls', namespace='rentals')),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Book Rental Administration'
admin.site.index_title = 'Manage the Book Rental System'
