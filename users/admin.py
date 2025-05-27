from django.contrib import admin
from .models import Permission, User, Cidadao, FuncionarioJudicial, UserPermissions

admin.site.register(User)
admin.site.register(FuncionarioJudicial)

@admin.register(Cidadao)
class CredelecCounterByHome(admin.ModelAdmin):
    list_display = ['id', "full_name", "numero_bi_nuit", "endereco", 'nacionalidade', "provincia", "distrito", "data_nascimento"]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', "description"]


@admin.register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ['id', "utilizador", "role"]

