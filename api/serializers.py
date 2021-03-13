from rest_framework import serializers
from impressao.models import Impressao, Turma, TipoImpressao

class TurmaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turma
        fields = ('id', 'nome')



class TipoImpressaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoImpressao
        fields = ('id', 'nome')

class ImpressaoSerializer(serializers.ModelSerializer):

    turma = TurmaSerializer(read_only=True)
    tipo = TipoImpressaoSerializer(read_only=True)
    arquivo = serializers.SerializerMethodField('get_file_name')
    cliente = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Impressao
        fields = ('id', 'arquivo', 'qtd_copias', 'tipo', 'set_imprimida_em', 'data_pedido', 'qtd_laudas_imprimidas', 
                    'prazo_entrega', 'colorida', "cliente", 'imprimida', 'turma'
        )
    
    def get_file_name(self, instance):
        return instance.uri_arquivo.name

    def get_user_name(self, instance):
        return instance.cliente.getFullName()