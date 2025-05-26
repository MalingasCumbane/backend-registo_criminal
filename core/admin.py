from django.contrib import admin
from .models import RegistoCriminal, Searches, SolicitarRegisto, Pagamento, CertificadoRegisto


admin.site.site_header = "Sistema de Registo Criminal"
admin.site.site_title = "Administração do Sistema"
admin.site.index_title = "Bem-vindo ao Sistema de Registo Criminal"

admin.site.register(SolicitarRegisto)
admin.site.register(Pagamento)
admin.site.register(RegistoCriminal)
admin.site.register(Searches)

@admin.register(CertificadoRegisto)
class CertificadoRegistoAdmin(admin.ModelAdmin):
    list_display = ['id', "data_emissao", "data_validade", "numero_referencia"]
