from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from innerlyapp.models.Registros import Registro
from innerlyapp.models.Usuarios import Usuario
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRegistro(request):

    dados = json.loads(request.body)

    try:

        usuario = Usuario.objects.get(email=request.user)

        registro = Registro.objects.create(
            idUsuario=usuario,
            valueHumor=int(dados.get('valuehumor')),
            dataRegistro=dados.get('data'),
            anotacao=dados.get('anotacao')
        )
        
        return JsonResponse({
            'message' : 'registro criado com sucesso',
            'resgistro' : registro.outputRegistroDto()    
        })
    
    except Exception as e:
        return JsonResponse({'message' : 'erro ao criar o registro'})

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
    usuario = Usuario.objects.get(email=usuario)

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
        auth = User.objects.get(username=auth.email)

        if (request.user == auth):

            usuario = Usuario.objects.get(id=idUsuario)
            registros = list(Registro.objects.filter(idUsuario=usuario).values())

            return JsonResponse(registros, safe=False)
        else :
            return JsonResponse({'message' : 'Você não tem permissão para realizar esta ação'})
    
    except Exception as e:

        JsonResponse({'message' : 'falha na consulta'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateRegistro(request):

    dados = json.loads(request.body)
    requestUser = request.user

    try:

        usuario = Usuario.objects.get(id=dados.get('idUsuario'))
        registro = Registro.objects.get(pk=dados.get('idRegistro'))

        if requestUser.username == usuario.email and registro.idUsuario == usuario:

            for key, value in dados.items():
                if key not in ['id', 'idUsuario', 'data']:
                    setattr(registro, key, value)

            registro.save()

            return JsonResponse({'novoregistro' : registro.outputRegistroDto()})

        else:
            return JsonResponse({'message' : 'você não tem permissão para executar esta ação'})

    except Usuario.DoesNotExist as e:
        return JsonResponse({'message' : 'informe o id do usuario', 'erro' : str(e)})