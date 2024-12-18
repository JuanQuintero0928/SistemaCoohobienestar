# Generated by Django 5.0.6 on 2024-12-03 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asociado', '0021_repatriaciontitular_ciudadrepatriacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repatriaciontitular',
            name='ciudadRepatriacion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='repatriaciontitular',
            name='fechaRepatriacion',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='repatriaciontitular',
            name='fechaRetiro',
            field=models.DateField(blank=True, null=True),
        ),
    ]
