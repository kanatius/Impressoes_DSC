from django.urls import path
from impressao import views as impressao_views

app_name = "impressao"

urlpatterns = [
    path("download/<str:filename>", impressao_views.downloadFile, name="download")
]