from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import urls

urlpatterns = [
    path('xiidot1303/', admin.site.urls),
    path('', include('app.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)