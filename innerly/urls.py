from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('innerlyapp.routes.usuarioUrls')),
    path('registros/', include('innerlyapp.routes.registroUrls'))
]
