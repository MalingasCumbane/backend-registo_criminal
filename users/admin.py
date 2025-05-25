from django.contrib import admin
from .models import User, Cidadao, FuncionarioJudicial

admin.site.register(User)
admin.site.register(FuncionarioJudicial)

@admin.register(Cidadao)
class CredelecCounterByHome(admin.ModelAdmin):
    list_display = ['id', "full_name", "numero_bi_nuit", "endereco", 'nacionalidade', "provincia", "distrito", "data_nascimento"]
