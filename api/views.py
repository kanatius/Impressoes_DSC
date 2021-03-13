from django.http import JsonResponse, HttpResponse
from impressao.service import ImpressaoService, TipoImpressaoService, TurmaService
from usuario.service import UsuarioService
from django.core import serializers
from rest_framework import permissions
from .serializers import ImpressaoSerializer, TipoImpressaoSerializer, TurmaSerializer

from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import json

impressaoService = ImpressaoService()
tipoImpressaoService = TipoImpressaoService()
turmaService = TurmaService()
usuarioService = UsuarioService()

#----------------------------------------------------------#
#----------------------------------------------------------#
offset = openapi.Parameter('offset', openapi.IN_QUERY, default=0, description="", type=openapi.TYPE_INTEGER)
limit= openapi.Parameter('limit', openapi.IN_QUERY, default=0, description="Limite de impressões retornadas", type=openapi.TYPE_INTEGER)

@swagger_auto_schema(method='GET', manual_parameters=[offset, limit], responses={200 : ImpressaoSerializer})
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
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

    data = ImpressaoSerializer(impressoes_model, many=True).data
   
    data = json.dumps(data)
    
    return HttpResponse(data, content_type='application/json')

    # data = serializers.serialize("json", impressoes_model)

    # return HttpResponse(data, content_type='application/json')

#----------------------------------------------------------#
#----------------------------------------------------------#
uri_arquivo = openapi.Parameter('uri_arquivo', openapi.IN_FORM, description="Arquivo a ser imprimido", type=openapi.TYPE_FILE)
qtd_copias = openapi.Parameter('qtd_copias', openapi.IN_FORM, description="Quantidade de cópias", type=openapi.TYPE_INTEGER)
colorida = openapi.Parameter('colorida', openapi.IN_FORM, description="Se a impressão é colorida ou não", type=openapi.TYPE_BOOLEAN)
comentario = openapi.Parameter('comentario', openapi.IN_FORM, description="Mensagem/Observação", type=openapi.TYPE_STRING)
turma = openapi.Parameter('turma', openapi.IN_FORM, description="id da turma", type=openapi.TYPE_INTEGER)
tipo = openapi.Parameter('tipo', openapi.IN_FORM, description="id do tipo da impressão", type=openapi.TYPE_INTEGER)

@swagger_auto_schema(method='post', manual_parameters=[uri_arquivo, qtd_copias, colorida, comentario, turma, tipo])
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def solicitar_impressao(request):
    # print(request.data)
    data = {}

    if impressaoService.create(request):
        data = json.dumps("Impressão cadastrada com sucesso!")
    else:
        data = json.dumps("Erro na solicitação")

    return HttpResponse(data, content_type='application/json')
#----------------------------------------------------------#
#----------------------------------------------------------#
@swagger_auto_schema(method='PATCH', manual_parameters=[uri_arquivo, qtd_copias, colorida, comentario, turma, tipo])
@swagger_auto_schema(method='GET', responses={200 : ImpressaoSerializer})
@api_view(["GET", "DELETE", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([FormParser, MultiPartParser]) 
def impressao_by_id(request, id):
    '''
    Acesso à impressão pelo id
    '''
    if request.method == "GET":
        impressao = impressaoService.getById(request=request, id=id)

        if impressao is not None:
            data = ImpressaoSerializer(impressao, many=False).data
   
            data = json.dumps(data)
        else:
            data = json.dumps(None)

        return HttpResponse(data, content_type='application/json')

    if request.method == "DELETE":
        deleted = impressaoService.delete(request=request, id=id)

        if deleted:
            data = json.dumps("impressão removida com sucesso")
        else:
            data = json.dumps("erro na solicitação")
        
        return HttpResponse(data, content_type='application/json')
    
    if request.method == "PATCH":
        

        success = impressaoService.update(request, id)

        if success:
            data = json.dumps("impressão atualizada com sucesso!")
        else:
            data = json.dumps(None)
        return HttpResponse(data, content_type='application/json')
#----------------------------------------------------------#
#----------------------------------------------------------#
@swagger_auto_schema(method='GET', responses={ 200 : TipoImpressaoSerializer})
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def tipos_de_impressoes(request):

    tipos_model = tipoImpressaoService.getAllTipos(request)

    if not tipos_model:
        return JsonResponse({})
    
    data = TipoImpressaoSerializer(tipos_model, many=True).data
    
    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')
#----------------------------------------------------------#
#----------------------------------------------------------#
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def download_impressao(request, filename):
    return impressaoService.download(request, filename)
#----------------------------------------------------------#
#----------------------------------------------------------#
@swagger_auto_schema(method='GET', responses={ 200 : TurmaSerializer})
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_turmas(request):

    turmas = turmaService.getAllTurmas(request)

    if not turmas:
        return JsonResponse({"response" : None})

    data = TurmaSerializer(turmas, many=True).data
    
    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')
#----------------------------------------------------------#
#----------------------------------------------------------#
@swagger_auto_schema(method='GET', responses={ 200 : TurmaSerializer})
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def turma_by_id(request, id):

    turma = turmaService.getById(request=request, id=id)

    if not turma:
        return JsonResponse({"response" : None})
    
    data = TurmaSerializer(turma, many=False).data
    
    data = json.dumps(data)

    return HttpResponse(data, content_type='application/json')
#----------------------------------------------------------#
#----------------------------------------------------------#

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_name(request, id):
    
    user_name = usuarioService.getUserName(request, id)

    if user_name is not None:
        data = json.dumps(user_name)
    else:
        data = json.dumps(None)

    return HttpResponse(data, content_type='application/json')

