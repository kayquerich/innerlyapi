from django.urls import path
from innerlyapp.controllers.profissionalController import *

urlpatterns = [
    path('', getProfissionais),
    path('profissional', getProfissional),
    path('create', createProfissional),
    path('update', upadateProfissional),
    path('listar/<str:parametro>', listarProfissionais),
    path('nomes', listarNomes)
]