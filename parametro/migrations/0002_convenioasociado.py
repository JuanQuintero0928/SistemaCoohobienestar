# Generated by Django 5.0.6 on 2024-12-03 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvenioAsociado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField(verbose_name='Fecha Inicio')),
                ('concepto', models.CharField(max_length=30, verbose_name='Convenio Asociado')),
                ('valor', models.IntegerField(verbose_name='Valor')),
                ('fechaTerminacion', models.DateField(blank=True, null=True, verbose_name='Fecha Terminacion')),
                ('estado', models.BooleanField(verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Convenio Asociado',
                'verbose_name_plural': 'Convenio Asociado',
                'ordering': ['pk'],
            },
        ),
    ]