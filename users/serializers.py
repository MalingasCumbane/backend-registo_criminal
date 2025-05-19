from rest_framework import serializers
from .models import User, Log, Cidadao, FuncionarioJudicial


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nome_completo', 'email', 'telefone', 'tipo_utilizador', 'data_criacao']
        extra_kwargs = {'senha': {'write_only': True}}


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class CidadaoSerializer(serializers.ModelSerializer):
    utilizador = UserSerializer()
    
    class Meta:
        model = Cidadao
        fields = '__all__'


class FuncionarioJudicialSerializer(serializers.ModelSerializer):
    utilizador = UserSerializer()
    
    class Meta:
        model = FuncionarioJudicial
        fields = '__all__'