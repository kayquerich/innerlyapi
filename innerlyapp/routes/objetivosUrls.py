from django.urls import path
from innerlyapp.controllers.objetivoController import *

urlpatterns = [
    path('criar', createObjetivo),
    path('listar', getObjetivosByUser),
    path('atualizar', updateObjetivo),
    path('resultados/adicionar', cadastrar_resultados)
]