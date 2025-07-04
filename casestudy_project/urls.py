"""
URL configuration for casestudy_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.views.static import serve
from casestudies.models import CaseStudy
from casestudies.views import custom_404



from django.contrib.auth.models import User

from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin


class OTPAdmin(OTPAdminSite):

      def has_permission(self, request):
        return request.user.is_active and request.user.is_authenticated and request.user.otp_device


# Create instance of custom admin site
admin_site = OTPAdmin(name='OTPAdmin')

# Copy all models already registered in default admin to your OTP admin
for model, model_admin in admin.site._registry.items():
    admin_site.register(model, model_admin.__class__)



secret_admin_path = os.environ.get('SECRET_ADMIN_PATH')

urlpatterns = [
    path(f"{secret_admin_path}/", admin_site.urls),
    path('admin/', custom_404, name='admin_404'),
    path('', include('casestudies.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

sitemaps = {
    'cases': GenericSitemap({'queryset': CaseStudy.objects.all(), 'date_field': 'created_at'}, priority=0.8),
}

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', serve, {'path': 'robots.txt', 'document_root': settings.BASE_DIR}),
]

# Custom 404 handler
handler404 = 'casestudies.views.custom_404'