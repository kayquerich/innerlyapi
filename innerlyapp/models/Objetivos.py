from django.db import models
from innerlyapp.models.Usuarios import Usuario

class Objetivo(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False)
    descricao = models.TextField()
    data_criacao = models.DateField(auto_now_add=True)
    prazo = models.DateField(null=True, blank=True)
    concluido = models.BooleanField(default=False)
    data_conclusao = models.DateField(null=True, blank=True)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    progresso = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Objetivo - {self.descricao} - {self.usuario.nome}'