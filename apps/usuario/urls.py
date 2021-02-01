from django.urls import path
from apps.usuario import views as usuario_views

urlpatterns = [
    path("login", usuario_views.login, name="login")
]