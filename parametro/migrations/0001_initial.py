# Generated by Django 5.0.6 on 2024-09-12 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormaPago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('formaPago', models.CharField(max_length=30, verbose_name='Forma Pago')),
            ],
            options={
                'verbose_name': 'Forma de Pago',
                'verbose_name_plural': 'Forma de Pago',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='MesTarifa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.CharField(max_length=30, verbose_name='Concepto')),
                ('aporte', models.IntegerField(verbose_name='Aporte')),
                ('bSocial', models.IntegerField(verbose_name='Bienestar Social')),
                ('fechaInicio', models.DateField(blank=True, null=True, verbose_name='Fecha Inicio')),
                ('fechaFinal', models.DateField(blank=True, null=True, verbose_name='Fecha Final')),
            ],
            options={
                'verbose_name': 'Tarifa Por Mes',
                'verbose_name_plural': 'Tarifa Por Mes',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ServicioFuneraria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.CharField(max_length=30, verbose_name='Servicio Funerario')),
            ],
            options={
                'verbose_name': 'Servicio Funeraria',
                'verbose_name_plural': 'Servicio Funeraria',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Tarifas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.CharField(max_length=30, verbose_name='Concepto')),
                ('cuenta', models.IntegerField(verbose_name='Cuenta')),
                ('valor', models.IntegerField(verbose_name='Valor')),
                ('estadoRegistro', models.BooleanField(verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Tarifa',
                'verbose_name_plural': 'Tarifas',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='TipoAsociado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.CharField(max_length=30, verbose_name='Tipo Asociado')),
            ],
            options={
                'verbose_name': 'Tipo Asociado',
                'verbose_name_plural': 'Tipo Asociado',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='TipoAuxilio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('valor', models.IntegerField(verbose_name='Valor')),
                ('estadoRegistro', models.BooleanField(verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Tipo Auxilio',
                'verbose_name_plural': 'Tipo Auxilio',
                'ordering': ['pk'],
            },
        ),
    ]
