from django.http import JsonResponse, HttpResponse
from impressao.service import ImpressaoService
from django.core import serializers
from rest_framework.decorators import api_view

impressaoService = ImpressaoService()

@api_view(['GET'])
def minhas_impressoes(request):

    """
    Get impressões do usuário logado
    ---
    parameters_strategy:
        form: replace
        query: merge

    parameters:
        - name: offset
          description: JSON object containing two strings: password and username.
          required: true
          paramType: body
    
    consumes:
        - application/json
        - application/xml
    produces:
        - application/json
        - application/xml
    """

    #default
    offset = 0
    limit = 0

    if request.GET.get("offset"):
        offset = int(request.GET.get("offset"))

    if request.GET.get("limit"):
        offset = int(request.GET.get("limit"))
    
    impressoes_model = impressaoService.getImpressoes(request=request, offset=offset, limit=limit)

    if impressoes_model:
        impressoes_model = impressoes_model.values()
    else:
        return JsonResponse({"response" : None})

    impressoes_list = list(impressoes_model)

    print(impressoes_list)

    return JsonResponse({"response" : impressoes_list})


@api_view
def get_impressao_by_id(request, id):

    impressao = impressaoService.getById(request=request, id=id)

    return JsonResponse({"response" : impressao})

