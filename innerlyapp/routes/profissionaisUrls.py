from django.urls import path
from innerlyapp.controllers.profissionalController import *

urlpatterns = [
    path('', getProfissionais),
    path('profissional', getProfissional),
    path('create', createProfissional),
    path('login', loginProfissional),
    path('logout', logoutProfissional),
    path('update', upadateProfissional)
]