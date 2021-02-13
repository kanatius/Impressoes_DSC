from django.db import models
from usuario.models import Usuario
from datetime import datetime

# Create your models here.
class TipoImpressao(models.Model):
    nome = models.CharField("nome", max_length=55)
    descricao = models.CharField("descricao", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome


class Impressao(models.Model):

    comentario = models.CharField('comentario', max_length=255, blank=True, null=True)
    arquivo = models.FileField(name='uri_arquivo', max_length=400)
    qtd_copias = models.SmallIntegerField("qtd_copias")
    visualizado_em = models.DateTimeField("visualizado_em", blank=True, null=True)
    set_imprimida_em = models.DateTimeField("set_imprimida_em", blank=True, null=True)
    data_pedido = models.DateTimeField("data_pedido", auto_now_add=True)
    qtd_laudas_imprimidas = models.IntegerField("qtd_laudas_imprimidas", blank=True, null=True)
    prazo_entrega = models.DateTimeField("prazo_entrega", blank=True, null=True)
    colorida = models.BooleanField("colorida", default=False)
    cliente = models.ForeignKey(Usuario, name="cliente", on_delete=models.CASCADE, null=True)
    imprimida = models.BooleanField("is_imprimida", blank=True, default=False)
    tipo = models.ForeignKey(TipoImpressao, on_delete=models.SET_NULL, null=True, name="tipo")
        
