# Generated by Django 4.2.3 on 2023-07-20 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Identificador')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('informacio', models.CharField(max_length=1000, verbose_name='Informació')),
                ('dataCreacio', models.DateTimeField(auto_now_add=True, verbose_name='Data creació')),
            ],
        ),
    ]
