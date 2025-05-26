from django.http import Http404
from django.http import FileResponse
from django.views import View
from http.client import HTTPResponse
import os
from django.shortcuts import render
from core.serializers import CertificadoRegistoSerializer, CidadaoDetailSerializer, SolicitarRegistoSerializer
from core.serializers import CertificadoRegistoSerializer, CidadaoDetailSerializer, RegistoCriminalSerializer, SolicitarRegistoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
import datetime
from users.models import Cidadao
from .models import RegistoCriminal, Searches, SolicitarRegisto, Pagamento, CertificadoRegisto, RegistoCriminal
from django.contrib.auth.models import User
from django.db.models import Count
from .models import SolicitarRegisto, Pagamento, CertificadoRegisto
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, action
viewsets.ModelViewSet


class SolicitarRegistoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    print("this one then")

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

    def get(self, request, id):
        solicitacoes = SolicitarRegisto.objects.filter(cidadao__id=id)
        serializer = SolicitarRegistoSerializer(solicitacoes, many=True)
        return Response(serializer.data)

    def post(self, request, id):
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
            'with_records': RegistoCriminal.objects.filter(
                tipo_ocorrencia__in=['CRIME', 'CONTRAVENCAO', 'INFRACCAO']
            ).count(),            'today_records': RegistoCriminal.objects.filter(created_at=today).count(),
        }

        return Response(stats)


@api_view(['GET'])
def get_cidadao_registos(request, id):
    try:
        cidadao = Cidadao.objects.get(numero_bi_nuit=id)
        registos = RegistoCriminal.objects.filter(cidadao=cidadao)
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


class CertificadoDetailView(generics.RetrieveAPIView):
    queryset = CertificadoRegisto.objects.all()
    serializer_class = CertificadoRegistoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class DashboardStatsAPIView(APIView):
    def get(self, request):
        try:
            total_searches = Searches.objects.count()

            total_cidadaos_processados = Cidadao.objects.annotate(
                num_registos=Count('registos_criminais')
            ).filter(num_registos__gt=0).count()

            total_registos_emitidos = RegistoCriminal.objects.count()

            total_registos_limpos = Cidadao.objects.annotate(
                num_registos=Count('registos_criminais')
            ).filter(num_registos=0).count()

            data = {
                'registos_emitidos': total_registos_emitidos,
                'pesquisas_realizadas': total_searches,
                'cidadaos_processados': total_cidadaos_processados,
                'registos_limpos': total_registos_limpos
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecordDetailsByReference(APIView):
    def post(self, request):
        try:
            # Certifique-se de usar .get() para retornar um único objeto
            certif = CertificadoRegisto.objects.get(numero_referencia=request.data['num_ref'])
            serializer = CertificadoRegistoSerializer(certif)  # Agora serializando um objeto único
            return Response(serializer.data)
        except CertificadoRegisto.DoesNotExist:
            return Response({"detail": "Certificado não encontrado"}, status=status.HTTP_404_NOT_FOUND)

class TodasSolicitacoes(APIView):
    def get(self, request, *args, **kwargs):
        list_some = SolicitarRegisto.objects.all()
        serializer = SolicitarRegistoSerializer(list_some, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateNewCriminalRecords(APIView):
    def post(self, request, *args, **kwargs):

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        pessoa = Cidadao.objects.get(id=request.data['cidadao'])

        if SolicitarRegisto.objects.filter(id=request.data['id']).exists():
            SolicitarRegisto.objects.filter(id=request.data['id']).update(
                estado = "APROVADO"
            )

        RegistoCriminal.objects.create(
            cidadao = pessoa,
            cumprido = request.data['cidadao'],
            data_ocorrencia = request.data['data_ocorrencia'],
            data_setenca = request.data['data_setenca'],
            numero_processo = timestamp,
            observacao = request.data['observacao'],
            setenca = request.data['setenca'],
            tipo_ocorrencia = request.data['tipo_ocorrencia'],
            tribunal = request.data['tribunal'],
        )

        return Response(status=status.HTTP_200_OK)
    
