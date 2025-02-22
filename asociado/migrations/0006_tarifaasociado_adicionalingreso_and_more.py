# Generated by Django 5.0.6 on 2024-11-05 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0005_alter_asociado_tipodocumento'),
        ('parametro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarifaasociado',
            name='adicionalIngreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='adicionalIngreso', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='tarifaasociado',
            name='coohopIngreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='coohopIngreso', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='tarifaasociado',
            name='mascotaIngreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='mascotaIngreso', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='tarifaasociado',
            name='repatriacionIngreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='repatriacionIngreso', to='parametro.mestarifa'),
        ),
        migrations.AddField(
            model_name='tarifaasociado',
            name='seguroVidaIngreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='seguroVidaIngreso', to='parametro.mestarifa'),
        ),
    ]
