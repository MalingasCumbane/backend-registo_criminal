from rest_framework import serializers
from .models import Log, Cidadao, FuncionarioJudicial, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', ]


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class CidadaoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cidadao
        fields = '__all__'


class FuncionarioJudicialSerializer(serializers.ModelSerializer):
    utilizador = UserSerializer()
    
    class Meta:
        model = FuncionarioJudicial
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()  
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('password', 'token')
        read_only_fields = ['token']