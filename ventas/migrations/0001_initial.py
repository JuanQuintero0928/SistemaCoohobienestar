# Generated by Django 5.0.6 on 2024-12-10 20:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asociado', '0028_tarifaasociado_estadoadicional_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nit', models.CharField(max_length=18)),
                ('razonSocial', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoVenta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaVenta', models.DateField()),
                ('estadoRegistro', models.BooleanField(default=True)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True)),
                ('asociado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asociado.asociado')),
                ('userCreacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('referencia', models.CharField(max_length=20)),
                ('ean', models.CharField(max_length=13)),
                ('descripcion', models.CharField(max_length=200)),
                ('precio', models.IntegerField()),
                ('descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('inventario', models.BooleanField(default=False)),
                ('stock', models.IntegerField()),
                ('estadoRegistro', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.categoria')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('totalBruto', models.IntegerField()),
                ('descuento', models.IntegerField()),
                ('totalNeto', models.IntegerField()),
                ('historicoVenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.historicoventa')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.producto')),
            ],
        ),
    ]
