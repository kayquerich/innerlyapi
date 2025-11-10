from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from innerlyapp.controllers.loginController import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('innerlyapp.routes.usuarioUrls')),
    path('registros/', include('innerlyapp.routes.registroUrls')),
    path('profissionais/', include('innerlyapp.routes.profissionalUrls')),
    path('acompanhamentos/', include('innerlyapp.routes.acompanhamentoUrls')),
    path('objetivos/', include('innerlyapp.routes.objetivosUrls')),
    path('login', login),
    path('logout', logout),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
