# Generated by Django 4.2.3 on 2023-07-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_resultatentrenament_entrenament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metrica',
            name='descripcio',
            field=models.CharField(max_length=1000, null=True, verbose_name='Descripcio'),
        ),
        migrations.AlterField(
            model_name='metrica',
            name='limits',
            field=models.CharField(max_length=1000, null=True, verbose_name='Límits'),
        ),
    ]
