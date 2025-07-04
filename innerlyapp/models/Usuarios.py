from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
import uuid
import random

class Usuario(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=254, null=False, blank=False, unique=True)
    nome = models.CharField(max_length=254, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    contato = models.CharField(max_length=254, null=True, blank=True)
    nascimento = models.DateField()
    senha = models.CharField(max_length=254, null=False, blank=False)

    def save(self, *args, **kwargs):

        if self.nome:
            self.nome = self.nome.upper()

        if self.email:
            self.email = self.email.lower()

        if self.username:
            self.username = f'{self.username.lower()}#{random.randint(1000,9999)}'

        if self.senha:
            self.senha = make_password(self.senha)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    def usuarioDto(self):
        return {
            'id' : self.id,
            'nome' : self.nome,
            'username' : self.username,
            'email' : self.email,
            'contato' : self.contato,
            'nascimento' : self.nascimento
        }
    
@receiver(post_save, sender=Usuario)
def criarUsuarioAuth(sender, instance, created, **kwargs):
    if created:
        User.objects.create(username=instance.username, email=instance.email, password=instance.senha)