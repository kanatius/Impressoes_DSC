from django.urls import path
from usuario import views as usuario_views
from usuario import func_views
from usuario import cliente_views
from .views import CreateUser
from impressao.repository import ImpressaoRepository
from impressao.views import ImpressaoCreate, ImpressaoDelete, ImpressaoList, ImpressaoUpdate

app_name = "usuario"

urlpatterns = [
    path("login", usuario_views.login, name="login"),
    path("logout", usuario_views.logout, name="logout"),
    path("funcionario/home", func_views.home, name="home_funcionario"),
    path("cliente/soliticar_impressao", cliente_views.solicitar_impressao, name="solicitar_impressao"),
    # path('cliente/impressao/create', ImpressaoCreate.as_view(), name='solicitar_impressao'),
    path('cliente/impressao/list', cliente_views.home, name='minhas_impressoes'),
    path('cliente/impressao/edit/<int:pk>/', ImpressaoUpdate.as_view(), name='edit_impressao'),
    path('cliente/impressao/delete/<int:pk>/', ImpressaoDelete.as_view(), name='excluirImpressao')
]