# Generated by Django 5.0.2 on 2024-03-06 05:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoTabela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diaSemana', models.CharField(max_length=10)),
                ('tolerancia', models.TimeField()),
                ('esperado', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=14)),
                ('razao_social', models.CharField(max_length=150)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='empresa_associada', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cabecalho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia_campo', models.CharField(max_length=9)),
                ('tipo_registro', models.CharField(max_length=1)),
                ('tipo_identificador', models.CharField(max_length=1)),
                ('cnpj_cpf', models.CharField(max_length=14)),
                ('cei', models.CharField(blank=True, max_length=12, null=True)),
                ('razao_social_nome', models.CharField(max_length=150)),
                ('numero_fabricacao_rep', models.CharField(max_length=17)),
                ('data_inicial', models.CharField(max_length=8)),
                ('data_final', models.CharField(max_length=8)),
                ('data_geracao', models.CharField(max_length=8)),
                ('horario_geracao', models.CharField(max_length=8)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pis', models.CharField(max_length=12, unique=True)),
                ('nome', models.CharField(max_length=52)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Marcacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsr', models.CharField(max_length=9)),
                ('pis', models.CharField(max_length=12)),
                ('data', models.DateField()),
                ('hora', models.TimeField(blank=True, null=True)),
                ('nome', models.CharField(blank=True, max_length=52, null=True)),
                ('entrada', models.BooleanField(blank=True, default=False, null=True)),
                ('saida', models.BooleanField(blank=True, default=False, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('situacao', models.CharField(choices=[('ferias', 'ferias'), ('pagar', 'pagar'), ('folga', 'folga'), ('atestado', 'Atestado'), ('normal', 'normal')], default='normal', max_length=8)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroAjusteRelogio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsr', models.CharField(max_length=9)),
                ('tipo_registro', models.CharField(max_length=1)),
                ('data_antes_ajuste', models.CharField(max_length=8)),
                ('horario_antes_ajuste', models.CharField(max_length=4)),
                ('data_ajustada', models.CharField(max_length=8)),
                ('horario_ajustado', models.CharField(max_length=4)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroAlteracaoExclusao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsr', models.CharField(max_length=9)),
                ('tipo_registro', models.CharField(max_length=1)),
                ('data_gravacao', models.CharField(max_length=8)),
                ('horario_gravacao', models.CharField(max_length=4)),
                ('tipo_operacao', models.CharField(max_length=1)),
                ('numero_pis', models.CharField(max_length=12)),
                ('nome_empregado', models.CharField(max_length=52)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroInclusaoAlteracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsr', models.CharField(max_length=9)),
                ('tipo_registro', models.CharField(max_length=1)),
                ('data_gravacao', models.CharField(max_length=8)),
                ('horario_gravacao', models.CharField(max_length=4)),
                ('tipo_identificador', models.CharField(max_length=1)),
                ('cnpj_cpf', models.CharField(max_length=14)),
                ('cei', models.CharField(blank=True, max_length=12, null=True)),
                ('razao_social_nome', models.CharField(max_length=150)),
                ('local_prestacao_servicos', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroMarcacaoPonto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsr', models.CharField(max_length=9)),
                ('tipo_registro', models.CharField(default='3', max_length=1)),
                ('data_marcacao', models.CharField(max_length=8)),
                ('horario_marcacao', models.CharField(max_length=4)),
                ('numero_pis', models.CharField(max_length=12)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rodape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsr', models.CharField(default='999999999', max_length=9)),
                ('quantidade_registros_tipo_2', models.IntegerField(default=0)),
                ('quantidade_registros_tipo_3', models.IntegerField(default=0)),
                ('quantidade_registros_tipo_4', models.IntegerField(default=0)),
                ('quantidade_registros_tipo_5', models.IntegerField(default=0)),
                ('tipo_registro', models.CharField(default='5', max_length=1)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readerAfd.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario_associado', to='readerAfd.empresa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
