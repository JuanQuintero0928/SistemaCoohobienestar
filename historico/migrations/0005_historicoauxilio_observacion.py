# Generated by Django 5.0.6 on 2024-11-07 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0004_remove_historialpagos_adicionalesfecha_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoauxilio',
            name='observacion',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Observaciones'),
        ),
    ]
