from django.db import models

class Atividade(models.Model):

    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=100)

    def __str__(self):
        return self.nome