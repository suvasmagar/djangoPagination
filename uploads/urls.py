from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.authtoken import views

from uploads.core import views


urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'simple/', views.simple_upload, name='simple_upload'),
    path(r'form/', views.model_form_upload, name='model_form_upload'),
    path(r'admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
