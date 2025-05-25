from django.urls import path, include
from users.views import CidadaoSearchAPIView, LoginView
from users.views import CidadaoDetailView
from core.views import CertificadoDetailView, CriminalRecordListView, DashboardStatsAPIView, GerarCertificadoView, RecordDetailsByReference, RecordStatsView, SolicitarRegistoListCreateView, SolicitarRegistoDetailView, get_cidadao_registos


app_name = "api"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    
    path('pesquisar/cidadaos/<str:bi>/', CidadaoDetailView.as_view(), name='cidadao-detail'), # get ID details
    path('cidadaos/<str:id>/registos/', get_cidadao_registos, name='cidadao-registos'), # Buscar registos criminais do Cidadao atraves do ID dele

    path('cidadaos/search/', CidadaoSearchAPIView.as_view(), name='cidadao-search'), #Pesquisar por um Cidadao

    path('records/', CriminalRecordListView.as_view(), name='records-list'), #listar todos os registos criminais
    path('records/stats/', RecordStatsView.as_view(), name='records-stats'), #listar estatísticas de registos criminais
    path('records/certificate/<int:num_ref>/', RecordDetailsByReference.as_view(), name='numero_referencia'), #listar estatísticas de registos criminais

    path('<int:id>/solicitacoes/', SolicitarRegistoListCreateView.as_view(), name='solicitacao-list'), #Criar solicitação re registo criminal
    path('solicitacoes/<int:pk>/', SolicitarRegistoDetailView.as_view(), name='solicitacao-detail'), #Pegar solicitação por ID

    path('certificados/<int:pk>/gerar/', GerarCertificadoView.as_view(), name='gerar-certificado'), #Gerar documento PDF
    path('certificados/actualizar/<int:id>/', CertificadoDetailView.as_view(), name='certificado-detail'),

    path('dashboard-stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
]