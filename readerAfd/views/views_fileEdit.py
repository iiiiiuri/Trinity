import json
from django.shortcuts import render, HttpResponse
from readerAfd.models import Funcionario, Marcacao, ConfiguracaoTabela, UserProfile
from datetime import datetime, date, time, timedelta
from calendar import monthrange
import calendar
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def get_data_marcacao(marcacao):
    return marcacao.data.strftime('%d/%m/%Y')


def add_marcacao(marcacoes_por_dia, marcacao, data_marcacao):
    if marcacao.entrada and marcacao.hora is not None:
        marcacoes_por_dia[data_marcacao]['entradas'].append(marcacao.hora.strftime('%H:%M'))
    elif marcacao.hora is not None:
        marcacoes_por_dia[data_marcacao]['saidas'].append(marcacao.hora.strftime('%H:%M'))


def calculate_tempo_str(entradas, saidas):
    total_seconds = 0
    for entrada, saida in zip(entradas, saidas):
        entrada = datetime.strptime(entrada, '%H:%M')
        saida = datetime.strptime(saida, '%H:%M')

        # Calculate the time difference and add it to the total
        tempo = saida - entrada
        total_seconds += tempo.seconds

    # Convert the total seconds to 'hh:mm' format and store it in 'tempo_str'
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}"


def get_marcacoes_por_dia(marcacoes):
    marcacoes_por_dia = {}
    for marcacao in marcacoes:
        marcacao.refresh_from_db() 

        data_marcacao = get_data_marcacao(marcacao)

        if data_marcacao not in marcacoes_por_dia:
            marcacoes_por_dia[data_marcacao] = {'entradas': [], 'saidas': [],  'tempo_str': '00:00'}

        add_marcacao(marcacoes_por_dia, marcacao, data_marcacao)

        # Ensure there is an equal number of entries and exits
        if len(marcacoes_por_dia[data_marcacao]['entradas']) == len(marcacoes_por_dia[data_marcacao]['saidas']):
            marcacoes_por_dia[data_marcacao]['tempo_str'] = calculate_tempo_str(marcacoes_por_dia[data_marcacao]['entradas'], marcacoes_por_dia[data_marcacao]['saidas'])

    return marcacoes_por_dia



def get_marcacoes(pis, mes, ano, user):
    data_inicio = datetime(day=1, month=mes, year=ano)
    _, ultimo_dia = monthrange(ano, mes)
    data_fim = datetime(day=ultimo_dia, month=mes, year=ano)
    return Marcacao.objects.filter(pis=pis, data__range=(data_inicio, data_fim), user=user)
    
def get_dias_mes(mes, ano):
    NomesPortugues = {
        'Sunday': 'DOM',
        'Monday': 'SEG',
        'Tuesday': 'TER',
        'Wednesday': 'QUA',
        'Thursday': 'QUI',
        'Friday': 'SEX',
        'Saturday': 'SAB'
    }

    diasMes = []
    _, num_dias = monthrange(ano, mes)
    for day in range(1, num_dias + 1):
        data = datetime(day=day, month=mes, year=ano)
        nome = calendar.day_name[data.weekday()]
        nome = NomesPortugues[nome]
        data_formatada = data.strftime('%d/%m/%Y')
        diasMes.append({'data': data_formatada, 'nome': nome})

    return diasMes

   
def get_funcionario(id, user):
    return Funcionario.objects.get(id=id, user=user)


def CalculoTempoTrabalhado(marcacao):
    tempo = marcacao['tempo_str']
    horas, minutos = [int(i) for i in tempo.split(':')]
    tempo_trabalhado = horas * 60 * 60 + minutos * 60
    return tempo_trabalhado


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{int(hours):02d}:{int(minutes):02d}"


def CalculoTotal(primeira_entrada, segunda_entrada, primeira_saida, segunda_saida):
    tempo_1 = datetime.combine(date.today(), segunda_entrada) - datetime.combine(date.today(), primeira_entrada)
    tempo_2 = datetime.combine(date.today(), segunda_saida) - datetime.combine(date.today(), primeira_saida)
    total = tempo_1 + tempo_2
    return total


def calcular_total(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        primeira_entrada = body['primeira_entrada']
        segunda_entrada = body['segunda_entrada']
        primeira_saida = body['primeira_saida']
        segunda_saida = body['segunda_saida']
        total = CalculoTotal(primeira_entrada, segunda_entrada, primeira_saida, segunda_saida)
        return JsonResponse({'total': str(total)})


def CalculoFalta(tempo_trabalhado, data_atual, user):
    NomesPortugues = {
        'Sunday': 'DOM',
        'Monday': 'SEG',
        'Tuesday': 'TER',
        'Wednesday': 'QUA',
        'Thursday': 'QUI',
        'Friday': 'SEX',
        'Saturday': 'SAB'
    }

    dia_atual = NomesPortugues[data_atual.strftime('%A')]
    configuracao = ConfiguracaoTabela.objects.get(Q(diaSemana=dia_atual, user=user))
    jornada_trabalhado = configuracao.esperado.hour * 3600 + configuracao.esperado.minute * 60 + configuracao.esperado.second
    tolerancia = configuracao.tolerancia.hour * 3600 + configuracao.tolerancia.minute * 60 + configuracao.tolerancia.second
    tempo_trabalhado_ajustado = tempo_trabalhado + tolerancia

    if tempo_trabalhado_ajustado < jornada_trabalhado:
        falta = jornada_trabalhado - tempo_trabalhado_ajustado
    else:
        falta = 0

    return seconds_to_time(falta)


def CalculoHoraExtra(tempo_trabalhado, data_atual, user, pis):
    NomesPortugues = {
        'Sunday': 'DOM',
        'Monday': 'SEG',
        'Tuesday': 'TER',
        'Wednesday': 'QUA',
        'Thursday': 'QUI',
        'Friday': 'SEX',
        'Saturday': 'SAB'
    }

    dia_atual = NomesPortugues[data_atual.strftime('%A')]
    configuracao = ConfiguracaoTabela.objects.get(Q(diaSemana=dia_atual, user=user))
    jornada_trabalho = configuracao.esperado.hour * 3600 + configuracao.esperado.minute * 60 + configuracao.esperado.second
    tolerancia = configuracao.tolerancia.hour * 3600 + configuracao.tolerancia.minute * 60 + configuracao.tolerancia.second
    tempo_trabalhado_ajustado = tempo_trabalhado + tolerancia

    funcionario = Funcionario.objects.get(user=user, pis=pis)

    marcacao = Marcacao.objects.filter(data=data_atual, pis=funcionario.pis).first()

    if tempo_trabalhado_ajustado > jornada_trabalho:
        hora_extra = tempo_trabalhado_ajustado - jornada_trabalho
        if marcacao and marcacao.situacao == 'pagar' and hora_extra > 7200: # 2 hours
            hora_extra = 7200
    else:
        hora_extra = 0

    return seconds_to_time(hora_extra)


def CalculoApagar(tempo_trabalhado, data_atual, user, pis):
    falta = CalculoFalta(tempo_trabalhado, data_atual, user)
    hora_extra = CalculoHoraExtra(tempo_trabalhado, data_atual, user, pis)
    hora_extra = str_to_timedelta(hora_extra)

    funcionario = Funcionario.objects.get(user=user, pis=pis)

    marcacao = Marcacao.objects.filter(data=data_atual, pis=funcionario.pis).first()

    if marcacao and marcacao.situacao != 'pagar':
        return '00:00'
    else:
        dicionario = {
            'MON' : 'SEG',
            'TUE' : 'TER',
            'WED' : 'QUA',
            'THU' : 'QUI',
            'FRI' : 'SEX',
            'SAT' : 'SAB',
            'SUN' : 'DOM'
        }

        dia_semana = data_atual.strftime('%a').upper()  # get weekday in format 'MON', 'TUE', etc.
        dia_semana = dicionario.get(dia_semana, dia_semana)  # convert to Portuguese format

        configuracao = ConfiguracaoTabela.objects.filter(user=user, diaSemana=dia_semana).first()

        if configuracao is not None:
            esperado = datetime.combine(date.min, configuracao.esperado) - datetime.min
            valor_a_pagar =  tempo_trabalhado-esperado.total_seconds()
            if hora_extra is not None:
                valor_a_pagar = valor_a_pagar - hora_extra.total_seconds()

        return seconds_to_time(valor_a_pagar)
    

def str_to_timedelta(time_str):
    parts = list(map(int, time_str.split(':')))
    parts.extend([0]*(3-len(parts)))  # Add 0s if time_str has fewer than 3 parts
    hours, minutes, seconds = parts
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def time_to_minutes(time):
    return time.hour * 60 + time.minute


def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def edit_funcionario(request, id, data):
    funcionario = get_funcionario(id, request.user)
    dia, mes, ano = [int(i) for i in (data[:2], data[2:4], data[4:8])]
    data_atual = datetime(ano, mes, dia)
    diasMes = get_dias_mes(mes, ano)
    marcacoes = get_marcacoes(funcionario.pis, mes, ano, request.user)
    marcacoes_por_dia = get_marcacoes_por_dia(marcacoes)

    # Calcular falta, hora extra e valor a pagar para cada dia
    for data, marcacao in marcacoes_por_dia.items():
        dia, mes, ano = [int(i) for i in data.split('/')]
        data_marcacao = datetime(ano, mes, dia)
        
        tempo_trabalhado = CalculoTempoTrabalhado(marcacao)
        marcacao['falta'] = CalculoFalta(tempo_trabalhado, data_marcacao, request.user)
        marcacao['hora_extra'] = CalculoHoraExtra(tempo_trabalhado, data_marcacao, request.user, funcionario.pis)
        marcacao['valor_a_pagar'] = CalculoApagar(tempo_trabalhado, data_marcacao, request.user, funcionario.pis)


    for dia in diasMes:
        # Convert the date to the expected format
        formatted_date = datetime.strptime(dia['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
        situacao = Marcacao.objects.filter(data=formatted_date, pis=funcionario.pis, user=request.user).first()
        if situacao:
            dia['situacao'] = situacao.situacao
        else:
            dia['situacao'] = 'normal'  # or whatever the default situation is

    esperado_sabado = minutes_to_time(time_to_minutes(ConfiguracaoTabela.objects.get(Q(diaSemana='SAB', user=request.user)).esperado))
    tolerancia_sabado = minutes_to_time(time_to_minutes(ConfiguracaoTabela.objects.get(Q(diaSemana='SAB', user=request.user)).tolerancia))
    tolerancia_semana = minutes_to_time(time_to_minutes(ConfiguracaoTabela.objects.get(Q(diaSemana='SEG', user=request.user)).tolerancia))
    esperado_semana = minutes_to_time(time_to_minutes(ConfiguracaoTabela.objects.get(Q(diaSemana='SEG', user=request.user)).esperado))
    return render(request, 'readerAfd/edit_funcionario.html', 
    {
     'funcionario': funcionario,
     'diasMes': diasMes,
     'marcacoes_por_dia': marcacoes_por_dia,
     'esperado_sabado': esperado_sabado,
     'tolerancia_sabado': tolerancia_sabado,
     'tolerancia_semana': tolerancia_semana,
     'esperado_semana': esperado_semana,
     
    })