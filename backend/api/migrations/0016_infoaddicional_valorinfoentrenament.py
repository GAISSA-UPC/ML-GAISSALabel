# Generated by Django 4.2.3 on 2023-10-25 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_inferencia_alter_resultatentrenament_entrenament_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoAddicional',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Identificador')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('fase', models.CharField(choices=[('T', 'Entrenament'), ('I', 'Inferència')], max_length=5, verbose_name='Fase')),
                ('descripcio', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Descripcio')),
                ('opcions', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Opcions')),
            ],
        ),
        migrations.CreateModel(
            name='ValorInfoEntrenament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=10000, verbose_name='Valor')),
                ('entrenament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informacionsEntrenament', to='api.entrenament', verbose_name='Entrenament')),
                ('infoAddicional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informacionsEntrenament', to='api.infoaddicional', verbose_name='Informació')),
            ],
        ),
    ]
