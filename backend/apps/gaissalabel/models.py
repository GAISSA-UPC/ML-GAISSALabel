from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models


class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    autor = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Autor/a'))
    informacio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Informació'))
    dataCreacio = models.DateTimeField(auto_now_add=True, verbose_name=_('Data creació'))

    def __str__(self):
        return self.nom


class Entrenament(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    dataRegistre = models.DateTimeField(auto_now_add=True, verbose_name=_('Data registre'))
    model = models.ForeignKey(Model, related_name='entrenaments', null=False, on_delete=models.CASCADE, verbose_name=_('Model'))

    def __str__(self):
        return f'Entrenament {self.id} - {self.model.nom}'


class Inferencia(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    dataRegistre = models.DateTimeField(auto_now_add=True, verbose_name=_('Data registre'))
    model = models.ForeignKey(Model, related_name='inferencies', null=False, on_delete=models.CASCADE, verbose_name=_('Model'))

    class Meta:
        verbose_name_plural = _('Inferències')

    def __str__(self):
        return f'Inferencia {self.id} - {self.model.nom}'


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
    calcul = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Com es calcula'))
    recomanacions = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Recomanacions'))

    class Meta:
        verbose_name_plural = _('Mètriques')

    def __str__(self):
        return self.nom


class Qualificacio(models.Model):
    id = models.CharField(primary_key=True, max_length=100, verbose_name=_('Identificador'))
    # Color codificat en hexadecimal ('#' + 6 valors hexa)
    color = models.CharField(max_length=7, validators=[RegexValidator(r'^#([A-Fa-f0-9]{6})$')], verbose_name=_('Color'))
    ordre = models.IntegerField(null=False, blank=False, verbose_name=_('Ordre'))

    class Meta:
        verbose_name_plural = _('Qualificacions')

    def __str__(self):
        return self.id


class Interval(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    metrica = models.ForeignKey(Metrica, related_name='intervals', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))
    qualificacio = models.ForeignKey(Qualificacio, related_name='intervals', null=False, on_delete=models.CASCADE, verbose_name=_('Qualificació'))
    limitSuperior = models.FloatField(null=False, blank=False, verbose_name=_('Límit superior'))
    limitInferior = models.FloatField(null=False, blank=False, verbose_name=_('Límit inferior'))
    imatge = models.ImageField(null=True, blank=True, verbose_name=_('Imatge'))

    def __str__(self):
        return f'{self.metrica.nom} - {self.qualificacio.id}'


class ResultatEntrenament(models.Model):
    valor = models.FloatField(null=True, blank=True, verbose_name=_('Valor'))
    entrenament = models.ForeignKey(Entrenament, related_name='resultatsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Entrenament'))
    metrica = models.ForeignKey(Metrica, related_name='resultatsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))

    def __str__(self):
        return f'{self.entrenament} - {self.metrica.nom}: {self.valor}'


class ResultatInferencia(models.Model):
    valor = models.FloatField(null=True, blank=True, verbose_name=_('Valor'))
    inferencia = models.ForeignKey(Inferencia, related_name='resultatsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Inferència'))
    metrica = models.ForeignKey(Metrica, related_name='resultatsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))

    class Meta:
        verbose_name_plural = _('Resultat Inferències')

    def __str__(self):
        return f'{self.inferencia} - {self.metrica.nom}: {self.valor}'


class InfoAddicional(models.Model):
    TRAIN = 'T'
    INF = 'I'
    TFASE = (
        (TRAIN, _('Entrenament')),
        (INF, _('Inferència'))
    )

    id = models.CharField(primary_key=True, max_length=100, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    fase = models.CharField(choices=TFASE, null=False, blank=False, max_length=5, verbose_name=_('Fase'))
    descripcio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Descripcio'))
    # Opcions possibles (separades per ';'). Si null vol dir que és camp lliure
    opcions = models.CharField(max_length=10000, null=True, blank=True, verbose_name=_('Opcions'))

    def __str__(self):
        return self.nom


class ValorInfoEntrenament(models.Model):
    valor = models.CharField(max_length=10000, null=False, blank=False, verbose_name=_('Valor'))
    entrenament = models.ForeignKey(Entrenament, related_name='informacionsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Entrenament'))
    infoAddicional = models.ForeignKey(InfoAddicional, related_name='informacionsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Informació'))

    def __str__(self):
        return f'{self.entrenament} - {self.infoAddicional.nom}: {self.valor}'


class ValorInfoInferencia(models.Model):
    valor = models.CharField(max_length=10000, null=False, blank=False, verbose_name=_('Valor'))
    inferencia = models.ForeignKey(Inferencia, related_name='informacionsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Inferència'))
    infoAddicional = models.ForeignKey(InfoAddicional, related_name='informacionsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Informació'))

    class Meta:
        verbose_name_plural = _('Valor info inferències')

    def __str__(self):
        return f'{self.inferencia} - {self.infoAddicional.nom}: {self.valor}'


class EinaCalcul(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    descripcio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Descripció'))

    class Meta:
        verbose_name_plural = _('Eines càlcul')

    def __str__(self):
        return self.nom


class TransformacioMetrica(models.Model):
    valor = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Valor'))
    metrica = models.ForeignKey(Metrica, related_name='transformacions', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))
    eina = models.ForeignKey(EinaCalcul, related_name='transformacionsMetriques', null=False, on_delete=models.CASCADE, verbose_name=_('Eina càlcul'))

    class Meta:
        verbose_name_plural = _('Transformació Mètriques')

    def __str__(self):
        return f'{self.metrica.nom} - {self.eina.nom}: {self.valor}'


class TransformacioInformacio(models.Model):
    valor = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Valor'))
    informacio = models.ForeignKey(InfoAddicional, related_name='transformacions', null=False, on_delete=models.CASCADE, verbose_name=_('Informació addicional'))
    eina = models.ForeignKey(EinaCalcul, related_name='transformacionsInformacions', null=False, on_delete=models.CASCADE, verbose_name=_('Eina càlcul'))

    class Meta:
        verbose_name_plural = _('Transformació Informacions')

    def __str__(self):
        return f'{self.informacio.nom} - {self.eina.nom}: {self.valor}'
