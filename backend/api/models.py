from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models


class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    informacio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Informació'))
    dataCreacio = models.DateTimeField(auto_now_add=True, verbose_name=_('Data creació'))


class Entrenament(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    dataRegistre = models.DateTimeField(auto_now_add=True, verbose_name=_('Data registre'))
    model = models.ForeignKey(Model, related_name='entrenaments', null=False, on_delete=models.CASCADE, verbose_name=_('Model'))


class Inferencia(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    dataRegistre = models.DateTimeField(auto_now_add=True, verbose_name=_('Data registre'))
    model = models.ForeignKey(Model, related_name='inferencies', null=False, on_delete=models.CASCADE, verbose_name=_('Model'))

    class Meta:
        verbose_name_plural = _('Inferències')


class Metrica(models.Model):
    TRAIN = 'T'
    INF = 'I'
    TFASE = (
        (TRAIN, _('Entrenament')),
        (INF, _('Inferència'))
    )

    POSITIVA = 'P'
    NEGATIVA = 'N'
    TINFLUENCIA = (
        (POSITIVA, _('Positiva')),
        (NEGATIVA, _('Negativa'))
    )

    id = models.CharField(primary_key=True, max_length=100, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    fase = models.CharField(choices=TFASE, null=False, blank=False, max_length=5, verbose_name=_('Fase'))
    pes = models.FloatField(null=True, blank=True, verbose_name=_('Pes'))
    unitat = models.CharField(max_length=5, null=True, blank=True, verbose_name=_('Unitat'))
    influencia = models.CharField(choices=TINFLUENCIA, null=False, blank=False, max_length=5, verbose_name=_('Influència'))
    descripcio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Descripcio'))

    class Meta:
        verbose_name_plural = _('Mètriques')


class Qualificacio(models.Model):
    id = models.CharField(primary_key=True, max_length=100, verbose_name=_('Identificador'))
    # Color codificat en hexadecimal ('#' + 6 valors hexa)
    color = models.CharField(max_length=7, validators=[RegexValidator(r'^#([A-Fa-f0-9]{6})$')], verbose_name=_('Color'))
    ordre = models.IntegerField(null=False, blank=False, verbose_name=_('Ordre'))

    class Meta:
        verbose_name_plural = _('Qualificacions')


class Interval(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    metrica = models.ForeignKey(Metrica, related_name='intervals', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))
    qualificacio = models.ForeignKey(Qualificacio, related_name='intervals', null=False, on_delete=models.CASCADE, verbose_name=_('Qualificació'))
    limitSuperior = models.FloatField(null=False, blank=False, verbose_name=_('Límit superior'))
    limitInferior = models.FloatField(null=False, blank=False, verbose_name=_('Límit inferior'))
    imatge = models.ImageField(null=True, blank=True, verbose_name=_('Imatge'))


class ResultatEntrenament(models.Model):
    valor = models.FloatField(null=False, blank=False, verbose_name=_('Valor'))
    entrenament = models.ForeignKey(Entrenament, related_name='resultatsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Entrenament'))
    metrica = models.ForeignKey(Metrica, related_name='resultatsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))


class ResultatInferencia(models.Model):
    valor = models.FloatField(null=False, blank=False, verbose_name=_('Valor'))
    inferencia = models.ForeignKey(Inferencia, related_name='resultatsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Inferència'))
    metrica = models.ForeignKey(Metrica, related_name='resultatsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))

    class Meta:
        verbose_name_plural = _('Resultat Inferències')
