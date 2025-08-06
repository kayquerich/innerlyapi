from django.urls import path
from innerlyapp.controllers.acompanhamentoController import *

urlpatterns = [
    path('solicitacao/solicitar', solicitarAcompanhamento),
    path('solicitacao/responder', responderSolicitacao),
    path('solicitacao/listar', listaSolicitacoes),
    path('listar', listarAcompanhamentos),
    path('encerrar', encerrarAcompanhamento),
    path('solicitacao/<str:codigo>', getSolicitacaoByUser),
    path('codigo/<str:codigo>', getAcompanhamentoByCode),
    path('clientes', listarClientes)
]