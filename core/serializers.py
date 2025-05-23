from rest_framework import serializers
from users.models import Cidadao
from .models import Pagamento, CertificadoRegisto, RegistoCriminal, SolicitarRegisto


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


class RegistoCriminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistoCriminal
        fields = '__all__'


class CidadaoDetailSerializer(serializers.ModelSerializer):
    registos_criminais = RegistoCriminalSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cidadao
        fields = ['numero_bi_nuit', 'utilizador', 'endereco', 'provincia', 
                 'distrito', 'data_nascimento', 'registos_criminais']