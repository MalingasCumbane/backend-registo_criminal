from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Log, Cidadao, FuncionarioJudicial

# Configuração para o model Log
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'acao', 'utilizador', 'data_hora', 'ip')
    list_filter = ('acao', 'data_hora')
    search_fields = ('acao', 'detalhes', 'ip')
    date_hierarchy = 'data_hora'
    readonly_fields = ('data_hora',)

# Configuração para o model FuncionarioJudicial
class FuncionarioJudicialAdmin(admin.ModelAdmin):
    list_display = ('utilizador', 'cargo', 'departamento', 'nivel_acesso')
    search_fields = ('utilizador__nome_completo', 'cargo', 'departamento')
    list_filter = ('departamento', 'nivel_acesso')
    raw_id_fields = ('utilizador',)


admin.site.register(User)
admin.site.register(Log, LogAdmin)
admin.site.register(Cidadao)
admin.site.register(FuncionarioJudicial, FuncionarioJudicialAdmin)