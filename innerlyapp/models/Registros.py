from django.db import models
from innerlyapp.models.Usuarios import Usuario
from django.forms.models import model_to_dict

class Registro(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False)
    valueHumor = models.SmallIntegerField()
    dataRegistro = models.DateField()
    anotacao = models.TextField()

    def outputRegistroDto(self):

        return {
            'id' : self.id,
            'usuario' : self.usuario.usuarioDto(),
            'title' : f'Detalhes - {self.dataRegistro.strftime("%d/%m/%Y")}',
            'br_date' : self.dataRegistro.strftime("%d/%m/%Y"),
            'value_humor' : self.valueHumor,
            'data_registro' : self.dataRegistro,
            'anotacao' : self.anotacao
        }

    def __str__(self):

        return f'resgistro - {self.dataRegistro} - {self.usuario.nome}'