from rest_framework.decorators import api_view, permission_classes
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Usuarios import Usuario
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
            genero=dados.get('genero'),
            nascimento = dados.get('nascimento'),
            senha = dados.get('senha'),
            concelho = dados.get('concelho').upper(),
            regiao = dados.get('regiao'),
            numeroRegistro = dados.get('registro')
        )

        if profissional:
            return JsonResponse({
                'message' : 'conta criada com sucesso',
                'criado' : True
            }, status=201)
        else:
            return JsonResponse({
                'message' : 'não foi possivel criar sua conta',
                'criado' : False
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao criar sua conta',
            'criado' : False
        }, status=409)
    
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
            profissional.biografia = dados.get('biografia')
            profissional.genero = dados.get('genero')
            profissional.save()

            return JsonResponse({'message' : 'dados alterados com sucesso'}, status=200)
        else:
            return JsonResponse({'message' : 'não foi possivel realizar está ação'}, status=401)
    except Exception as e:
        return JsonResponse({'message' : 'erro na alteração'}, status=409)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listarProfissionais(request, parametro):

    usuario = Usuario.objects.filter(username=request.user.username).first()

    if not usuario: return JsonResponse({ 'message' : 'você não tem permissão para realizar a consulta' }, status=401)

    parametro_busca = str( parametro or '' ).upper()

    try:

        query_1 = [ profissional.dtoViewUser() for profissional in Profissional.objects.filter(codigo_acompanhamento=parametro_busca) ]

        query_2 = [ profissional.dtoViewUser() for profissional in Profissional.objects.filter(nome=parametro_busca) ]

        profissionais = query_1 + query_2

        return JsonResponse( profissionais, safe=False, status=200 )
    
    except Exception as e:
        return JsonResponse({'message' : 'erro na consulta'}, status=409)

@api_view(['GET'])
def listarNomes(request):

    try:
        lista_nome = [profissional.nome for profissional in Profissional.objects.all()]
        return JsonResponse(lista_nome, safe=False, status=200)
    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao realizar a consulta'
        }, status=409)
