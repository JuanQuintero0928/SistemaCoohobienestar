# Generated by Django 5.0.6 on 2024-10-08 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiario', '0002_alter_beneficiario_apellido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiario',
            name='numDocumento',
            field=models.CharField(max_length=12, verbose_name='Número Documento'),
        ),
    ]
