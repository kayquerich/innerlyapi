from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from innerlyapp.models.Profissionais import Profissional
from innerlyapp.models.Usuarios import Usuario
from innerlyapp.models.Solicitacoes import Solicitacao
from innerlyapp.models.Acompanhamentos import Acompanhamento
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from datetime import date

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def solicitarAcompanhamento(request):

    usuario = Usuario.objects.get(username=request.user.username)
    dados = json.loads(request.body)

    try:

        profissional = Profissional.objects.get(codigo_acompanhamento=dados.get('codigo_acompanhamento'))

        if profissional and usuario:

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

                acompanhamento = {}

                acompanhamento = Acompanhamento.objects.filter(
                    usuario=solicitacao.usuario, 
                    profissional=solicitacao.profissional
                ).first()

                if acompanhamento:
                    acompanhamento.isAtivo = True
                    acompanhamento.save()
                else :
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
def getSolicitacaoByUser(request, codigo):

    usuario = Usuario.objects.filter(username=request.user.username).first()

    if usuario:

        try:

            profissional = Profissional.objects.filter(codigo_acompanhamento=codigo).first()
            solicitacao = Solicitacao.objects.filter(usuario=usuario, profissional=profissional).first()

            if solicitacao: return JsonResponse(solicitacao.solicitacao_dto(), status=200)
            return JsonResponse({}, status=200)

        except Exception as e:
            print(str(e))
            return JsonResponse({'message' : 'informações inválidas'}, status=409)

    else:
        return JsonResponse({ 'message' : 'você não tem permissão para realizar está ação' }, status=401)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAcompanhamentoByCode(request, codigo):

    usuario = Usuario.objects.filter(username=request.user.username).first()

    if usuario:

        try:

            profissional = Profissional.objects.filter(codigo_acompanhamento=codigo).first()
            acompanhamento = Acompanhamento.objects.filter(usuario=usuario, profissional=profissional).first()

            if acompanhamento:
                return JsonResponse(acompanhamento.acompanhamento_dto(), status=200)
            else: 
                return JsonResponse({})

        except Exception as e:
            print(str(e))
            return JsonResponse({'message' : 'erro na consulta dos dados'}, status=409)
    
    return JsonResponse({'message' : 'ainda não fiz'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listarAcompanhamentos(request): # falta o lado do profissional que ainda não fiz

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
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def encerrarAcompanhamento(request):

    dados = json.loads(request.body)

    usuario = Usuario.objects.filter(username=request.user.username).first()
    if usuario:
        
        if dados.get('id'):

            id = dados.get('id')
            follow = Acompanhamento.objects.filter(id=id).first()

            try:

                follow.isAtivo = False
                follow.data_finalizacao = date.today()
                follow.save()

            except Exception as e:
                return JsonResponse({
                    'message' : 'erro ao encerrar o acompanhamento'
                }, status=409)
            
            return JsonResponse({
                'message' : 'acompanhamento encerrado'
            }, status=200)

        else: 
            return JsonResponse({
                'message' : 'id do acompanhamento não informado'
            }, status=401)

    return JsonResponse({
        'message' : 'ainda não fiz'
    }, status=404)
