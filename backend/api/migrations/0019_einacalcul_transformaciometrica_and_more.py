# Generated by Django 4.2.3 on 2023-11-13 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_valorinfoinferencia_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='EinaCalcul',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Identificador')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('descripcio', models.CharField(max_length=1000, verbose_name='Descripció')),
            ],
            options={
                'verbose_name_plural': 'Eines càlcul',
            },
        ),
        migrations.CreateModel(
            name='TransformacioMetrica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=100, verbose_name='Valor')),
                ('eina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformacionsMetriques', to='api.einacalcul', verbose_name='Eina càlcul')),
                ('metrica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformacions', to='api.metrica', verbose_name='Mètrica')),
            ],
            options={
                'verbose_name_plural': 'Transformació Mètriques',
            },
        ),
        migrations.CreateModel(
            name='TransformacioInformacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=100, verbose_name='Valor')),
                ('eina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformacionsInformacions', to='api.einacalcul', verbose_name='Eina càlcul')),
                ('informacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transformacions', to='api.infoaddicional', verbose_name='Informació addicional')),
            ],
            options={
                'verbose_name_plural': 'Transformació Informacions',
            },
        ),
    ]