# Generated by Django 4.2.21 on 2025-06-08 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='core_administrador', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Configuracio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gaissa_label_enabled', models.BooleanField(default=True, verbose_name='GAISSALabel Enabled')),
                ('gaissa_roi_analyzer_enabled', models.BooleanField(default=True, verbose_name='GAISSA ROI Analyzer Enabled')),
                ('ultimaSincronitzacio', models.DateTimeField(verbose_name='Last GAISSA Label Model Synchronization')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Country Name')),
                ('country_code', models.CharField(max_length=3, unique=True, verbose_name='Country Code')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CarbonIntensity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_year', models.PositiveIntegerField(verbose_name='Data Year')),
                ('carbon_intensity', models.FloatField(verbose_name='Carbon Intensity (kgCO2/kWh)')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carbon_intensities', to='core.country', verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Carbon Intensity',
                'verbose_name_plural': 'Carbon Intensities',
                'ordering': ['-data_year', 'country__name'],
                'unique_together': {('country', 'data_year')},
            },
        ),
    ]
