# Generated by Django 5.0.6 on 2024-12-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0006_historicoauxilio_entidadbancaria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoauxilio',
            name='motivoEliminacion',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Motivo de Eliminacion'),
        ),
    ]