from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Acompanhamentos import Acompanhamento
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from datetime import datetime
from innerlyapp.models.Objetivos import Objetivo
from innerlyapp.models.Resultados import Resultado

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createObjetivo(request):

    dados = json.loads(request.body)

    try:

        usuario = Usuario.objects.get(username=request.user)

        objetivo = Objetivo.objects.create(
            usuario=usuario,
            descricao=dados.get('descricao'),
            prazo=datetime.strptime(dados.get('prazo'), '%Y-%m-%d').date() if dados.get('prazo') else None,
            categoria=dados.get('categoria')
        )

        objetivo_data_transfer = {
            'descricao': objetivo.descricao,
            'prazo': objetivo.prazo,
            'categoria': objetivo.categoria,
        }

        if objetivo:

            return JsonResponse({
                'message' : 'objetivo criado com sucesso',
                'objetivo' : objetivo_data_transfer,
                'criado' : True    
            }, status=201)
        else :

            return JsonResponse({
                'message' : 'Não foi possivel criar o objetivo',
                'criado' : False
            }, status=409)
    except Exception as e:
        print(str(e))
        return JsonResponse({
            'message' : 'erro ao criar o objetivo',
            'criado' : False    
        }, status=409)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getObjetivosByUser(request):

    try:

        usuario = Usuario.objects.get(username=request.user)
        objetivos = Objetivo.objects.filter(usuario=usuario)

        objetivos_list = []
        for obj in objetivos:
            resultados = Resultado.objects.filter(objetivo=obj)
            resultados_list = [{'id': res.id, 'descricao': res.descricao, 'data_criacao': res.data_criacao} for res in resultados]
            objetivos_list.append({
                'id': obj.id,
                'descricao': obj.descricao,
                'data_criacao': obj.data_criacao,
                'prazo': obj.prazo,
                'concluido': obj.concluido,
                'data_conclusao': obj.data_conclusao,
                'categoria': obj.categoria,
                'progresso': obj.progresso,
                'resultados': resultados_list
            })

        return JsonResponse(objetivos_list, safe=False, status=200)

    except Exception as e:
        print(str(e))
        return JsonResponse({
            'message' : 'erro ao buscar os objetivos do usuário',
            'sucesso' : False    
        }, status=409)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateObjetivo(request):

    try:

        dados = json.loads(request.body)
        user = request.user
        user = Usuario.objects.get(username=user)

        objetivo = Objetivo.objects.get(id=dados.get('id'), usuario=user)
        
        if objetivo:

            objetivo.descricao = dados.get('descricao')
            objetivo.prazo = datetime.strptime(dados.get('prazo'), '%Y-%m-%d').date() if dados.get('prazo') else None
            objetivo.categoria = dados.get('categoria')
            objetivo.concluido = dados.get('concluido')
            if dados.get('concluido'):
                objetivo.data_conclusao = datetime.strptime(dados.get('data_conclusao'), '%Y-%m-%d').date() if dados.get('data_conclusao') else None
            objetivo.progresso = dados.get('progresso', objetivo.progresso)
            objetivo.save()

            return JsonResponse({
                'message' : 'objetivo atualizado com sucesso',
                'sucesso' : True    
            }, status=200)
        else :

            return JsonResponse({
                'message' : 'Não foi possivel atualizar o objetivo',
                'sucesso' : False
            }, status=409)

    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao atualizar o objetivo',
            'sucesso' : False    
        }, status=409)

    pass