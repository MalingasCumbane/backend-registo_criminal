from rest_framework import serializers
from users.models import Cidadao
from .models import Pagamento, CertificadoRegisto, RegistroCriminal, SolicitarRegisto


class SolicitarRegistoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitarRegisto
        fields = '__all__'


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'


class CertificadoRegistoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoRegisto
        fields = '__all__'


class RegistroCriminalSerializer(serializers.ModelSerializer):
    cidadao_nome = serializers.CharField(source='cidadao.nome', read_only=True)
    cidadao_numero_id = serializers.CharField(source='cidadao.numero_id', read_only=True)

    class Meta:
        model = RegistroCriminal
        fields = '__all__'


class CidadaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidadao
        fields = '__all__'


class CidadaoDetailSerializer(serializers.ModelSerializer):
    registros_criminais = RegistroCriminalSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cidadao
        fields = ['numero_bi_nuit', 'utilizador', 'endereco', 'provincia', 
                 'distrito', 'data_nascimento', 'registros_criminais']