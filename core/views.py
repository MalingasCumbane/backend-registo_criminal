from http.client import HTTPResponse
import os
from django.shortcuts import render
from core.serializers import CertificadoRegistoSerializer, CidadaoDetailSerializer, PagamentoSerializer, SolicitarRegistoSerializer
from core.serializers import CertificadoRegistoSerializer, CidadaoDetailSerializer, PagamentoSerializer, RegistoCriminalSerializer, SolicitarRegistoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
import datetime
from users.models import Cidadao
from .models import RegistoCriminal, SolicitarRegisto, Pagamento, CertificadoRegisto, RegistoCriminal
from django.contrib.auth.models import User
from django.db.models import Count
from .models import SolicitarRegisto, Pagamento, CertificadoRegisto
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, action
viewsets.ModelViewSet
from django.views import View
from django.http import FileResponse
from django.http import Http404




class SolicitarRegistoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(SolicitarRegisto, pk=pk)

    def get(self, request, pk):
        solicitacao = self.get_object(pk)
        serializer = SolicitarRegistoSerializer(solicitacao)
        return Response(serializer.data)

    def put(self, request, pk):
        solicitacao = self.get_object(pk)
        serializer = SolicitarRegistoSerializer(solicitacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        solicitacao = self.get_object(pk)
        solicitacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SolicitarRegistoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        solicitacoes = SolicitarRegisto.objects.all()
        serializer = SolicitarRegistoSerializer(solicitacoes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SolicitarRegistoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CidadaoDetailView(generics.RetrieveAPIView):
    queryset = Cidadao.objects.all()
    serializer_class = CidadaoDetailSerializer
    lookup_field = 'numero_bi_nuit'
    permission_classes = [IsAuthenticated]

class SolicitarRegistoCreateView(generics.CreateAPIView):
    queryset = SolicitarRegisto.objects.all()
    serializer_class = SolicitarRegistoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            cidadao=get_object_or_404(Cidadao, numero_bi_nuit=self.kwargs['bi']),
            funcionario=self.request.user.funcionario
        )

    serializer_class = CertificadoRegistoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        solicitacao = get_object_or_404(SolicitarRegisto, pk=kwargs['pk'])
        
        if hasattr(solicitacao, 'certificado'):
            return Response(
                {'error': 'Já existe um certificado para esta solicitação'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registos = solicitacao.cidadao.registos_criminais.all()
        tem_registos = registos.exists()
        
        conteudo = {
            "cidadao": {
                "nome": solicitacao.cidadao.full_name,
                "bi": solicitacao.cidadao.numero_bi_nuit,
                "nascimento": solicitacao.cidadao.data_nascimento,
                "endereco": solicitacao.cidadao.endereco
            },
            "tem_registos": tem_registos,
            "registos": [
                {
                    "processo": r.numero_processo,
                    "data": r.data_ocorrencia,
                    "tipo": r.get_tipo_ocorrencia_display(),
                    "sentenca": r.setenca
                } for r in registos
            ],
            "validade": (datetime.date.today() + datetime.timedelta(days=90)).strftime('%Y-%m-%d')
        }

        certificado = CertificadoRegisto.objects.create(
            solicitacao=solicitacao,
            data_validade=datetime.date.today() + datetime.timedelta(days=90),
            numero_referencia=f"CR-{solicitacao.id}-{datetime.datetime.now().strftime('%Y%m%d')}",
            conteudo=conteudo,
            funcionario_emissor=request.user.funcionario
        )

        solicitacao.estado = 'APROVADO'
        solicitacao.save()

        serializer = self.get_serializer(certificado)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GerarCertificadoView(generics.CreateAPIView):
    serializer_class = CertificadoRegistoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        solicitacao = get_object_or_404(SolicitarRegisto, pk=kwargs['pk'])
        
        # Verificar se já existe certificado
        if hasattr(solicitacao, 'certificado'):
            # Se existir, retornar os detalhes do certificado existente
            certificado_existente = solicitacao.certificado
            serializer = self.get_serializer(certificado_existente)
            
            # Adicionar mensagem informativa na resposta
            response_data = serializer.data
            response_data['message'] = 'Certificado já existente - retornando dados do certificado anterior'
            
            return Response(
                response_data,
                status=status.HTTP_200_OK
            )
        
        # Se não existir, criar novo certificado
        registos = solicitacao.cidadao.registos_criminais.all()
        tem_registos = registos.exists()
        
        conteudo = {
            "cidadao": {
                "nome": solicitacao.cidadao.full_name,
                "bi": solicitacao.cidadao.numero_bi_nuit,
                "nascimento": solicitacao.cidadao.data_nascimento,
                "endereco": solicitacao.cidadao.endereco,
                "nacionalidade": solicitacao.cidadao.nacionalidade
            },
            "tem_registos": tem_registos,
            "registos": [
                {
                    "processo": r.numero_processo,
                    "data": r.data_ocorrencia.strftime('%Y-%m-%d') if r.data_ocorrencia else None,
                    "tribunal": r.tribunal,
                    "tipo": r.get_tipo_ocorrencia_display(),
                    "sentenca": r.setenca
                } for r in registos
            ],
            "validade": (datetime.date.today() + datetime.timedelta(days=90)).strftime('%Y-%m-%d'),
            "data_emissao": datetime.date.today().strftime('%Y-%m-%d')
        }

        # Gerar número de referência único
        numero_referencia = self.gerar_numero_referencia(solicitacao)

        certificado = CertificadoRegisto.objects.create(
            solicitacao=solicitacao,
            data_validade=datetime.date.today() + datetime.timedelta(days=90),
            numero_referencia=numero_referencia,
            conteudo=conteudo,
            funcionario_emissor=request.user.funcionario
        )

        # Atualizar estado da solicitação
        solicitacao.estado = 'APROVADO'
        solicitacao.save()

        # Registrar ação no histórico
        # self.registrar_historico(solicitacao, request.user)

        serializer = self.get_serializer(certificado)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def gerar_numero_referencia(self, solicitacao):
        """Gera um número de referência único para o certificado"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return f"CR-{solicitacao.id}-{timestamp}"


class CriminalRecordListView(generics.ListAPIView):
    serializer_class = RegistoCriminalSerializer
    
    def get_queryset(self):
        queryset = RegistoCriminal.objects.all()
        
        # Search functionality
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(record_id__icontains=search_term) |
                Q(citizen__icontains=search_term) |
                Q(citizen_id__icontains=search_term)
            )
            
        return queryset.order_by('-id')

class RecordStatsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        
        stats = {
            'total_records': RegistoCriminal.objects.count(),
            'unique_citizens': RegistoCriminal.objects.values('cidadao_id').distinct().count(),
            # 'with_records': RegistoCriminal.objects.filter(has_criminal_record=True).count(),
            'today_records': RegistoCriminal.objects.filter(created_at=today).count(),
        }
        
        return Response(stats)



@api_view(['GET'])
def get_cidadao_registos(request, id):
    try:
        # Get the citizen
        cidadao = Cidadao.objects.get(numero_bi_nuit=id)
        
        # Get all criminal records for this citizen
        registos = RegistoCriminal.objects.filter(cidadao=cidadao)
        
        # Serialize the data
        serializer = RegistoCriminalSerializer(registos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Cidadao.DoesNotExist:
        return Response(
            {"error": "Cidadão não encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class CertificadoViewSet(viewsets.ModelViewSet):
    queryset = CertificadoRegisto.objects.all()
    serializer_class = CertificadoRegistoSerializer

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        certificado = self.get_object()
        file_path = certificado.arquivo_pdf.path  # Ajuste para seu campo de arquivo
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as pdf:
                response = HTTPResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        return Response({"detail": "Arquivo não encontrado"}, status=404)
    

class CertificadoDetailView(generics.RetrieveAPIView):
    queryset = CertificadoRegisto.objects.all()
    serializer_class = CertificadoRegistoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

