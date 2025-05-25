from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Log, Cidadao, FuncionarioJudicial

admin.site.register(User)
admin.site.register(Log)
admin.site.register(FuncionarioJudicial)

@admin.register(Cidadao)
class CredelecCounterByHome(admin.ModelAdmin):
    list_display = ['id', "full_name", "numero_bi_nuit", "endereco", 'nacionalidade', "provincia", "distrito", "data_nascimento"]
