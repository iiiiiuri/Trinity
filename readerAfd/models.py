from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.SET_NULL, related_name='usuario_associado', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return 'Usuário : ' + self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Funcionario(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    pis = models.CharField(max_length=12, unique=True)
    nome = models.CharField(max_length=52)

    def __str__(self):
        return "Nome : " + self.nome + " PIS : " + self.pis + " Empresa : " + self.empresa.razao_social

class RegistroAlteracaoExclusao(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nsr = models.CharField(max_length=9)
    tipo_registro = models.CharField(max_length=1)
    data_gravacao = models.CharField(max_length=8)
    horario_gravacao = models.CharField(max_length=4)
    tipo_operacao = models.CharField(max_length=1)
    numero_pis = models.CharField(max_length=12)
    nome_empregado = models.CharField(max_length=52)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Registro Número : " + str(self.nsr)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.tipo_operacao != 'E':
            Funcionario.objects.update_or_create(
                pis=self.numero_pis, 
                defaults={
                    'nome': self.nome_empregado,
                    'empresa': self.empresa,
                    'user': self.user
                }
            )

class Cabecalho(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    referencia_campo = models.CharField(max_length=9)
    tipo_registro = models.CharField(max_length=1)
    tipo_identificador = models.CharField(max_length=1)
    cnpj_cpf = models.CharField(max_length=14)
    cei = models.CharField(max_length=12, blank=True, null=True)
    razao_social_nome = models.CharField(max_length=150)
    numero_fabricacao_rep = models.CharField(max_length=17)
    data_inicial = models.CharField(max_length=8)
    data_final = models.CharField(max_length=8)
    data_geracao = models.CharField(max_length=8)
    horario_geracao = models.CharField(max_length=8)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Registro Número : " + str(self.referencia_campo)

class RegistroInclusaoAlteracao(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nsr = models.CharField(max_length=9)
    tipo_registro = models.CharField(max_length=1)
    data_gravacao = models.CharField(max_length=8)
    horario_gravacao = models.CharField(max_length=4)
    tipo_identificador = models.CharField(max_length=1)
    cnpj_cpf = models.CharField(max_length=14)
    cei = models.CharField(max_length=12, blank=True, null=True)
    razao_social_nome = models.CharField(max_length=150)
    local_prestacao_servicos = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Registro Número : " + str(self.nsr)

class RegistroMarcacaoPonto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nsr = models.CharField(max_length=9)
    tipo_registro = models.CharField(max_length=1, default="3")
    data_marcacao = models.CharField(max_length=8)
    horario_marcacao = models.CharField(max_length=4)
    numero_pis = models.CharField(max_length=12)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Registro Número : " + str(self.nsr)

class RegistroAjusteRelogio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nsr = models.CharField(max_length=9)
    tipo_registro = models.CharField(max_length=1)
    data_antes_ajuste = models.CharField(max_length=8)
    horario_antes_ajuste = models.CharField(max_length=4)
    data_ajustada = models.CharField(max_length=8)
    horario_ajustado = models.CharField(max_length=4)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Registro Número : " + str(self.nsr)

class Rodape(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nsr = models.CharField(max_length=9, default="999999999")
    quantidade_registros_tipo_2 = models.IntegerField(default=0)
    quantidade_registros_tipo_3 = models.IntegerField(default=0)
    quantidade_registros_tipo_4 = models.IntegerField(default=0)
    quantidade_registros_tipo_5 = models.IntegerField(default=0)
    tipo_registro = models.CharField(max_length=1, default="5")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Registro Número : " + str(self.nsr)

class Marcacao(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nsr = models.CharField(max_length=9)
    pis = models.CharField(max_length=12)
    data = models.DateField()
    hora = models.TimeField(blank=True, null=True)
    nome = models.CharField(max_length=52, blank=True, null=True)
    entrada = models.BooleanField(default=False, blank=True, null=True)
    saida = models.BooleanField(default=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    SITUACAO_CHOICES = [
            ('ferias', 'ferias'),
            ('pagar', 'pagar'),
            ('folga', 'folga'),
            
('atestado', 'Atestado'),
            ('normal', 'normal'),
    ]
    situacao = models.CharField(
            max_length=8,
            choices=SITUACAO_CHOICES,
            default='normal',
    )

    def save(self, *args, **kwargs):
        update = kwargs.pop('update', False)
        if not update:
            # Obtenha todas as marcações do mesmo dia para o mesmo PIS
            marcacoes_mesmo_dia = Marcacao.objects.filter(pis=self.pis, data=self.data).order_by('nsr')

            # Conta o número de marcações existentes no mesmo dia
            count = marcacoes_mesmo_dia.count()

            # Se não houver marcações para o mesmo dia, então é a primeira marcação
            if count == 0:
                self.entrada = True
            # Se houver apenas uma marcação, então é a segunda marcação
            elif count == 1:
                self.saida = True
            # Se houver mais de duas marcações, então é a terceira marcação
            elif count == 2:
                self.entrada = True
            # Se houver mais de três marcações, então é a quarta marcação
            elif count == 3:
                self.saida = True

        super().save(*args, **kwargs)
        
        @receiver(post_save, sender=Marcacao)
        def update_marcacao_ponto(sender, instance, created, **kwargs):
            if not created:  
                try:
                    marcacao_ponto = RegistroMarcacaoPonto.objects.get(nsr=instance.nsr)
                    hora_as_string = instance.hora.strftime('%H:%M:%S')
                    if ':' in hora_as_string:
                        hh, mm, ss = hora_as_string.split(':')
                        formatted_hora = hh + mm
                    else:

                        formatted_hora = hora_as_string
                    marcacao_ponto.horario_marcacao = formatted_hora
                    marcacao_ponto.save()
                except RegistroMarcacaoPonto.DoesNotExist:
                    pass
    def __str__(self):
        return " Data : " + str(self.data) + " Nsr : " +str(self.nsr)


class ConfiguracaoTabela(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diaSemana = models.CharField(max_length=10)
    tolerancia = models.TimeField()
    esperado  = models.TimeField()
    
    

    def __str__(self):
        return "Dia da Semana : " + str(self.diaSemana) + " Tolerancia : " + str(self.tolerancia) + " Esperado : " + str(self.esperado)

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa_associada')
    cnpj = models.CharField(max_length=14)
    razao_social = models.CharField(max_length=150)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.razao_social  