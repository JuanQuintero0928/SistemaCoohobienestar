# Generated by Django 5.0.6 on 2025-03-21 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formapago',
            name='estadoRegistro',
            field=models.BooleanField(default=True),
        ),
    ]
