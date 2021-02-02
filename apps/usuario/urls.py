from django.urls import path
from apps.usuario import views as usuario_views

app_name = "usuario"

urlpatterns = [
    path("login", usuario_views.login, name="login"),
    path("logout", usuario_views.logout, name="logout")
]