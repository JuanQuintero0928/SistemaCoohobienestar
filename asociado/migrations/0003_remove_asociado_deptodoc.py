# Generated by Django 5.0.6 on 2024-07-03 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0002_remove_residencia_fechaingreso_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asociado',
            name='deptoDoc',
        ),
    ]
