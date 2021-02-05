from django import forms
from impressao.repository import TipoImpressaoRepository
from impressao.models import Impressao


class ImpressaoForm(forms.Form):

    uri_arquivo = forms.FileField(label="Arquivo")
    qtd_copias = forms.IntegerField(label="cópias", initial=1, min_value=1)
    colorida = forms.BooleanField(label="colorida")
    comentario = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 10, 'cols': 40}), required=False)
    tipo = forms.Select()

    class Meta:
        model = Impressao
