from rest_framework.decorators import api_view, permission_classes
from innerlyapp.models.Usuarios import Usuario
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import json

@api_view(['GET'])
def getUsuarios(request): # para fins de testes

    try: 

        usuarios = list(Usuario.objects.values())
        return JsonResponse(usuarios, safe=False)
    
    except Exception as e:
        return JsonResponse({'message' : 'erro na consulta'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsuario(request, id):

    try:

        auth = User.objects.get(username=Usuario.objects.get(id=id).email)

        if (request.user == auth):
            usuario = Usuario.objects.get(id=id).usuarioDto()
            return JsonResponse(usuario)
        else:
            return JsonResponse({'message' : 'você não tem permissão para realizar esta ação'})
    
    except Usuario.DoesNotExist:
        return JsonResponse({'message' : 'usuario não existe'})
    except Exception as e:
        return JsonResponse({'message' : 'erro na consulta'})
    
@api_view(['POST'])
def createUsuario(request):

    try:

        dadosUsuario = json.loads(request.body)

        usuario = Usuario.objects.create(
            nome=dadosUsuario.get('nome'),
            email=dadosUsuario.get('email'),
            nascimento=dadosUsuario.get('nascimento'),
            senha=dadosUsuario.get('senha')
        )

        if usuario:
            return JsonResponse({
                'message' : 'usuario criado com sucesso',
                'id' : usuario.id,
                'criado' : True
            })
        else:
            return JsonResponse({
                'message' : 'não foi possivel criar o usuario',
                'criado' : False
            })
    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao criar usuario'
        })
    
@api_view(['POST'])
def loginUsuario(request):

    dados = json.loads(request.body)
    user = authenticate(username=dados.get('email'), password=dados.get('senha'))

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'message' : 'usuario logado com sucesso',
            'token' : token.key
        })
    else:
        return JsonResponse({'message' : 'credenciais inválidas'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUsuario(request):

    user = request.user

    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Exception as e:
        return JsonResponse({'message' : 'falha a realizar logout'})
    
    return JsonResponse({'message' : 'logout realizado com sucesso'})
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUsuario(request):

    dados = json.loads(request.body)
    usuario = Usuario.objects.get(id=dados.get('id'))
    auth = User.objects.get(username=usuario.email)

    if request.user == auth:
        try:

            if dados.get('contato'):

                usuario.contato = dados.get('contato')
                usuario.save()

                return JsonResponse({'message' : 'usuario alterado com sucesso'})
            else :
                return JsonResponse({'message' : 'impossivel alterar este campo'})  

        except Exception as e:
            return JsonResponse({'message' : 'erro na ateração do usuario'})
    else:
        return JsonResponse({'message' : 'você não tem permissão para realizar está ação'})