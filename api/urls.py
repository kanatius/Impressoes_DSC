from django.urls import path
import api.views as api_views

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Documentação')

app_name = "api"

urlpatterns = [
    path("impressoes", api_views.minhas_impressoes, name = "get_impressoes"),
    path("impressao/getImpressao/<int:id>" , api_views.get_impressao_by_id, name = "get_impressao_by_id")
]

urlpatterns += [
    path("docs", schema_view)
]




