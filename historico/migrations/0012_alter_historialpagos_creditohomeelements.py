# Generated by Django 5.0.6 on 2025-01-15 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0011_historialpagos_creditohomeelements_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialpagos',
            name='creditoHomeElements',
            field=models.IntegerField(default=0, verbose_name='Credito Home Elements'),
            preserve_default=False,
        ),
    ]
