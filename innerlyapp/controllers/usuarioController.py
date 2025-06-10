from rest_framework.decorators import api_view
from innerlyapp.models.Usuarios import Usuario
from django.http import JsonResponse
import json

@api_view(['GET'])
def getUsuarios(request):

    try: 

        usuarios = list(Usuario.objects.values())
        return JsonResponse(usuarios, safe=False)
    
    except Exception as e:
        return JsonResponse({'message' : 'erro na consulta'})

@api_view(['GET'])
def getUsuario(request, id):

    try:

        usuario = Usuario.objects.get(id=id).usuarioDto()
        return JsonResponse(usuario)
    
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