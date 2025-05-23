from django.urls import path, include
from users.views import CidadaoSearchAPIView, LoginView
from users.views import UserListCreateView, UserDetailView, LogListCreateView, LogDetailView, CidadaoDetailView, FuncionarioJudicialListCreateView, FuncionarioJudicialDetailView
from core.views import CriminalRecordListView, GerarCertificadoView, RecordStatsView, SolicitarRegistoCreateView, SolicitarRegistoListCreateView, SolicitarRegistoDetailView, PagamentoListCreateView, PagamentoDetailView, CertificadoRegistoListCreateView, CertificadoRegistoDetailView, RegistoCriminalListCreateView, RegistoCriminalDetailView


app_name = "api"
urlpatterns = [
    # Autenticação
    path('login/', LoginView.as_view(), name='login'),
    
    # Users
    # path('users/', UserListCreateView.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Logs
    # path('logs/', LogListCreateView.as_view(), name='log-list'),
    # path('logs/<int:pk>/', LogDetailView.as_view(), name='log-detail'),
    
    # Cidadãos
    # path('cidadaos/', CidadaoListCreateView.as_view(), name='cidadao-list'),
    path('cidadaos/search/', CidadaoSearchAPIView.as_view(), name='cidadao-search'),
    # path('cidadaos/<int:pk>/', CidadaoDetailView.as_view(), name='cidadao-detail'),
    
    # Funcionários Judiciais
    # path('funcionarios/', FuncionarioJudicialListCreateView.as_view(), name='funcionario-list'),
    # path('funcionarios/<int:pk>/', FuncionarioJudicialDetailView.as_view(), name='funcionario-detail'),
    
    # Solicitações de Registro
    path('solicitacoes/', SolicitarRegistoListCreateView.as_view(), name='solicitacao-list'),
    path('solicitacoes/<int:pk>/', SolicitarRegistoDetailView.as_view(), name='solicitacao-detail'),
    
    # # Pagamentos
    # path('pagamentos/', PagamentoListCreateView.as_view(), name='pagamento-list'),
    # path('pagamentos/<int:pk>/', PagamentoDetailView.as_view(), name='pagamento-detail'),
    
    # Certificados
    path('certificados/', CertificadoRegistoListCreateView.as_view(), name='certificado-list'),
    path('certificados/<int:pk>/', CertificadoRegistoDetailView.as_view(), name='certificado-detail'),
    
    # Registros Criminais
    path('registros-criminais/', RegistoCriminalListCreateView.as_view(), name='registo-criminal-list'),
    path('registros-criminais/<int:pk>/', RegistoCriminalDetailView.as_view(), name='registo-criminal-detail'),
    
    # Autenticação da API
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('cidadaos/<str:bi>/', CidadaoDetailView.as_view(), name='cidadao-detail'),
    path('solicitacoes/<str:bi>/', SolicitarRegistoCreateView.as_view(), name='solicitar-registo'),
    path('certificados/<int:pk>/gerar/', GerarCertificadoView.as_view(), name='gerar-certificado'),

    path('records/', CriminalRecordListView.as_view(), name='records-list'), #listar todos os registos criminais
    path('records/stats/', RecordStatsView.as_view(), name='records-stats'), #listar estatísticas de registos criminais
]
