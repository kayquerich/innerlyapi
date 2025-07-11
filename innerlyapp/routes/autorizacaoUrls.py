from django.urls import path
from innerlyapp.controllers.AutorizacaoController import *

urlpatterns = [
    path('solicitacao/solicitar', solicitarAcompanhamento)
]