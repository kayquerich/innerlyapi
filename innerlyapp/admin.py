from django.contrib import admin
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Registros import Registro
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Autorizacoes import Autorizacao
from innerlyapp.models.Solicitacoes import Solicitacao

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Registro)
admin.site.register(Profissional)
admin.site.register(Autorizacao)
admin.site.register(Solicitacao)