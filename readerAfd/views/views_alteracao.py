from datetime import datetime, timedelta
from readerAfd.models import Empresa,Rodape,RegistroAjusteRelogio,RegistroMarcacaoPonto,RegistroInclusaoAlteracao,Cabecalho,RegistroAlteracaoExclusao,Funcionario, Marcacao, UserProfile, ConfiguracaoTabela
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

@login_required
def reset_database(request):
    if request.method == 'POST':

        lista_models = [
            Funcionario,
            RegistroAlteracaoExclusao,
            Cabecalho,
            RegistroInclusaoAlteracao,
            RegistroMarcacaoPonto,
            RegistroAjusteRelogio,
            Rodape,
            Marcacao,
            ConfiguracaoTabela,
            Empresa
        ]

        for model in lista_models:
            model.objects.filter(user=request.user).delete()

        return JsonResponse({'mensagem': 'Marcações deletadas com sucesso.'})
    else:
        return JsonResponse({'erro': 'Requisição inválida'}, status=400)

@login_required
def alterar_registro(request, funcionario_id):
    if request.method == 'POST':
        funcionario = Funcionario.objects.get(id=funcionario_id)
        alteracoes = json.loads(request.body)

        for data_formatada, situacao_alterada in alteracoes.items():
            data_banco = datetime.strptime(data_formatada, '%d/%m/%Y').strftime('%Y-%m-%d')

            if not Marcacao.objects.filter(data=data_banco, pis=funcionario.pis).exists():
                ultimo_nsr = Marcacao.objects.latest('nsr').nsr if Marcacao.objects.exists() else 1
                situacao = next((chave for chave, valor in situacao_alterada.items() if valor), 'normal')

                for i in range(4):
                    horario = (datetime.min + timedelta(hours=1+i)).time()
                    eh_entrada = i % 2 == 0

                    ultimo_nsr = int(ultimo_nsr) + 1
                    nsr_formatado = str(ultimo_nsr).zfill(9)
                    registro = Marcacao.objects.create(
                        data=data_banco, 
                        pis=funcionario.pis, 
                        user=request.user,
                        situacao=situacao,
                        entrada=eh_entrada,
                        saida=not eh_entrada,
                        hora=horario,
                        nome=funcionario.nome,
                        empresa=funcionario.empresa,
                        nsr=nsr_formatado,
                    )
            else:
                marcacoes = Marcacao.objects.filter(data=data_banco)

                for marcacao in marcacoes:
                    situacao = next((chave for chave, valor in situacao_alterada.items() if valor), 'normal')
                    marcacao.situacao = situacao
                    marcacao.save(update=True)

        return JsonResponse({'mensagem': 'Alterações salvas com sucesso.'})
    else:
        return JsonResponse({'erro': 'Requisição inválida'}, status=400)


@csrf_exempt
@login_required
def atualizar_horario(request):
    if request.method == 'POST':
        corpo = json.loads(request.body)
        data = datetime.strptime(corpo['data'], '%d%m%Y').date()
        hora = datetime.strptime(corpo['hora'], '%H:%M').time()
        pis = corpo['pis']
        novaHora = None if corpo['novaHora'].strip() == "" else datetime.strptime(corpo['novaHora'], '%H:%M').time()

        funcionario = Funcionario.objects.get(pis=corpo['pis'])
        marcacao = Marcacao.objects.get(data=data, hora=hora, pis=pis, user=request.user)
        
        if novaHora is None:
            perfil_usuario = UserProfile.objects.get(user=request.user)

            if perfil_usuario.empresa is None:
                return HttpResponse('Empresa não definida para o usuário', status=400)

            registro = Marcacao.objects.filter(pis=pis).order_by('-nsr').first()

            if registro is not None:
                nova_marcacao = Marcacao(
                    nome=funcionario.nome,
                    data=data,
                    pis=pis,
                    hora=None,
                    user=request.user,
                    empresa=perfil_usuario.empresa,
                    entrada=True,
                    saida=False,
                    nsr=str(int(registro.nsr) + 1).zfill(9)
                )
                nova_marcacao.save()
        else:
            marcacao.hora = novaHora
            marcacao.save(update=True)

        return JsonResponse({'status': 'ok'})

@login_required
def criar_nova_marcacao(request):
    if request.method == "POST":
        corpo = json.loads(request.body)
        data = datetime.strptime(corpo['data'], '%d%m%Y').date()
        pis = corpo['pis']
        funcionario = Funcionario.objects.get(pis=corpo['pis'])

        perfil_usuario = UserProfile.objects.get(user=request.user)

        if perfil_usuario.empresa is None:
            return HttpResponse('Empresa não definida para o usuário', status=400)

        registros = Marcacao.objects.filter(data=data, pis=pis).order_by('nsr')

        proxima_entrada = registros.count() % 2 == 0

        if corpo['hora'] == '-':
            novaHora = datetime.strptime(corpo['novaHora'], '%H:%M').time()

            registro = Marcacao.objects.filter(pis=pis).order_by('-nsr').first()
            situacao = Marcacao.objects.filter(data=data, pis=pis).order_by('-nsr').first().situacao if registros.exists() else 'normal'

            nova_marcacao = Marcacao(
                nome=funcionario.nome,
                data=data,
                pis=pis,
                hora=novaHora,
                user=request.user,
                empresa=perfil_usuario.empresa,
                entrada=proxima_entrada,
                saida=not proxima_entrada,
                situacao=situacao,
                nsr=str((int(registro.nsr) + 1) if registro else 1).zfill(9)
            )
            nova_marcacao.save(update=True)
        else:
            if registros.exists():
                registros.last().delete()

        return HttpResponse('Marcação atualizada com sucesso', status=200)
    else:
        return HttpResponse('Requisição inválida', status=400)



@login_required
def delete_marcacao_unica(request):
    if request.method == "POST":
        corpo = json.loads(request.body)
        data = datetime.strptime(corpo['data'], '%d%m%Y').date()
        pis = corpo['pis']
        hora = datetime.strptime(corpo['hora'], '%H:%M').time()

        marcacao = Marcacao.objects.filter(data=data, pis=pis, hora=hora, user=request.user)
        marcacao.delete()

        return JsonResponse({'status': 'ok'})

@login_required
def atualizar_configuracao(request):
    if request.method == "POST":
        corpo = json.loads(request.body)
        dia = corpo['dia']
        campo = corpo['campo']
        antigo = datetime.strptime(corpo['antigo'], '%H:%M').time()
        novoValor = datetime.strptime(corpo['novoValor'], '%H:%M').time()

        try:
            configuracao = ConfiguracaoTabela.objects.get(diaSemana=dia, user=request.user)
            if campo == 'tolerancia':
                configuracao.tolerancia = novoValor
            elif campo == 'esperado':
                configuracao.esperado = novoValor
            else:
                return JsonResponse({'status': 'error', 'message': 'Campo inválido.'})
            configuracao.save(update_fields=[campo])
            return JsonResponse({'status': 'ok'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Configuração não encontrada.'})

@login_required
def deletar_marcacao(request):
    if request.method == "POST":
        corpo = json.loads(request.body)
        data = datetime.strptime(corpo['data'], '%d%m%Y').date()
        pis = corpo['pis']

        marcacoes = Marcacao.objects.filter(data=data, pis=pis, user=request.user)
        marcacoes.delete()

        return JsonResponse({'status': 'ok'})