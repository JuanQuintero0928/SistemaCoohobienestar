# Generated by Django 5.0.6 on 2024-12-14 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_alter_historicoventa_formapago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoventa',
            name='formaPago',
            field=models.CharField(choices=[('CREDITO', 'CREDITO'), ('CONTADO', 'CONTADO')], default='CREDITO'),
        ),
    ]
