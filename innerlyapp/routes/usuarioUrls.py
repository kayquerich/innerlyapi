from django.urls import path
from innerlyapp.controllers.usuarioController import *

urlpatterns = [
    path('', getUsuarios),
    path('usuario', getUsuario),
    path('create', createUsuario),
    path('update', updateUsuario)
]