from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, UserSerializer
from .serializers import *
from .models import User, Log, Cidadao, FuncionarioJudicial
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = UserSerializer(user).data
            
            return Response({
                'token': token.key,
                'user': user_data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if 'password' in request.data:
                user.set_password(request.data['password'])
                user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            if 'password' in request.data:
                user.set_password(request.data['password'])
                user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Log Views
class LogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Log, pk=pk)

    def get(self, request, pk):
        log = self.get_object(pk)
        serializer = LogSerializer(log)
        return Response(serializer.data)

    def delete(self, request, pk):
        log = self.get_object(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Cidadao Views
class CidadaoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cidadaos = Cidadao.objects.all()
        serializer = CidadaoSerializer(cidadaos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CidadaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CidadaoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Cidadao, pk=pk)

    def get(self, request, pk):
        cidadao = self.get_object(pk)
        serializer = CidadaoSerializer(cidadao)
        return Response(serializer.data)

    def put(self, request, pk):
        cidadao = self.get_object(pk)
        serializer = CidadaoSerializer(cidadao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cidadao = self.get_object(pk)
        cidadao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# FuncionarioJudicial Views
class FuncionarioJudicialListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        funcionarios = FuncionarioJudicial.objects.all()
        serializer = FuncionarioJudicialSerializer(funcionarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FuncionarioJudicialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FuncionarioJudicialDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(FuncionarioJudicial, pk=pk)

    def get(self, request, pk):
        funcionario = self.get_object(pk)
        serializer = FuncionarioJudicialSerializer(funcionario)
        return Response(serializer.data)

    def put(self, request, pk):
        funcionario = self.get_object(pk)
        serializer = FuncionarioJudicialSerializer(funcionario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        funcionario = self.get_object(pk)
        funcionario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)