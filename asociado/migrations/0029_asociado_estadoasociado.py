# Generated by Django 5.0.6 on 2024-08-23 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0028_asociado_tasociado_alter_referenciafamiliar_nombre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asociado',
            name='estadoAsociado',
            field=models.CharField(choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO'), ('RETIRADO', 'RETIRADO')], default='ACTIVO', verbose_name='Estado Asociado'),
        ),
    ]
