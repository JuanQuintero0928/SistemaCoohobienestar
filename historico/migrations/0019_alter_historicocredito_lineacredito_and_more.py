# Generated by Django 5.0.6 on 2025-02-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0018_historicocredito_banco_historicocredito_numcuenta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicocredito',
            name='lineaCredito',
            field=models.CharField(choices=[('ANTICIPO NOMINA', 'ANTICIPO NOMINA'), ('SOLUCION INMEDIATA', 'SOLUCION INMEDIATA'), ('CREDILIBRE', 'CREDILIBRE'), ('CREDICONTIGO', 'CREDICONTIGO'), ('KUPI', 'KUPI'), ('CREDISEGURO', 'CREDISEGURO'), ('CREDITO SOAT', 'CREDITO SOAT')], default='SOLUCION INMEDIATA', verbose_name='Linea Credito'),
        ),
        migrations.AlterField(
            model_name='historicocredito',
            name='tipoCuenta',
            field=models.CharField(blank=True, choices=[('CUENTA AHORROS', 'CUENTA AHORROS'), ('CUENTA CORRIENTE', 'CUENTA CORRIENTE')], null=True, verbose_name='Tipo Cuenta'),
        ),
    ]
