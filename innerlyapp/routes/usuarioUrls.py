from django.urls import path
from innerlyapp.controllers.usuarioController import *

urlpatterns = [
    path('', getUsuarios),
    path('usuario/<str:id>', getUsuario),
    path('create', createUsuario),
    path('update', updateUsuario),
    path('login', loginUsuario),
    path('logout', logoutUsuario)
]