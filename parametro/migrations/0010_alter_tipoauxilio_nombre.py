# Generated by Django 5.0.6 on 2025-02-07 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametro', '0009_alter_tasasinterescredito_porcentaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoauxilio',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
    ]
