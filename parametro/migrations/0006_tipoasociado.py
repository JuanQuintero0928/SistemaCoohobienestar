# Generated by Django 5.0.6 on 2024-08-09 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametro', '0005_formapago'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoAsociado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('concepto', models.CharField(max_length=30, verbose_name='Tipo Asociado')),
            ],
            options={
                'verbose_name': 'Tipo Asociado',
                'verbose_name_plural': 'Tipo Asociado',
                'ordering': ['pk'],
            },
        ),
    ]
