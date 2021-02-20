from django.urls import path
import api.views as api_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



app_name = "api"

urlpatterns = [
   path("impressao/<int:id>" , api_views.impressao_by_id, name = "impressao_by_id"),
   path("impressao/list", api_views.minhas_impressoes, name = "get_impressoes"), 
   path("impressao/solicitar", api_views.solicitar_impressao, name = "solicitar_impressao")
]


schema_view = get_schema_view(
   openapi.Info(
      title="API SGIIF",
      default_version='v1',
      description="Documentação do Sistema de Gerenciamento de Imrpessões do IFRN (SGIIF)",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="natanalmeidadelima@gamil.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]



