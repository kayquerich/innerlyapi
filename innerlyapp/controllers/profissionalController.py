from rest_framework.decorators import api_view, permission_classes
from innerlyapp.models.Profissionais import Profissional
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import json

@api_view(['POST'])
def createProfissional(request):

    dados = json.loads(request.body)

    try:

        profissional = Profissional.objects.create(
            nome = dados.get('nome'),
            username = dados.get('username'),
            email = dados.get('email'),
            nascimento = dados.get('nascimento'),
            senha = dados.get('senha'),
            concelho = dados.get('concelho'),
            regiao = dados.get('regiao'),
            numeroRegistro = dados.get('registro')
        )

        if profissional:
            return JsonResponse({
                'message' : 'conta criada com sucesso',
                'criado' : True
            })
        else:
            return JsonResponse({
                'message' : 'não foi possivel criar sua conta',
                'criado' : False
            })
    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao criar sua conta',
            'criado' : False
        })
    
@api_view(['GET'])
def getProfissionais(request): # para fins de teste

    try:

        profissionais = list(Profissional.objects.values())
        return JsonResponse(profissionais, safe=False)
    except Exception as e:
        return JsonResponse({
            'message' : 'erro na consulta',
            'erro' : str(e)
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfissional(request):

    user = request.user

    try:

        profissional = Profissional.objects.get(username=user.username).profissionalDto()

        if profissional:
            return JsonResponse(profissional)
        else :
            return JsonResponse({'message' : 'você não tem permissão para realizar esta ação'})
    except Exception as e:
        return JsonResponse({'message' : 'erro na consulta'})
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def upadateProfissional(request):

    dados = json.loads(request.body)

    try:

        profissional = Profissional.objects.get(username=request.user.username)

        if profissional:

            profissional.nome = dados.get('nome')
            profissional.contato = dados.get('contato')
            profissional.save()

            return JsonResponse({'message' : 'dados alterados com sucesso'})
        else:
            return JsonResponse({'message' : 'não foi possivel realizar está ação'})
    except Exception as e:
        return JsonResponse({'message' : 'erro na alteração'})