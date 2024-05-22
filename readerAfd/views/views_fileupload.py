from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from readerAfd.models import UserProfile,ConfiguracaoTabela, Empresa, Cabecalho, RegistroInclusaoAlteracao, RegistroMarcacaoPonto, RegistroAjusteRelogio, RegistroAlteracaoExclusao, Rodape, Funcionario, Marcacao
from datetime import datetime
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
from django.contrib.auth.decorators import login_required

 
def limpar_banco_dados():
    models_to_delete = [Rodape,
                        RegistroAlteracaoExclusao,
                        RegistroAjusteRelogio, 
                        RegistroMarcacaoPonto,
                        RegistroInclusaoAlteracao,
                        Cabecalho,
                        Funcionario,
                        Marcacao,
                        
                        ]

    for model in models_to_delete:
        model.objects.all().delete()

 
def tabelaConfig(request, user=None):
    if user is None:
        user = request.user  # Obter o usuário logado se nenhum usuário for fornecido

    diaSemana = [
        'SEG',
        'TER',
        'QUA',
        'QUI',
        'SEX',
        'SAB',
        'DOM'
        ]
    
    for dia in diaSemana:
        config, created = ConfiguracaoTabela.objects.get_or_create(
            diaSemana=dia,
            user=user,  # use the provided user here
            defaults={'tolerancia': '00:00:00', 'esperado': '00:00:00'}
        )

        if dia in ['SEG', 'TER', 'QUA', 'QUI', 'SEX']:
            config.tolerancia = '00:10:00'
            config.esperado = '08:00:00'
        
        elif dia == 'SAB':
            config.tolerancia = '00:10:00'
            config.esperado = '04:00:00'

        config.save()


 
def processar_cabecalho(linha, user):
    cabecalho, created = Cabecalho.objects.update_or_create(
        referencia_campo=linha[0:9].strip(),
        tipo_registro=linha[9].strip(),
        tipo_identificador=linha[10].strip(),
        cnpj_cpf=linha[11:25].strip(),
        cei=linha[25:37].strip(),
        razao_social_nome=linha[37:187].strip(),
        numero_fabricacao_rep=linha[187:204].strip(),
        data_inicial=linha[204:212].strip(),
        data_final=linha[212:220].strip(),
        data_geracao=linha[220:228].strip(),
        horario_geracao=datetime.strptime(linha[228:232].strip(), "%H%M").strftime("%H:%M"),
        user=user,
        defaults={
            'empresa': Empresa.objects.get_or_create(user=user, cnpj=linha[11:25].strip())[0],
            'updated_at': timezone.now(),
        }
    )
    return cabecalho

 
def processar_inclusao_alteracao(linha, cabecalho, rodape):
    rodape = Rodape()

    registro_inclusao_alteracao, created = RegistroInclusaoAlteracao.objects.update_or_create(
        nsr=linha[0:9].strip(),
        tipo_registro=linha[9].strip(),
        data_gravacao=linha[10:18].strip(),
        horario_gravacao=datetime.strptime(linha[19:22].strip(), "%H%M").strftime("%H:%M"),
        tipo_identificador=linha[23].strip(),
        cnpj_cpf=linha[24:37].strip(),
        cei=linha[38:49].strip(),
        razao_social_nome=linha[50:199].strip(),
        local_prestacao_servicos=linha[200:299].strip(),
        empresa=cabecalho.empresa,
        user=cabecalho.user,
        defaults={
            'updated_at': timezone.now(),
        }
    )
    rodape.quantidade_registros_tipo_2 += 1
    rodape.save()

 
def processar_marcacao_ponto(linha, cabecalho, rodape):
    rodape = Rodape()

    # Converta a data para o formato YYYY-MM-DD
    data_formatada = datetime.strptime(linha[10:18].strip(), '%d%m%Y').date()

    # Busca o RegistroAlteracaoExclusao correspondente
    registro_alteracao_exclusao = RegistroAlteracaoExclusao.objects.filter(numero_pis=linha[22:34].strip()).first()

    nome_empregado = registro_alteracao_exclusao.nome_empregado if registro_alteracao_exclusao else None

    registro_marcacao_ponto, created = RegistroMarcacaoPonto.objects.update_or_create(
        nsr=linha[0:9].strip(),
        tipo_registro=linha[9].strip(),
        data_marcacao=linha[10:18].strip(),
        horario_marcacao=datetime.strptime(linha[18:22].strip(), "%H%M").strftime("%H:%M"),
        numero_pis=linha[22:34].strip(),
        empresa=cabecalho.empresa,
        user=cabecalho.user,
        defaults={
            'updated_at': timezone.now(),
        }
    )

    rodape.quantidade_registros_tipo_3 += 1

    marcacao, created = Marcacao.objects.update_or_create(
        nsr=registro_marcacao_ponto.nsr,
        pis=registro_marcacao_ponto.numero_pis,
        data=data_formatada,
        hora=registro_marcacao_ponto.horario_marcacao,
        nome=nome_empregado, 
        empresa=cabecalho.empresa,
        user=cabecalho.user,
        defaults={
            'updated_at': timezone.now(),
        }
    )
 
def processar_alteracao_relogio(linha, cabecalho, rodape):
    rodape = Rodape()

    registro_alteracao_relogio, created = RegistroAjusteRelogio.objects.update_or_create(
        nsr=linha[0:9].strip(),
        tipo_registro=linha[9].strip(),
        data_antes_ajuste=linha[10:18].strip(),
        horario_antes_ajuste=linha[18:22].strip(),
        data_ajustada=linha[22:30].strip(),
        horario_ajustado=linha[30:34].strip(),
        empresa=cabecalho.empresa,
        user=cabecalho.user,
        defaults={
            'updated_at': timezone.now(),
        }
    )

    rodape.quantidade_registros_tipo_4 += 1
    rodape.save()

 
def processar_alteracao_exclusao(linha, cabecalho, rodape):
    rodape = Rodape()

    registro_alteracao_exclusao, created = RegistroAlteracaoExclusao.objects.update_or_create(
        nsr = linha[0:9].strip(),
        tipo_registro = linha[9].strip(),
        data_gravacao = linha[10:18].strip(),
        horario_gravacao = linha[18:22].strip(),
        tipo_operacao = linha[22].strip(),
        numero_pis = linha[23:35].strip(),
        empresa = cabecalho.empresa,
        user = cabecalho.user,
        defaults = {
            'nome_empregado': linha[35:87].strip(), 
            'updated_at': timezone.now(),
        }
    )

    rodape.quantidade_registros_tipo_5 += 1
    registro_alteracao_exclusao.save()


 
def processar_rodape(linha, cabecalho):
    empresa = Empresa.objects.get(cnpj=cabecalho.cnpj)  # Get the Empresa object
    rodape, created = Rodape.objects.update_or_create(
        referencia_campo=linha[0:9].strip(),
        tipo_registro=linha[9].strip(),
        empresa=empresa,  # Use the Empresa object
        user=cabecalho.user,
        defaults={
            'quantidade_registros_tipo_2': int(linha[10:18].strip()),
            'quantidade_registros_tipo_3': int(linha[18:27].strip()),
            'quantidade_registros_tipo_4': int(linha[27:36].strip()),
            'quantidade_registros_tipo_5': int(linha[36:45].strip()),
            'updated_at': timezone.now(),
        }
    )

 
def empresa(linha, user):
    empresa, created = Empresa.objects.update_or_create(
        cnpj=linha[11:25].strip(),
        defaults={
            'razao_social': linha[37:187].strip(),
            'user': user,
            'updated_at': timezone.now(),
        }
    )


 
def cnpj_usuario(linha, user):
    userProfile = UserProfile.objects.get(user=user)
    empresa, created = Empresa.objects.update_or_create(
        cnpj=linha[11:25].strip(),
        defaults={
            'updated_at': timezone.now(),
        }
    )
    userProfile.empresa = empresa
    userProfile.save()
    user.cnpj = linha[11:25].strip()
    user.save()


def fileupload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        rodape = Rodape()

        funcoes = {
            '1': [empresa, processar_cabecalho, cnpj_usuario],
            '2': [processar_inclusao_alteracao],
            '3': [processar_marcacao_ponto],
            '4': [processar_alteracao_relogio],
            '5': [processar_alteracao_exclusao],
            '999999999': [processar_rodape]
        }

        cabecalho = None

        with file.open() as f:
            for linha in f:
                linha = linha.decode()

                funcoes_linha = funcoes.get(linha[9], None)
                tabelaConfig(request)

                if funcoes_linha:
                    if 'empresa' in [funcao.__name__ for funcao in funcoes_linha] and linha[9] == '1':
                        try:
                            result = empresa(linha, request.user)
                            print(f'Resultado da função empresa: {result}')
                        except MultipleObjectsReturned:
                            messages.error(request, "Empresa Já Cadastrada para o Usuário: " + str(request.user))

                    for funcao in funcoes_linha:
                        with transaction.atomic():
                            try:
                                if linha[9] == '1' and funcao.__name__ == 'processar_cabecalho':
                                    cabecalho = funcao(linha, request.user)
                                    if cabecalho is None:
                                        print("Erro: processar_cabecalho não retornou um valor")
                                elif linha[9] == '1' and funcao.__name__ == 'cnpj_usuario':
                                    funcao(linha, request.user)
                                elif linha[9] == '999999999':
                                    if cabecalho is not None:
                                        funcao(linha, cabecalho)
                                    else:
                                        print("Erro: cabecalho é None")
                                else:
                                    if cabecalho is not None:
                                        funcao(linha, cabecalho, rodape)
                                    else:
                                        print("Erro: cabecalho é None")
                            except Exception as e:
                                print(f"Erro ao executar a função {funcao.__name__}: {e}")

        return redirect('fileData')
    else:
        return render(request, 'readerAfd/fileupload.html')


