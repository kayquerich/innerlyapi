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
    
@api_view(['POST'])
def loginProfissional(request):

    dados = json.loads(request.body)

    try:

        verify = Profissional.objects.get(email=dados.get('email'))
        user = authenticate(username=verify.username, password=dados.get('senha'))

        if user is not None:

            token, _ = Token.objects.get_or_create(user=user)

            return JsonResponse({
                'message' : 'login realizado com sucesso',
                'token' : token
            })
        else:
            JsonResponse({
                'message' : 'credênciais inválidas'
            })
    except Exception as e:
        return JsonResponse({'message' : 'erro ao fazer o login'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutProfissional(request):

    user = request.user

    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Exception as e:
        JsonResponse({'message' : 'erro ao realizar o logout'})
        
    JsonResponse({'message' : 'logout realizado com sucesso'})