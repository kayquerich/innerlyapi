from rest_framework.decorators import api_view, permission_classes
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Usuarios import Usuario
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import json

def accountVerify(modelClass, dados):
    try:

        verify = modelClass.objects.get(email=dados.get('email'))
        user = authenticate(username=verify.username, password=dados.get('senha'))

        if user is not None:

            token, _ = Token.objects.get_or_create(user=user)

            return token
        else:
            return
    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao fazer o login'
        })
    
def buildResponse(token, isProUser):

    if token:
        return {
            'message' : 'login realizado com sucesso',
            'token' : token.key,
            'isprouser' : isProUser
        }
    else :
        return {
            'message' : 'credênciais inválidas, não foi possivel fazer o login',
            'token' : None,
            'isprouser' : isProUser
        }


@api_view(['POST'])
def login(request):

    dados = json.loads(request.body)

    if Usuario.objects.filter(email=dados.get('email')).first():

        token = accountVerify(Usuario, dados=dados)

        return JsonResponse(buildResponse(token, False))

    elif Profissional.objects.filter(email=dados.get('email')).first():
        
        token = accountVerify(Profissional, dados=dados)

        return JsonResponse(buildResponse(token, True))
    
    else:
        return JsonResponse({
            'message' : 'credênciais inválidas, não foi possivel realizar o login'
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):

    user = request.user

    try:
        
        token = Token.objects.get(user=user)
        token.delete()

    except Exception as e:
        return JsonResponse({'message' : 'erro ao realizar o logout'})

    return JsonResponse({'message' : 'logout realizado com sucesso'})