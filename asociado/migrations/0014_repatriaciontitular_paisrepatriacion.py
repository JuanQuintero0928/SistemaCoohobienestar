# Generated by Django 5.0.6 on 2024-11-20 01:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0013_repatriaciontitular'),
        ('departamento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repatriaciontitular',
            name='PaisRepatriacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='departamento.paisrepatriacion'),
        ),
    ]
