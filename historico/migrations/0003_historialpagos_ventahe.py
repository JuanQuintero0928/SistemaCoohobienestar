# Generated by Django 5.0.6 on 2025-04-08 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0002_initial'),
        ('ventas', '0003_alter_historicoventa_formapago'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialpagos',
            name='ventaHE',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagosHE', to='ventas.historicoventa'),
        ),
    ]
