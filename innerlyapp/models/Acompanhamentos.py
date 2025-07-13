from django.db import models
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Profissionais import Profissional

class Acompanhamento(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=False, blank=False)
    isAtivo = models.BooleanField(default=True)
    dataCriacao = models.DateField(auto_now_add=True)
    data_finalizacao = models.DateField(blank=True, null=True)

    def acompanhamento_dto(self):

        return {
            'data_inicio' : self.dataCriacao,
            'is_ativo' : self.isAtivo,
            'nome_profissional' : self.profissional.nome,
            'biografia' : self.profissional.biografia,
            'codigo_acompanhamento' : self.profissional.codigo_acompanhamento,
        }

    def __str__(self):
        return f'autorização {self.usuario.nome} - {self.profissional.nome}'
    
    class Meta:
        verbose_name_plural = 'Acompanhamentos'