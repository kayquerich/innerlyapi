from django.urls import path
from innerlyapp.controllers.acompanhamentoController import *

urlpatterns = [
    path('solicitacao/solicitar', solicitarAcompanhamento),
    path('solicitacao/responder', responderSolicitacao),
    path('solicitacao/listar', listaSolicitacoes)
]