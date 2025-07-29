from django.db import models
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Profissionais import Profissional

class Solicitacao(models.Model):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    isAceita = models.BooleanField(default=False)
    dataSolicitacao = models.DateField(auto_now_add=True)
    menssagem_solicitacao = models.TextField(default='')
    estado = models.CharField(max_length=254, choices=[
        ('aguardando', 'em andamento'),
        ('recusada', 'solicitação recusada'),
        ('aceita', 'solicitação aceita')
    ], default='aguardando')

    def solicitacao_dto(self):

        user_data = {
            'nome' : self.usuario.nome,
            'biografia' : self.usuario.biografia,
            'nascimento' : self.usuario.nascimento,
            'contato' : self.usuario.contato,
            'genero' : self.usuario.genero
        }

        return {
            'id' : self.id,
            'dados_usuario' : user_data,
            'descricao' : f'Solicitação de acompanhamento {self.usuario.nome} - {self.profissional.nome}',
            'data' : self.dataSolicitacao,
            'menssagem' : self.menssagem_solicitacao,
            'estado' : self.estado
        }

    def __str__(self):
        return f'Solicitação de acompanhamento {self.usuario.nome} - {self.profissional.nome}'
    
    class Meta:
        verbose_name_plural = 'Solicitacoes'
    