from django.contrib import admin
from .models import TipoImpressao, Impressao, Turma
# Register your models here.

admin.site.register(Impressao)
admin.site.register(TipoImpressao)
admin.site.register(Turma)