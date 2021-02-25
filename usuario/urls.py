from django.urls import path
from django.conf.urls import url
from usuario import views as usuario_views
from usuario import func_views
from usuario import cliente_views
from .views import CreateUser
from impressao.repository import ImpressaoRepository
from impressao.views import ImpressaoCreate, ImpressaoDelete, ImpressaoList, ImpressaoUpdate
from wkhtmltopdf.views import PDFTemplateView

app_name = "usuario"

urlpatterns = [
    path("login", usuario_views.login, name="login"),
    path("logout", usuario_views.logout, name="logout"),
    path("funcionario/home", func_views.home, name="home_funcionario"),
    path("funcionario/relatorio/page", func_views.relatorio_page, name="relatorio_page"),
    path("funcionario/relatorio/gerar", PDFTemplateView.as_view(template_name='relatorio.html', filename='relarotio.pdf'), name="gerar_relatorio"),
    path("cliente/soliticar_impressao", cliente_views.solicitar_impressao, name="solicitar_impressao"),
    path('cliente/impressao/list', cliente_views.home, name='minhas_impressoes'),
    path('cliente/impressao/edit/<int:id_impressao>/', cliente_views.update_impressao, name='edit_impressao'),
    path('cliente/impressao/delete', cliente_views.delete_impressao, name='delete_impressao')
]