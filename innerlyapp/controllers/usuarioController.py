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
            return JsonResponse(usuario, status=200)
        else:
            return JsonResponse({'message' : 'você não tem permissão para realizar esta ação'}, status=401)
    
    except Usuario.DoesNotExist:
        return JsonResponse({'message' : 'usuario não existe'}, status=404)
    except Exception as e:
        return JsonResponse({'message' : 'erro na consulta'}, status=400)
    
@api_view(['POST'])
def createUsuario(request):

    try:

        dadosUsuario = json.loads(request.body)

        usuario = Usuario.objects.create(
            nome=dadosUsuario.get('nome'),
            username=dadosUsuario.get('username'),
            email=dadosUsuario.get('email'),
            nascimento=dadosUsuario.get('nascimento'),
            genero=dadosUsuario.get('genero'),
            senha=dadosUsuario.get('senha')
        )

        if usuario:
            return JsonResponse({
                'message' : 'usuario criado com sucesso',
                'criado' : True
            }, status=201)
        else:
            return JsonResponse({
                'message' : 'não foi possivel criar o usuario',
                'criado' : False
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao criar usuario',
            'criado' : False,
        }, status=409)

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
                usuario.genero = dados.get('genero')
                usuario.biografia = dados.get('biografia')
                
                usuario.save()

                return JsonResponse({'message' : 'usuario alterado com sucesso'}, status=200)
            else :
                return JsonResponse({'message' : 'campos inválidos para a alteração'}, status=409)  

        except Exception as e:
            return JsonResponse({'message' : 'erro na ateração do usuario'}, status=404)
    else:
        return JsonResponse({'message' : 'você não tem permissão para realizar está ação'}, status=401)