# Generated by Django 5.0.6 on 2024-11-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0006_tarifaasociado_adicionalingreso_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarifaasociado',
            name='mascotaIngreso',
        ),
        migrations.RemoveField(
            model_name='tarifaasociado',
            name='repatriacionIngreso',
        ),
        migrations.AddField(
            model_name='tarifaasociado',
            name='fechaInicioAdicional',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Inicio Adicional'),
        ),
    ]
