from django.urls import path
from innerlyapp.controllers.registroController import *

urlpatterns = [
    path('create', createRegistro),
    path('', getRegistros),
    path('registro/<int:id>', getRegistro),
    path('usuario/<str:idUsuario>', getRegistrosByUser)
]