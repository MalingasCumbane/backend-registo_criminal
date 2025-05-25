from django.shortcuts import render
from core.models import Searches
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


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

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

    
class CidadaoSearchAPIView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CidadaoSerializer

    def get_queryset(self):

        search_query = self.request.query_params.get('q', '')
        search_type = self.request.query_params.get('type', 'bi')
        
        queryset = Cidadao.objects.all()
        
        if search_query:
            Searches.objects.create(identifier=search_query)
            if search_type == 'bi':
                print("")
                queryset = queryset.filter( Q(numero_bi_nuit__icontains=search_query) )
            else:
                queryset = queryset.filter( Q(full_name__icontains=search_query) )
        
        return queryset.order_by('full_name')
    
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


class CidadaoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, bi):
        return get_object_or_404(Cidadao, numero_bi_nuit=bi)

    def get(self, request, bi):

        cidadao = self.get_object(bi)
        serializer = CidadaoSerializer(cidadao)
        return Response(serializer.data)

    def put(self, request, bi):

        cidadao = self.get_object(bi)
        serializer = CidadaoSerializer(cidadao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bi):

        cidadao = self.get_object(bi)
        cidadao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


