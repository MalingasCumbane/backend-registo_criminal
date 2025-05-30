from django.contrib import admin
from .models import RegistoCriminal, Searches, SolicitarRegisto, Pagamento, CertificadoRegisto

admin.site.site_header = "Sistema de Registo Criminal"
admin.site.site_title = "Administração do Sistema"
admin.site.index_title = "Bem-vindo ao Sistema de Registo Criminal"

@admin.register(SolicitarRegisto)
class SolicitarRegistoAdmin(admin.ModelAdmin):
    list_display = ['id', "data_solicitacao", "finalidade", "estado"]

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['id', "solicitacao", "valor", "metodo"]

@admin.register(CertificadoRegisto)
class CertificadoRegistoAdmin(admin.ModelAdmin):
    list_display = ['id', "data_emissao", "data_validade", "numero_referencia"]

@admin.register(RegistoCriminal)
class CertificadoRegistoAdmin(admin.ModelAdmin):
    list_display = ['id', "numero_processo", "tipo_ocorrencia", "observacao"]

@admin.register(Searches)
class SearchesAdmin(admin.ModelAdmin):
    list_display = ['id', "identifier"]
