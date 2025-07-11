from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Solicitacoes import Solicitacao
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def solicitarAcompanhamento(request):

    usuario = Usuario.objects.get(username=request.user.username)
    dados = json.loads(request.body)

    try:

        profissional = Profissional.objects.get(codigo_acompanhamento=dados.get('codigo_acompanhamento'))

        if profissional and usuario:

            print(usuario)
            print(profissional)

            solicitacao = Solicitacao.objects.create(
                usuario=usuario,
                profissional=profissional,
                menssagem_solicitacao = dados.get('menssagem')
            )

            return JsonResponse({
                'solicitacao' : solicitacao.solicitacao_dto(),
                'criado' : True,
                'message' : f'Solicitação enviada para {profissional.nome}'
            }, status=200)
        
        else:

            return JsonResponse({
                'message' : 'não foi possivel solicitar o acompanhamento, tente novamente',
                'criado' : False
            }, status=401)

    except Exception as e:

        return JsonResponse({
            'message' : 'erro ao solicitar o acompanhamento, tente novamente',
            'criado' : False
        }, status=409)
