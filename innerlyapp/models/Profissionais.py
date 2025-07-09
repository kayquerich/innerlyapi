from django.db import models
import uuid
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import random

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
    senha = models.CharField(max_length=254, null=False, blank=False)

    def save(self, *args, **kwargs):

        if not self.senha:
            raise ValueError("Senha não pode ser vazia")

        if self.nome:
            self.nome = self.nome.upper()

        if self.email:
            self.email = self.email.lower()

        if self.regiao:
            self.regiao = self.regiao.upper()

        if self.username:
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
            'nascimento' : self.nascimento
        }
    
    class Meta:
        verbose_name_plural = 'Profissionais'
    
@receiver(post_save, sender=Profissional)
def criarUsuarioAuth(sender, instance, created, **kwargs):
    if created:
        User.objects.create(username=instance.username, email=instance.email, password=instance.senha)