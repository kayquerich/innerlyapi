from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('innerlyapp.routes.usuarioUrls')),
    path('registros/', include('innerlyapp.routes.registroUrls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
