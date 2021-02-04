from django.urls import path
from usuario import views as usuario_views
from usuario import func_views
from usuario import cliente_views
from .views import CreateUser

app_name = "usuario"

urlpatterns = [
    path("login", usuario_views.login, name="login"),
    path("logout", usuario_views.logout, name="logout"),
    path("cliente/home", cliente_views.home, name="home_cliente"),
    path("funcionario/home", func_views.home, name="home_funcionario"),
    path("cliente/soliticar_impressao", cliente_views.solicitar_impressao, name="solicitar_impressao")
]