# Generated by Django 5.0.6 on 2024-12-03 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0022_alter_repatriaciontitular_ciudadrepatriacion_and_more'),
        ('parametro', '0003_rename_convenioasociado_convenio'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConveniosAsociado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaIngreso', models.DateField(verbose_name='Fecha Ingreso')),
                ('fechaRetiro', models.DateField(blank=True, null=True, verbose_name='Fecha Retiro')),
                ('estadoRegistro', models.BooleanField(verbose_name='Estado')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('asociado', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='asociado.asociado')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='parametro.convenio')),
            ],
            options={
                'verbose_name': 'Convenios Asociado',
                'ordering': ['pk'],
            },
        ),
    ]