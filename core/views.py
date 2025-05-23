from django.shortcuts import render
from core.serializers import CertificadoRegistoSerializer, CidadaoDetailSerializer, CriminalRecordSerializer, PagamentoSerializer, RegistoCriminalSerializer, SolicitarRegistoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
import datetime
from users.models import Cidadao
from .models import SolicitarRegisto, Pagamento, CertificadoRegisto, RegistoCriminal
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q

# Create your views here.

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


# Pagamento Views
class PagamentoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagamentos = Pagamento.objects.all()
        serializer = PagamentoSerializer(pagamentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PagamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PagamentoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Pagamento, pk=pk)

    def get(self, request, pk):
        pagamento = self.get_object(pk)
        serializer = PagamentoSerializer(pagamento)
        return Response(serializer.data)

    def put(self, request, pk):
        pagamento = self.get_object(pk)
        serializer = PagamentoSerializer(pagamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pagamento = self.get_object(pk)
        pagamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CertificadoRegisto Views
class CertificadoRegistoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        certificados = CertificadoRegisto.objects.all()
        serializer = CertificadoRegistoSerializer(certificados, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CertificadoRegistoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificadoRegistoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(CertificadoRegisto, pk=pk)

    def get(self, request, pk):
        certificado = self.get_object(pk)
        serializer = CertificadoRegistoSerializer(certificado)
        return Response(serializer.data)

    def put(self, request, pk):
        certificado = self.get_object(pk)
        serializer = CertificadoRegistoSerializer(certificado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        certificado = self.get_object(pk)
        certificado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# RegistoCriminal Views
class RegistoCriminalListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registos = RegistoCriminal.objects.all()
        serializer = RegistoCriminalSerializer(registos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegistoCriminalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistoCriminalDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(RegistoCriminal, pk=pk)

    def get(self, request, pk):
        registo = self.get_object(pk)
        serializer = RegistoCriminalSerializer(registo)
        return Response(serializer.data)

    def put(self, request, pk):
        registo = self.get_object(pk)
        serializer = RegistoCriminalSerializer(registo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        registo = self.get_object(pk)
        registo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ===============================================================
# ===============================================================
# ===============================================================
# ===============================================================
# ===============================================================
# ===============================================================
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

class GerarCertificadoView(generics.CreateAPIView):
    serializer_class = CertificadoRegistoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        solicitacao = get_object_or_404(SolicitarRegisto, pk=kwargs['pk'])
        
        # Verificar se já existe certificado
        if hasattr(solicitacao, 'certificado'):
            return Response(
                {'error': 'Já existe um certificado para esta solicitação'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Gerar conteúdo do certificado
        registos = solicitacao.cidadao.registos_criminais.all()
        tem_registros = registos.exists()
        
        conteudo = {
            "cidadao": {
                "nome": solicitacao.cidadao.utilizador.full_name,
                "bi": solicitacao.cidadao.numero_bi_nuit,
                "nascimento": solicitacao.cidadao.data_nascimento,
                "endereco": solicitacao.cidadao.endereco
            },
            "tem_registros": tem_registros,
            "registros": [
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

        # Atualizar estado da solicitação
        solicitacao.estado = 'APROVADO'
        solicitacao.save()

        serializer = self.get_serializer(certificado)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class CriminalRecordListView(generics.ListAPIView):
    serializer_class = CriminalRecordSerializer
    
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
