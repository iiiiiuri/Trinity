from django.contrib.auth.models import User
from django.shortcuts import render
from readerAfd.models import (Cabecalho, RegistroInclusaoAlteracao, RegistroMarcacaoPonto, 
                  RegistroAjusteRelogio, RegistroAlteracaoExclusao, Rodape, Funcionario, Marcacao, ConfiguracaoTabela)
import time
from django.contrib.auth.decorators import login_required

@login_required
def fileData(request):
    user = request.user
    cabecalho = Cabecalho.objects.filter(user=user)
    registro_inclusao_alteracao = RegistroInclusaoAlteracao.objects.filter(user=user)
    registro_marcacao_ponto = RegistroMarcacaoPonto.objects.filter(user=user)
    registro_alteracao_relogio = RegistroAjusteRelogio.objects.filter(user=user)
    registro_alteracao_exclusao = RegistroAlteracaoExclusao.objects.filter(user=user)
    rodape = Rodape.objects.filter(user=user)
    funcionario = Funcionario.objects.filter(user=user)
    diaAtual = time.strftime("%d%m%Y")
    configuracoes = ConfiguracaoTabela.objects.filter(user=user)

    configuracoes_list = list(configuracoes)
    for configuracao in configuracoes_list:
        configuracao.tolerancia = configuracao.tolerancia.strftime('%H:%M')
        configuracao.esperado = configuracao.esperado.strftime('%H:%M')

    return render(request, 'readerAfd/fileInfo.html', {
        'cabecalho': cabecalho,
        'registro_inclusao_alteracao': registro_inclusao_alteracao,
        'registro_marcacao_ponto': registro_marcacao_ponto,
        'registro_alteracao_relogio': registro_alteracao_relogio,
        'registro_alteracao_exclusao': registro_alteracao_exclusao,
        'funcionario' : funcionario,
        'rodape': rodape,
        'diaAtual' : diaAtual,
        'configuracoes': configuracoes_list
    })

def timedelta_to_hhmm(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return "{:02}:{:02}".format(hours, minutes)





