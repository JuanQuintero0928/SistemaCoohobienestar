# Generated by Django 5.0.6 on 2025-04-09 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0004_historialpagos_creditoid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialpagos',
            name='creditoHomeElements',
            field=models.IntegerField(blank=True, null=True, verbose_name='Credito Home Elements'),
        ),
    ]
