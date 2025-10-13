from django.urls import path
from innerlyapp.controllers.registroController import *

urlpatterns = [
    path('create', createRegistro),
    path('', getRegistros),
    path('registro/<int:id>', getRegistro),
    path('usuario/<str:idUsuario>', getRegistrosByUser),
    path('update', updateRegistro),
    path('profissional/listar', getRegistrosByFollows),
    path('profissional/acompanhamento/<int:follow_id>', getRegistrosByFollow),
    path('atividades', getAtividades),
]