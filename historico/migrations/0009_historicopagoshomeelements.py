# Generated by Django 5.0.6 on 2025-01-10 21:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0033_delete_codeudor'),
        ('historico', '0008_historialpagos_conveniopago'),
        ('parametro', '0003_rename_convenioasociado_convenio'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoPagosHomeElements',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.IntegerField(verbose_name='Valor')),
                ('estadoRegistro', models.BooleanField(verbose_name='Estado')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('asociado', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='asociado.asociado')),
                ('formaPago', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='parametro.formapago')),
                ('userCreacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_creacion_HE', to=settings.AUTH_USER_MODEL)),
                ('userModificacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_modificacion_HE', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historial de Pagos Home Elements',
                'verbose_name_plural': 'Historial de Pagos Home Elements',
                'ordering': ['pk'],
            },
        ),
    ]
