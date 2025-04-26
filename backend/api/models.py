from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from solo.models import SingletonModel
from django.core.exceptions import ValidationError

class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    autor = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Autor/a'))
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
    calcul = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Com es calcula'))
    recomanacions = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Recomanacions'))

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
    valor = models.FloatField(null=True, blank=True, verbose_name=_('Valor'))
    entrenament = models.ForeignKey(Entrenament, related_name='resultatsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Entrenament'))
    metrica = models.ForeignKey(Metrica, related_name='resultatsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))

class ResultatInferencia(models.Model):
    valor = models.FloatField(null=True, blank=True, verbose_name=_('Valor'))
    inferencia = models.ForeignKey(Inferencia, related_name='resultatsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Inferència'))
    metrica = models.ForeignKey(Metrica, related_name='resultatsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))

    class Meta:
        verbose_name_plural = _('Resultat Inferències')

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

class ValorInfoEntrenament(models.Model):
    valor = models.CharField(max_length=10000, null=False, blank=False, verbose_name=_('Valor'))
    entrenament = models.ForeignKey(Entrenament, related_name='informacionsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Entrenament'))
    infoAddicional = models.ForeignKey(InfoAddicional, related_name='informacionsEntrenament', null=False, on_delete=models.CASCADE, verbose_name=_('Informació'))

class ValorInfoInferencia(models.Model):
    valor = models.CharField(max_length=10000, null=False, blank=False, verbose_name=_('Valor'))
    inferencia = models.ForeignKey(Inferencia, related_name='informacionsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Inferència'))
    infoAddicional = models.ForeignKey(InfoAddicional, related_name='informacionsInferencia', null=False, on_delete=models.CASCADE, verbose_name=_('Informació'))

    class Meta:
        verbose_name_plural = _('Valor info inferències')

class EinaCalcul(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Identificador'))
    nom = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Nom'))
    descripcio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Descripció'))

    class Meta:
        verbose_name_plural = _('Eines càlcul')

class TransformacioMetrica(models.Model):
    valor = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Valor'))
    metrica = models.ForeignKey(Metrica, related_name='transformacions', null=False, on_delete=models.CASCADE, verbose_name=_('Mètrica'))
    eina = models.ForeignKey(EinaCalcul, related_name='transformacionsMetriques', null=False, on_delete=models.CASCADE, verbose_name=_('Eina càlcul'))

    class Meta:
        verbose_name_plural = _('Transformació Mètriques')

class TransformacioInformacio(models.Model):
    valor = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Valor'))
    informacio = models.ForeignKey(InfoAddicional, related_name='transformacions', null=False, on_delete=models.CASCADE, verbose_name=_('Informació addicional'))
    eina = models.ForeignKey(EinaCalcul, related_name='transformacionsInformacions', null=False, on_delete=models.CASCADE, verbose_name=_('Eina càlcul'))

    class Meta:
        verbose_name_plural = _('Transformació Informacions')

class Administrador(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name=_('User'))

# ROI Models

class ModelArchitecture(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Architecture Name'))
    information = models.TextField(null=True, blank=True, verbose_name=_('Information'))

    class Meta:
        verbose_name = _('Model Architecture')
        verbose_name_plural = _('Model Architectures')

    def __str__(self):
        return self.name

class TacticSource(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_('Source Title'))
    url = models.URLField(max_length=500, verbose_name=_('Source URL'))

    class Meta:
        verbose_name = _('Tactic Source')
        verbose_name_plural = _('Tactic Sources')

    def __str__(self):
        return self.title

class MLTactic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Tactic Name'))
    information = models.TextField(null=True, blank=True, verbose_name=_('Information'))
    sources = models.ManyToManyField(TacticSource, related_name='tactics', blank=False, verbose_name=_('Sources'))

    class Meta:
        verbose_name = _('ML Tactic')
        verbose_name_plural = _('ML Tactics')

    def __str__(self):
        return self.name

class TacticParameterOption(models.Model):
    id = models.AutoField(primary_key=True)
    tactic = models.ForeignKey(MLTactic, related_name='parameter_options', on_delete=models.CASCADE, verbose_name=_('Tactic'))
    name = models.CharField(max_length=255, verbose_name=_('Parameter Name'))
    value = models.CharField(max_length=255, verbose_name=_('Parameter Value'))

    class Meta:
        verbose_name = _('Tactic Parameter Option')
        verbose_name_plural = _('Tactic Parameter Options')
        unique_together = ('tactic', 'name', 'value')

    def __str__(self):
        return f"{self.tactic.name} - {self.name}: {self.value}"

class ROIAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    model_architecture = models.ForeignKey(ModelArchitecture, related_name='roi_analyses', on_delete=models.PROTECT, verbose_name=_('Model Architecture'))
    tactic_parameter_option = models.ForeignKey(TacticParameterOption, related_name='roi_analyses', on_delete=models.PROTECT, verbose_name=_('Tactic Parameter Option'))
    # Implicit link to MLTactic via TacticParameterOption

    class Meta:
        verbose_name = _('ROI Analysis')
        verbose_name_plural = _('ROI Analyses')

    def clean(self):
        # Constraint 1: Check compatibility between MLTactic and ModelArchitecture (to be done)
        pass

    def __str__(self):
        return f"ROI Analysis {self.id} for {self.model_architecture.name} with {self.tactic_parameter_option}"

# Inheritance for the analysis subtypes
class ROIAnalysisCalculation(ROIAnalysis):
    dateRegistration = models.DateTimeField(auto_now_add=True, verbose_name=_('Registration Date'))
    country = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Country of Deployment'))

    class Meta:
        verbose_name = _('ROI Analysis Calculation')
        verbose_name_plural = _('ROI Analysis Calculations')

class ROIAnalysisResearch(ROIAnalysis):
    source = models.ForeignKey(TacticSource, related_name='roi_analysis_researches', on_delete=models.PROTECT, verbose_name=_('Source'))

    class Meta:
        verbose_name = _('ROI Analysis Research')
        verbose_name_plural = _('ROI Analysis Researches')


class ROIMetric(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Metric Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    unit = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Unit'))

    class Meta:
        verbose_name = _('ROI Metric')
        verbose_name_plural = _('ROI Metrics')

    def __str__(self):
        return self.name

class AnalysisMetricValue(models.Model):
    id = models.AutoField(primary_key=True)
    analysis = models.ForeignKey(ROIAnalysis, related_name='metric_values', on_delete=models.CASCADE, verbose_name=_('ROI Analysis'))
    metric = models.ForeignKey(ROIMetric, related_name='analysis_values', on_delete=models.PROTECT, verbose_name=_('ROI Metric'))
    baselineValue = models.FloatField(verbose_name=_('Baseline Value'))

    class Meta:
        verbose_name = _('Analysis Metric Value')
        verbose_name_plural = _('Analysis Metric Values')
        unique_together = ('analysis', 'metric')

    def clean(self):
        super().clean()
        # Constraint: Ensure a corresponding ExpectedMetricReduction exists
        if self.analysis_id and self.metric_id:
            try:
                # Fetch related objects safely
                analysis = ROIAnalysis.objects.select_related('model_architecture', 'tactic_parameter_option').get(pk=self.analysis_id)
                metric = ROIMetric.objects.get(pk=self.metric_id)

                exists = ExpectedMetricReduction.objects.filter(
                    model_architecture=analysis.model_architecture,
                    tactic_parameter_option=analysis.tactic_parameter_option,
                    metric=metric
                ).exists()

                if not exists:
                    raise ValidationError(
                        _("No matching ExpectedMetricReduction found for the combination of "
                          "Model Architecture '%(arch)s', Tactic Parameter Option '%(tpo)s', and Metric '%(metric)s'.") % {
                            'arch': analysis.model_architecture,
                            'tpo': analysis.tactic_parameter_option,
                            'metric': metric
                        }
                    )
            # This exceptions allow the creation of the object when creating the analysis
            # This constraint will be checked in the serializer when the analysis is created
            except ROIAnalysis.DoesNotExist:
                # This might happen if the analysis object hasn't been saved yet.
                # The foreign key constraint itself will handle invalid analysis_id.
                pass
            except AttributeError:
                 # This might happen if analysis doesn't have the related objects yet (e.g., during creation before save)
                 # Let the serializer handle pre-creation validation.
                 pass

    def __str__(self):
        return f"{self.analysis} - {self.metric.name}: {self.baselineValue}"

class ExpectedMetricReduction(models.Model):
    id = models.AutoField(primary_key=True)
    model_architecture = models.ForeignKey(ModelArchitecture, on_delete=models.CASCADE, verbose_name=_('Model Architecture'))
    tactic_parameter_option = models.ForeignKey(TacticParameterOption, on_delete=models.CASCADE, verbose_name=_('Tactic Parameter Option'))
    metric = models.ForeignKey(ROIMetric, on_delete=models.CASCADE, verbose_name=_('ROI Metric'))
    expectedReductionValue = models.FloatField(verbose_name=_('Expected Reduction Value')) # Assuming percentage or absolute value

    class Meta:
        verbose_name = _('Expected Metric Reduction')
        verbose_name_plural = _('Expected Metric Reductions')
        unique_together = ('model_architecture', 'tactic_parameter_option', 'metric') # Constraint 2 implied here

    def __str__(self):
        return f"Reduction for {self.metric.name} on {self.model_architecture.name} with {self.tactic_parameter_option}"


# Configuracio model
class Configuracio(SingletonModel):
    ultimaSincronitzacio = models.DateTimeField(verbose_name=_('Última sincronització'))

    class Meta:
        verbose_name_plural = _('Configuracions')