# Generated by Django 5.0.6 on 2024-11-20 02:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0016_rename_paisrepatriacion_repatriaciontitular_paisrepatriacion'),
        ('departamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repatriaciontitular',
            name='paisRepatriacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='departamento.paisrepatriacion'),
        ),
    ]
