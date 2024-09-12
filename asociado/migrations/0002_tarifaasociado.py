# Generated by Django 5.0.6 on 2024-09-12 02:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TarifaAsociado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cuotaAporte', models.IntegerField(verbose_name='Aporte')),
                ('cuotaBSocial', models.IntegerField(verbose_name='Bienestar Social')),
                ('cuotaMascota', models.IntegerField(blank=True, null=True, verbose_name='Mascota')),
                ('cuotaRepatriacion', models.IntegerField(blank=True, null=True, verbose_name='Repatriacion')),
                ('cuotaSeguroVida', models.IntegerField(blank=True, null=True, verbose_name='Seguro Vida')),
                ('cuotaAdicionales', models.IntegerField(blank=True, null=True, verbose_name='Adicionales')),
                ('cuotaCoohopAporte', models.IntegerField(blank=True, null=True, verbose_name='Coohoperativito Aporte')),
                ('cuotaCoohopBsocial', models.IntegerField(blank=True, null=True, verbose_name='Coohoperativito Bienestar Social')),
                ('total', models.IntegerField(verbose_name='Total')),
                ('estadoRegistro', models.BooleanField(verbose_name='Estado')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('asociado', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='asociado.asociado')),
            ],
            options={
                'verbose_name': 'Tarifa Por Asociado',
                'verbose_name_plural': 'Tarifa Por Asociado',
                'ordering': ['pk'],
            },
        ),
    ]
