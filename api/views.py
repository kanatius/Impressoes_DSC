from django.http import JsonResponse, HttpResponse
from impressao.service import ImpressaoService
from django.core import serializers
# from django.http import multipartparser

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import json

impressaoService = ImpressaoService()

offset = openapi.Parameter('offset', openapi.IN_QUERY, default=0, description="", type=openapi.TYPE_INTEGER)
limit= openapi.Parameter('limit', openapi.IN_QUERY, default=0, description="Limite de impressões retornadas", type=openapi.TYPE_INTEGER)

@swagger_auto_schema(method='get', manual_parameters=[offset, limit])
@api_view(['GET'])
def minhas_impressoes(request):
    '''
    Serviço para pegar impressões do usuário logado
    Caso o usuário seja um funcionário, retorna as impressões em aberto a serem imprimidas
    '''
    #default
    offset = 0
    limit = 0

    if request.GET.get('offset'):
        offset = int(request.GET['offset'])

    if request.GET.get("limit"):
        limit = int(request.GET.get("limit"))
    

    impressoes_model = impressaoService.getImpressoes(request=request, offset=offset, limit=limit)

    if not impressoes_model:
        return JsonResponse({"response" : None})

    
    impressoes_model = impressoes_model

    data = serializers.serialize("json", impressoes_model)

    return HttpResponse(data, content_type='application/json')


@swagger_auto_schema(method='get')
@api_view(["GET"])
def get_impressao_by_id(request, id):
    '''
    Solicita dados da impressão pelo id
    Só disponibiliza os dadis caso o usuário tenha permissão de acesso
    '''

    impressao = impressaoService.getById(request=request, id=id)

    if impressao is not None:
        data = serializers.serialize("json", [impressao])
    else:
        data = json.dumps(None)

    return HttpResponse(data, content_type='application/json')



uri_arquivo = openapi.Parameter('uri_arquivo', openapi.IN_FORM, required=True, description="Arquivo a ser imprimido", type=openapi.TYPE_FILE)
qtd_copias = openapi.Parameter('qtd_copias', openapi.IN_FORM, default=1, required=True, description="Quantidade de cópias a serem impressas", type=openapi.TYPE_INTEGER)
colorida = openapi.Parameter('colorida', openapi.IN_FORM, default=False,required=True, description="Se a impressão é colorida ou não", type=openapi.TYPE_BOOLEAN)
comentario = openapi.Parameter('comentario', openapi.IN_FORM, default="", description="Mensagem/Observação para o funcionário que irá imprimir", type=openapi.TYPE_STRING)
turma = openapi.Parameter('turma', openapi.IN_FORM, description="id da turma", type=openapi.TYPE_INTEGER)
tipo = openapi.Parameter('tipo', openapi.IN_FORM, required=True, description="id do tipo de impressão:\n1 - Prova\n2 - Trabalho\n3 - Atividade\n4 - Teste\n5 - outro", type=openapi.TYPE_INTEGER)

@swagger_auto_schema(method='post', manual_parameters=[uri_arquivo, qtd_copias, colorida, comentario, turma, tipo])
@api_view(["POST"])
@parser_classes([FormParser, MultiPartParser])
def solicitar_impressao(request):
    # print(request.data)
    data = {}

    if impressaoService.create(request):
        data = json.dumps("Impressão cadastrada com sucesso!")
    else:
        data = json.dumps("Erro na solicitação")

    return HttpResponse(data, content_type='application/json')



