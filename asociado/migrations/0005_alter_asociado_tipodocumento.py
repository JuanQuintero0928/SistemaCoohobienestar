# Generated by Django 5.0.6 on 2024-10-31 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0004_alter_laboral_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asociado',
            name='tipoDocumento',
            field=models.CharField(choices=[('CEDULA', 'CEDULA'), ('REGISTRO CIVIL', 'REGISTRO CIVIL'), ('TARJETA IDENTIDAD', 'TARJETA IDENTIDAD'), ('CEDULA EXTRANJERA', 'CEDULA EXTRANJERA'), ('PASAPORTE', 'PASAPORTE'), ('PPT', 'PPT')], default='CEDULA', verbose_name='Tipo Documento'),
        ),
    ]
