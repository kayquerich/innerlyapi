from django.db import models
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Profissionais import Profissional

class Autorizacao(models.Model):

    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False)
    idProfissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=False, blank=False)
    isAtiva = models.BooleanField(default=True)

    def __str__(self):
        return f'autorização {self.idUsuario.nome} - {self.idProfissional.nome}'