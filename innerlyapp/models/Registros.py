from django.db import models
from innerlyapp.models.Usuarios import Usuario

class Registro(models.Model):

    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False)
    valueHumor = models.SmallIntegerField()
    dataRegistro = models.DateField()
    anotacao = models.TextField()

    def outputRegistroDto(self):

        strhumorlist = ['muito-mal', 'mal', 'mais-ou-menos', 'bem', 'muito-bem']

        return {
            'id' : self.pk,
            'idUsuario' : self.idUsuario.id,
            'nomeusuario' : self.idUsuario.nome,
            'strhumor' : strhumorlist[self.valueHumor -1],
            'data' : self.dataRegistro,
            'anotacao' : self.anotacao
        }

    def __str__(self):

        return f'resgistro - {self.dataRegistro} - {self.idUsuario.nome}'