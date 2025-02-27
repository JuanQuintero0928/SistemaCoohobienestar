# Generated by Django 5.0.6 on 2025-02-12 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0036_alter_asociado_indicativocelular'),
        ('parametro', '0010_alter_tipoauxilio_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametroasociado',
            name='vinculacionCuotas',
            field=models.IntegerField(blank=True, null=True, verbose_name='Vincualacion cuotas'),
        ),
        migrations.AddField(
            model_name='parametroasociado',
            name='vinculacionFormaPago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='parametro.formapago'),
        ),
        migrations.AddField(
            model_name='parametroasociado',
            name='vinculacionValor',
            field=models.IntegerField(blank=True, null=True, verbose_name='Vinculacion valor'),
        ),
    ]
