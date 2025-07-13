from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Solicitacoes import Solicitacao
from innerlyapp.models.Acompanhamentos import Acompanhamento
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def solicitarAcompanhamento(request):

    usuario = Usuario.objects.get(username=request.user.username)
    dados = json.loads(request.body)

    try:

        profissional = Profissional.objects.get(codigo_acompanhamento=dados.get('codigo_acompanhamento'))

        if profissional and usuario:

            print(usuario)
            print(profissional)

            solicitacao = Solicitacao.objects.create(
                usuario=usuario,
                profissional=profissional,
                menssagem_solicitacao = dados.get('menssagem')
            )

            return JsonResponse({
                'solicitacao' : solicitacao.solicitacao_dto(),
                'criado' : True,
                'message' : f'Solicitação enviada para {profissional.nome}'
            }, status=200)
        
        else:

            return JsonResponse({
                'message' : 'não foi possivel solicitar o acompanhamento, tente novamente',
                'criado' : False
            }, status=401)

    except Exception as e:

        return JsonResponse({
            'message' : 'erro ao solicitar o acompanhamento, tente novamente',
            'criado' : False
        }, status=409)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def responderSolicitacao(request):

    profissional = Profissional.objects.get(username=request.user.username)
    dados = json.loads(request.body)

    try:

        if profissional:

            resposta = dados.get('resposta')
            solicitacao = Solicitacao.objects.get(id=dados.get('id'))

            if resposta == 'aceita':

                solicitacao.isAceita = True
                solicitacao.estado = 'aceita'
                solicitacao.save()

                acompanhamento = Acompanhamento.objects.create(
                    usuario=solicitacao.usuario,
                    profissional=solicitacao.profissional,
                    isAtivo=True
                )

                return JsonResponse({
                    'message' : f'Solcitação aceita, você esta acompanhando {acompanhamento.usuario.nome} deste o dia {acompanhamento.dataCriacao}',
                    'respondida' : True,
                    'estado' : solicitacao.isAceita
                }, status=200)

            else:

                solicitacao.isAceita = False
                solicitacao.estado = 'recusada'
                solicitacao.save()

                return JsonResponse({
                    'message' : f'Solcitação recusada, você pode comunicar a {solicitacao.usuario.nome} o motivo de ter recusado',
                    'respondida' : True,
                    'estado' : solicitacao.isAceita
                }, status=200)

        else:
            return JsonResponse({
                'message' : 'você não tem permissão para responder essa solicitação',
                'respondida' : False
            }, status=401)

    except Exception as e:
        return JsonResponse({
            'message' : 'erro ao responder solicitação',
            'respondida' : False
         }, status=409)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listaSolicitacoes(request):

    profissional = Profissional.objects.get(username=request.user.username)

    if profissional:

        lista_solicitacoes = list(Solicitacao.objects.filter(profissional=profissional).values())

        return JsonResponse(lista_solicitacoes, safe=False, status=200)

    else:

        return JsonResponse({
            'message' : 'Você não tem permissão para realizar esta ação'
        }, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listarAcompanhamentos(request):

    usuario = Usuario.objects.get(username=request.user.username)
    
    if usuario:
        try:

            acompanhamentos = [acompanhamento.acompanhamento_dto() for acompanhamento in Acompanhamento.objects.filter(usuario=usuario)]

            return JsonResponse(acompanhamentos, safe=False, status=200)

        except Exception as e:

            return JsonResponse({
                'message' : 'erro na consulta'
            }, status=404)

    else:

        return JsonResponse({
            'message' : 'você não tem permissão para realizar está ação'
        }, status=401)
