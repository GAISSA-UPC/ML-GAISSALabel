# Generated by Django 4.2.3 on 2023-12-28 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_model_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultatentrenament',
            name='valor',
            field=models.FloatField(blank=True, null=True, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='resultatinferencia',
            name='valor',
            field=models.FloatField(blank=True, null=True, verbose_name='Valor'),
        ),
    ]
