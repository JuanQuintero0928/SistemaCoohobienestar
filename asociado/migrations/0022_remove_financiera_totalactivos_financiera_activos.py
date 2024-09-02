# Generated by Django 5.0.6 on 2024-08-20 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0021_financiera_referenciafamiliar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financiera',
            name='totalActivos',
        ),
        migrations.AddField(
            model_name='financiera',
            name='activos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Activos'),
        ),
    ]
