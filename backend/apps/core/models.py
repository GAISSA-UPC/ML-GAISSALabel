from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from solo.models import SingletonModel


class Administrador(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, 
                               related_name='core_administrador', verbose_name=_('User'))

    def __str__(self):
        return self.user.username


class Configuracio(SingletonModel):
    """
    Singleton configuration model for application-wide settings
    """
    gaissa_label_enabled = models.BooleanField(default=True, verbose_name=_('GAISSALabel Enabled'))
    gaissa_roi_analyzer_enabled = models.BooleanField(default=True, verbose_name=_('GAISSA ROI Analyzer Enabled'))
    ultimaSincronitzacio = models.DateTimeField(verbose_name=_('Last GAISSA Label Model Synchronization'))

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
        
    def __str__(self):
        return "Configuration Settings"

    def __str__(self):
        return 'Configuration'


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Country Name'))
    country_code = models.CharField(max_length=5, unique=True, verbose_name=_('Country Code'))
    
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name']
        
    def __str__(self):
        return self.name


class CarbonIntensity(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='carbon_intensities', verbose_name=_('Country'))
    data_year = models.PositiveIntegerField(verbose_name=_('Data Year'))
    carbon_intensity = models.FloatField(verbose_name=_('Carbon Intensity (kgCO2/kWh)'))
    
    class Meta:
        verbose_name = _('Carbon Intensity')
        verbose_name_plural = _('Carbon Intensities')
        unique_together = ('country', 'data_year')
        ordering = ['-data_year', 'country__name']
        
    def __str__(self):
        return f"{self.country.name} - {self.data_year}: {self.carbon_intensity} kgCO2/kWh"
