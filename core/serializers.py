from rest_framework import serializers
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