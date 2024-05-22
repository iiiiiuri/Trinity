from django.contrib import admin
from .models import Empresa, ConfiguracaoTabela, UserProfile, Cabecalho, RegistroInclusaoAlteracao, RegistroMarcacaoPonto, RegistroAjusteRelogio, RegistroAlteracaoExclusao, Rodape, Funcionario, Marcacao

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('user',)

class CabecalhoAdmin(admin.ModelAdmin):
    list_filter = ('razao_social_nome', 'user')

class FuncionarioAdmin(admin.ModelAdmin):
    list_filter = ('nome', 'user')

class RegistroInclusaoAlteracaoAdmin(admin.ModelAdmin):
    list_filter = ('empresa', 'user')

class RegistroAjusteRelogioAdmin(admin.ModelAdmin):
    list_filter = ('empresa', 'user')

class RegistroAlteracaoExclusaoAdmin(admin.ModelAdmin):
    list_filter = ('empresa', 'user')

class RodapeAdmin(admin.ModelAdmin):
    list_filter = ('empresa', 'user')

class RegistroMarcacaoPontoAdmin(admin.ModelAdmin):
    list_filter = ('empresa', 'user')

class ConfiguracaoTabelaAdmin(admin.ModelAdmin):
    list_filter = ('diaSemana', 'user')

class MarcacaoAdmin(admin.ModelAdmin):
    list_display = ('nome','situacao', 'user')
    list_filter = ('nome','situacao', 'user')



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Cabecalho, CabecalhoAdmin)
admin.site.register(RegistroInclusaoAlteracao, RegistroInclusaoAlteracaoAdmin)
admin.site.register(RegistroAjusteRelogio, RegistroAjusteRelogioAdmin)
admin.site.register(RegistroAlteracaoExclusao, RegistroAlteracaoExclusaoAdmin)
admin.site.register(Rodape, RodapeAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Marcacao, MarcacaoAdmin)
admin.site.register(ConfiguracaoTabela, ConfiguracaoTabelaAdmin)
admin.site.register(Empresa)
