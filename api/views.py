from django.http import JsonResponse, HttpResponse
from impressao.service import ImpressaoService
from django.core import serializers

from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

impressaoService = ImpressaoService()

offset = openapi.Parameter('offset', openapi.IN_QUERY, default=0, description="", type=openapi.TYPE_INTEGER)
limit= openapi.Parameter('limit', openapi.IN_QUERY, default=0, description="", type=openapi.TYPE_INTEGER)

@swagger_auto_schema(method='get', manual_parameters=[offset, limit])
@api_view(['GET'])
def minhas_impressoes(request):

    #default
    offset = 0
    limit = 0

    if request.GET.get('offset'):
        offset = int(request.GET['offset'])

    if request.GET.get("limit"):
        limit = int(request.GET.get("limit"))
    
    print(offset, limit)

    impressoes_model = impressaoService.getImpressoes(request=request, offset=offset, limit=limit)

    if not impressoes_model:
        return JsonResponse({"response" : None})

    
    impressoes_model = impressoes_model

    data = serializers.serialize("json", impressoes_model)

    return HttpResponse(data, content_type='application/json')


@api_view
def get_impressao_by_id(request, id):

    impressao = impressaoService.getById(request=request, id=id)

    return JsonResponse({"response" : impressao})

