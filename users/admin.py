from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Log, Cidadao, FuncionarioJudicial

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nome_completo', 'telefone', 'tipo_utilizador', 'data_criacao', 'is_active')
    list_filter = ('tipo_utilizador', 'is_active', 'data_criacao')
    search_fields = ('email', 'nome_completo', 'telefone')
    ordering = ('-data_criacao',)
    filter_horizontal = ()
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informação Pessoal', {'fields': ('nome_completo', 'telefone')}),
        ('Permissões', {'fields': ('tipo_utilizador', 'is_active', 'is_staff', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'data_criacao')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_completo', 'telefone', 'tipo_utilizador', 'password1', 'password2'),
        }),
    )

# Configuração para o model Log
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'acao', 'utilizador', 'data_hora', 'ip')
    list_filter = ('acao', 'data_hora')
    search_fields = ('acao', 'detalhes', 'ip')
    date_hierarchy = 'data_hora'
    readonly_fields = ('data_hora',)

# Configuração para o model Cidadao
class CidadaoAdmin(admin.ModelAdmin):
    list_display = ('numero_bi_nuit', 'utilizador', 'provincia', 'distrito')
    search_fields = ('numero_bi_nuit', 'utilizador__nome_completo', 'endereco')
    list_filter = ('provincia', 'distrito')
    raw_id_fields = ('utilizador',)

# Configuração para o model FuncionarioJudicial
class FuncionarioJudicialAdmin(admin.ModelAdmin):
    list_display = ('utilizador', 'cargo', 'departamento', 'nivel_acesso')
    search_fields = ('utilizador__nome_completo', 'cargo', 'departamento')
    list_filter = ('departamento', 'nivel_acesso')
    raw_id_fields = ('utilizador',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Cidadao, CidadaoAdmin)
admin.site.register(FuncionarioJudicial, FuncionarioJudicialAdmin)
