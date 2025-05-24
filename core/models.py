from django.db import models
from django.conf import settings
from users.models import Cidadao, FuncionarioJudicial 
from utils.models import LifeCycle
# Create your models here.


class SolicitarRegisto(LifeCycle):
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, related_name='solicitacoes')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    FINALIDADE_CHOICES = [
        ('EMPREGO', 'Emprego'),
        ('VIAGEM', 'Viagem'),
        ('OUTRO', 'Outro'),
    ]
    finalidade = models.CharField(max_length=50, choices=FINALIDADE_CHOICES)
    agencia = models.CharField(max_length=100)
    FORMA_PAGAMENTO_CHOICES = [
        ('MBWAY', 'MBWay'),
        ('TRANSFERENCIA', 'Transferência Bancária'),
        ('DINHEIRO', 'Dinheiro'),
    ]
    forma_pagamento = models.CharField(max_length=50, choices=FORMA_PAGAMENTO_CHOICES)
    pago = models.BooleanField(default=False)
    ESTADO_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
        ('CANCELADO', 'Cancelado'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='PENDENTE')

    def __str__(self):
        return f"Solicitação #{self.id} - {self.cidadao}"

class Pagamento(LifeCycle):
    solicitacao = models.OneToOneField(SolicitarRegisto, on_delete=models.CASCADE, related_name='pagamento')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=50)
    referencia = models.CharField(max_length=100, unique=True)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('FALHADO', 'Falhado'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='PENDENTE')

    def __str__(self):
        return f"Pagamento #{self.id} - {self.solicitacao}"

class CertificadoRegisto(LifeCycle):
    solicitacao = models.OneToOneField(SolicitarRegisto, on_delete=models.CASCADE, related_name='certificado')
    data_emissao = models.DateTimeField(auto_now_add=True)
    data_validade = models.DateField()
    numero_referencia = models.CharField(max_length=100, unique=True)
    conteudo = models.TextField()
    ESTADO_CERTIFICADO_CHOICES = [
        ('VALIDO', 'Válido'),
        ('EXPIRADO', 'Expirado'),
        ('REVOGADO', 'Revogado'),
    ]
    estado_certificado = models.CharField(max_length=50, choices=ESTADO_CERTIFICADO_CHOICES, default='VALIDO')
    funcionario_emissor = models.ForeignKey(FuncionarioJudicial, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Certificado #{self.numero_referencia}"

class RegistroCriminal(models.Model):
    STATUS_CHOICES = [
        ('Emitido', 'Emitido'),
        ('Pendente', 'Pendente'),
    ]
    RESULTADO_CHOICES = [
        ('Limpo', 'Limpo'),
        ('Com Registros', 'Com Registros'),
    ]
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE, related_name='registros')
    data = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Registo #{self.numero_processo} - {self.cidadao}"
    
