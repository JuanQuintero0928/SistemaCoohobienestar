# Generated by Django 5.0.6 on 2024-08-15 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0009_rename_tipopersona_asociado_tpersona'),
        ('departamento', '0002_paisrepatriacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='asociado',
            name='dtoNacimiento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='departamento.departamento'),
            preserve_default=False,
        ),
    ]
