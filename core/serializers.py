from core.models import CertificadoRegisto, Pagamento, RegistoCriminal, SolicitarRegisto
from rest_framework import serializers
from users.models import Cidadao


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


class CidadaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidadao
        fields = '__all__'

class RegistoCriminalSerializer(serializers.ModelSerializer):
    cidadao = CidadaoSerializer(read_only=True) 
    
    class Meta:
        model = RegistoCriminal
        fields = '__all__'

class RegistoCriminalSerializer(serializers.ModelSerializer):
    cidadao = CidadaoSerializer(read_only=True)  # Adiciona os dados do cidadão
    
    class Meta:
        model = RegistoCriminal
        fields = '__all__'


class CidadaoDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cidadao
        fields = '__all__'
        
