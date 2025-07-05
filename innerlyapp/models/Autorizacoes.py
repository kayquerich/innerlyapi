from django.db import models
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Profissionais import Profissional

class Autorizacao(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=False, blank=False)
    isAtiva = models.BooleanField(default=True)
    dataCriacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'autorização {self.usuario.nome} - {self.profissional.nome}'
    
    class Meta:
        verbose_name_plural = 'Autorizacoes'