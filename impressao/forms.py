from django import forms
from impressao.repository import TipoImpressaoRepository
from impressao.models import Impressao


class ImpressaoForm(forms.ModelForm):

    uri_arquivo = forms.FileField(label="Arquivo")
    qtd_copias = forms.IntegerField(label="Cópias", initial=1, min_value=1)
    colorida = forms.BooleanField(label="Colorida", required=False)
    comentario = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 10, 'cols': 40}), required=False)

    class Meta:
        model = Impressao
        fields = ['uri_arquivo', 'qtd_copias', 'colorida', 'comentario', 'tipo', 'turma']