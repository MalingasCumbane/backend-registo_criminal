from rest_framework import serializers
from .models import Cidadao, Permission, User, UserPermissions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name','email', ]

class CidadaoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cidadao
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()  
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('password', 'token')
        read_only_fields = ['token']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['description']

class UserPermissionsSerializer(serializers.ModelSerializer):
    role = PermissionSerializer()
    class Meta:
        model = UserPermissions
        fields = ['role']
