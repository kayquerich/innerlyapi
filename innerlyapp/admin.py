from django.contrib import admin
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Registros import Registro
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Autorizacoes import Autorizacao

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Registro)
admin.site.register(Profissional)
admin.site.register(Autorizacao)