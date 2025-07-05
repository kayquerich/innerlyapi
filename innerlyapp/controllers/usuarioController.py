from rest_framework.decorators import api_view, permission_classes
from innerlyapp.models.Usuarios import Usuario
from django.contrib.auth import authenticate
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
        return JsonResponse({'message' : 'erro na consulta', 'erro' : str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsuario(request):

    try:

        usuario = Usuario.objects.get(username=request.user.username).usuarioDto()

        if usuario:
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
            username=dadosUsuario.get('username'),
            email=dadosUsuario.get('email'),
            nascimento=dadosUsuario.get('nascimento'),
            senha=dadosUsuario.get('senha')
        )

        if usuario:
            return JsonResponse({
                'message' : 'usuario criado com sucesso',
                'criado' : True
            })
        else:
            return JsonResponse({
                'message' : 'não foi possivel criar o usuario',
                'criado' : False
            })
    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao criar usuario',
            'criado' : False,
        })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUsuario(request):

    dados = json.loads(request.body)
    usuario = Usuario.objects.get(username=request.user.username)

    if usuario:

        try:

            if dados:

                usuario.nome = dados.get('nome')
                usuario.contato = dados.get('contato')
                usuario.save()

                return JsonResponse({'message' : 'usuario alterado com sucesso'})
            else :
                return JsonResponse({'message' : 'campos inválidos para a alteração'})  

        except Exception as e:
            return JsonResponse({'message' : 'erro na ateração do usuario'})
    else:
        return JsonResponse({'message' : 'você não tem permissão para realizar está ação'})