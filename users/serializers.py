from rest_framework import serializers
from .models import User, Log, Cidadao, FuncionarioJudicial
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        # extra_kwargs = {'senha': {'write_only': True}}


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


class LoginSerializer(serializers.Serializer):
    print("LOGIN SERIALIZER")
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciais inválidas')
        else:
            raise serializers.ValidationError('Email e password são obrigatórios')

        data['user'] = user
        return data