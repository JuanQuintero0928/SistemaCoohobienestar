# Generated by Django 5.0.6 on 2024-11-05 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0002_historialpagos_fechapago_historialpagos_usercreacion_and_more'),
        ('parametro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialpagos',
            name='adicionalesFecha',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='adicionales_fecha', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='historialpagos',
            name='coohopFecha',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='coohop_fecha', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='historialpagos',
            name='mascotaFecha',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='mascota_fecha', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='historialpagos',
            name='repatriacionFecha',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='repatriacion_fecha', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='historialpagos',
            name='seguroVidaFecha',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='seguroVida_fecha', to='parametro.mestarifa'),
        ),
    ]
