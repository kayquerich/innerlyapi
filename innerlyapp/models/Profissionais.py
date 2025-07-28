from django.db import models
import uuid
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import random

def generate_code():
    return uuid.uuid4().hex[:6].upper()

class Profissional(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    concelho = models.CharField(max_length=3, choices=[
        ('CRM', 'Concelho Regional de Medicina'),
        ('CRP', 'Concelho Regional de Psicologia')
    ], blank=False, null=False)
    regiao = models.CharField(max_length=2, blank=False, null=False)
    numeroRegistro = models.CharField(max_length=10, blank=False, null=False, unique=True)
    nome = models.CharField(max_length=254, null=False, blank=False)
    username = models.CharField(max_length=254, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    contato = models.CharField(max_length=254, null=True, blank=True)
    nascimento = models.DateField()
    genero = models.CharField(max_length=254, null=False, blank=False, default='unknow')
    biografia = models.CharField(max_length=254, null=True, blank=True, default='Olá estou no innerly!')
    senha = models.CharField(max_length=254, null=False, blank=False)
    codigo_acompanhamento = models.CharField(max_length=6, unique=True, default=generate_code)

    def save(self, *args, **kwargs):

        if not self.senha:
            raise ValueError("Senha não pode ser vazia")

        if self.nome:
            self.nome = self.nome.upper()

        if self.email:
            self.email = self.email.lower()

        if self.regiao:
            self.regiao = self.regiao.upper()

        if self._state.adding and self.username:
            self.username = f'{self.username.lower()}#{random.randint(1000,9999)}' 

        if self.senha:
            self.senha = make_password(self.senha)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    def profissionalDto(self):
        return {
            'id' : self.id,
            'credencial' : f'{self.concelho}-{self.regiao} {self.numeroRegistro}',
            'nome' : self.nome,
            'username' : self.username,
            'email' : self.email,
            'contato' : self.contato,
            'nascimento' : self.nascimento,
            'genero' : self.genero,
            'biografia' : self.biografia,
            'codigo_acompanhamento' : self.codigo_acompanhamento
        }
    
    def dtoViewUser(self):
        return {
            'nome' : self.nome,
            'contato' : self.contato,
            'biografia' : self.biografia,
            'codigo_acompanhamento' : self.codigo_acompanhamento
        }
    
    class Meta:
        verbose_name_plural = 'Profissionais'
    
@receiver(post_save, sender=Profissional)
def criarUsuarioAuth(sender, instance, created, **kwargs):
    if created:
        User.objects.create(username=instance.username, email=instance.email, password=instance.senha)