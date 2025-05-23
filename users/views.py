from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, UserSerializer
from .serializers import *
from .models import Log, Cidadao, FuncionarioJudicial
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import response,generics, status, permissions
from knox.models import AuthToken
from django.db.models import Q

# User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        print("Headers:", request.headers)
        print("Data:", request.data)       

        try:
            data = request.data
            user_name = data.get('user_name')
            password = data.get('password')

            user = authenticate(username=user_name, password=password)

            if not user:
                return self._invalid_credentials_response()
            
            return self._generate_login_response(user)

        except Exception as e:
            return self._server_error_response(e)
        
    def _generate_login_response(self, user):
            token = AuthToken.objects.create(user)[1]
            serializer = UserSerializer(user)
            
            return response.Response({
                'token': token,
                'user': serializer.data,
                'message': 'Login realizado com sucesso'
            }, status=status.HTTP_200_OK)

    def _invalid_credentials_response(self):
        return response.Response(
            {'message': 'Credenciais inválidas, tente novamente'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    def _server_error_response(self, error):
        """Resposta para erros internos do servidor"""
        return response.Response(
            {'message': 'Ocorreu um erro no servidor', 'error': str(error)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    
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
class CidadaoSearchAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CidadaoSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        search_type = self.request.query_params.get('type', 'bi')
        
        queryset = Cidadao.objects.all()
        
        if search_query:
            if search_type == 'bi':
                queryset = queryset.filter(
                    Q(numero_bi_nuit__icontains=search_query)
                )
            else:
                queryset = queryset.filter(
                    Q(utilizador__full_name__icontains=search_query)
                )
        
        return queryset.order_by('utilizador__full_name')
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'success': True,
                'count': queryset.count(),
                'results': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


    # def post(self, request):
    #     serializer = CidadaoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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