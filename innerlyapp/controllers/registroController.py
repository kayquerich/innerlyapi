from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from innerlyapp.models.Registros import Registro
from innerlyapp.models.Usuarios import Usuario
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRegistro(request):

    dados = json.loads(request.body)

    try:

        usuario = Usuario.objects.get(username=request.user)

        registro = Registro.objects.create(
            usuario=usuario,
            valueHumor=int(dados.get('value_humor')),
            dataRegistro=datetime.strptime(dados.get('data'), '%Y-%m-%d').date(),
            anotacao=dados.get('anotacao')
        )
        
        if registro:

            return JsonResponse({
                'message' : 'registro criado com sucesso',
                'registro' : registro.outputRegistroDto(),
                'criado' : True    
            }, status=201)
        else :

            return JsonResponse({
                'message' : 'Não foi possivel criar o registro',
                'criado' : False
            }, status=409)
    
    except Exception as e:
        print(str(e))
        return JsonResponse({
            'message' : 'erro ao criar o registro',
            'criado' : False    
        }, status=409)

@api_view(['GET'])
def getRegistros(request): # para fins de testes

    try:
        registros = list(Registro.objects.values())
        return JsonResponse(registros, safe=False)
    except Exception as e:
        return JsonResponse({'message' : 'erro na consulta'})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRegistro(request, id):

    usuario = request.user
    usuario = Usuario.objects.get(username=usuario)

    try:
        registro = Registro.objects.get(pk=id).outputRegistroDto()

        if registro and registro.get('idUsuario') == usuario.id:
            return JsonResponse(registro)
        else :
            return JsonResponse({'message' : 'você não tem permissão para realizar está ação'})
        
    except Exception as e:
        print(str(e))
        return JsonResponse({'message' : 'erro na consulta'})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRegistrosByUser(request, idUsuario):

    try:
        auth = Usuario.objects.get(id=idUsuario)
        auth = User.objects.get(username=auth.username)

        if (request.user == auth):

            usuario = Usuario.objects.get(id=idUsuario)
            registros = [registro.outputRegistroDto() for registro in Registro.objects.filter(usuario=usuario)]

            return JsonResponse(registros, safe=False)
        else :
            return JsonResponse({'message' : 'Você não tem permissão para realizar esta ação'})
    
    except Exception as e:

        return JsonResponse({'message' : 'falha na consulta', 'error' : str(e)})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateRegistro(request):

    dados = json.loads(request.body)
    requestUser = request.user

    try:

        usuario = Usuario.objects.get(username=requestUser.username)
        registro = Registro.objects.get(pk=dados.get('id'))

        if usuario and registro.usuario.id == usuario.id:

            registro.anotacao = dados.get('anotacao')
            registro.valueHumor = dados.get('value_humor')

            registro.save()

            return JsonResponse({'novo_registro' : registro.outputRegistroDto()}, status=200)

        else:
            return JsonResponse({'message' : 'você não tem permissão para executar esta ação'}, status=401)

    except Usuario.DoesNotExist as e:
        return JsonResponse({'message' : 'informe o id do usuario', 'erro' : str(e)}, status=401)