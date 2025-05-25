from django.contrib import admin
from .models import RegistoCriminal, Searches, SolicitarRegisto, Pagamento, CertificadoRegisto

# Register your models here.

class SolicitarRegistoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cidadao', 'data_solicitacao', 'finalidade', 'estado', 'pago')
    list_filter = ('estado', 'pago', 'finalidade', 'data_solicitacao')
    search_fields = ('cidadao__utilizador__nome_completo', 'cidadao__numero_bi_nuit')
    date_hierarchy = 'data_solicitacao'
    raw_id_fields = ('cidadao',)

# Configuração para o model Pagamento
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitacao', 'valor', 'metodo', 'estado', 'data_pagamento')
    list_filter = ('estado', 'metodo', 'data_pagamento')
    search_fields = ('solicitacao__id', 'referencia')
    date_hierarchy = 'data_pagamento'
    raw_id_fields = ('solicitacao',)

# Configuração para o model CertificadoRegisto
class CertificadoRegistoAdmin(admin.ModelAdmin):
    list_display = ('numero_referencia', 'solicitacao', 'data_emissao', 'data_validade', 'estado_certificado')
    list_filter = ('estado_certificado', 'data_emissao', 'data_validade')
    search_fields = ('numero_referencia', 'solicitacao__cidadao__utilizador__nome_completo')
    date_hierarchy = 'data_emissao'
    raw_id_fields = ('solicitacao', 'funcionario_emissor')

admin.site.register(SolicitarRegisto, SolicitarRegistoAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(CertificadoRegisto, CertificadoRegistoAdmin)
admin.site.register(RegistoCriminal)
admin.site.register(Searches)


admin.site.site_header = "Sistema de Registo Criminal"
admin.site.site_title = "Administração do Sistema"
admin.site.index_title = "Bem-vindo ao Sistema de Registo Criminal"
