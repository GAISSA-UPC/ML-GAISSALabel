# Generated by Django 4.2.3 on 2023-08-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_metrica_limits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='informacio',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Informació'),
        ),
    ]