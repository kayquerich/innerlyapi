from django.db import models
from innerlyapp.models.Objetivos import Objetivo

class Resultado(models.Model):

    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE, null=False, blank=False)
    descricao = models.TextField()
    data_criacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Resultado - {self.descricao}'