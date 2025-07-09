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
        }, status=409)
    
def buildResponse(token, isProUser):

    if token:
        return JsonResponse({
            'message' : 'login realizado com sucesso',
            'token' : token.key,
            'isprouser' : isProUser
        }, status=200)
    else :
        return JsonResponse({
            'message' : 'credênciais inválidas, não foi possivel fazer o login',
            'token' : None,
            'isprouser' : isProUser
        }, status=401)


@api_view(['POST'])
def login(request):

    dados = json.loads(request.body)

    if Usuario.objects.filter(email=dados.get('email')).first():

        token = accountVerify(Usuario, dados=dados)

        return buildResponse(token, False)

    elif Profissional.objects.filter(email=dados.get('email')).first():
        
        token = accountVerify(Profissional, dados=dados)

        return buildResponse(token, True)
    
    else:
        return JsonResponse({
            'message' : 'credênciais inválidas, não foi possivel realizar o login',
            'token' : None, 
            'isprouser' : False
        }, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):

    user = request.user

    try:
        
        token = Token.objects.get(user=user)
        token.delete()

    except Exception as e:
        return JsonResponse({'message' : 'erro ao realizar o logout'}, status=401)

    return JsonResponse({'message' : 'logout realizado com sucesso'}, status=200)