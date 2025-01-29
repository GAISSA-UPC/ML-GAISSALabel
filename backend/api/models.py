from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from solo.models import SingletonModel

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
class OptimizationTechnique(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Optimization Technique'))

    class Meta:
        verbose_name = _('Optimization Technique')
        verbose_name_plural = _('Optimization Techniques')

    def __str__(self):
        return self.name
    
class TechniqueParameter(models.Model):
    id = models.AutoField(primary_key=True)
    optimization_technique = models.ForeignKey(OptimizationTechnique, related_name='technique_parameters', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('Parameter Name'), null=False, blank=False)

    class Meta:
        verbose_name = _('Technique Parameter')
        verbose_name_plural = _('Technique Parameters')
        unique_together = ('optimization_technique', 'name')

    def __str__(self):
        return f"{self.optimization_technique.name} - {self.name}"

class ROIAnalysis(models.Model):
    model = models.ForeignKey(Model, related_name='roi_analyses', on_delete=models.CASCADE, verbose_name=_('Model'))
    optimization_technique = models.ForeignKey(OptimizationTechnique, on_delete=models.PROTECT, null=False, blank=False, verbose_name=_('Optimization Technique'))
    technique_parameter = models.ForeignKey(TechniqueParameter, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Technique Parameter'))
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Registration Date'))
    country = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Country of Deployment'))

    class Meta:
        verbose_name = _('ROI Analysis')
        verbose_name_plural = _('ROI Analyses')

    def clean(self):
        from django.core.exceptions import ValidationError
        metrics = self.roi_cost_metrics.all()
        types_found = {m.type for m in metrics}
        required_types = {'optimization', 'original', 'new'}

        if len(metrics) != 3 or types_found != required_types:
            raise ValidationError(_('Each ROIAnalysis must have exactly 3 ROICostMetrics, one of each type (optimization, original, new).'))

    def __str__(self):
        return f"ROI Analysis {self.id} - {self.model.nom}"
    
class ROICostMetrics(models.Model):
    roi_analysis = models.ForeignKey(ROIAnalysis, related_name='roi_cost_metrics', on_delete=models.CASCADE, verbose_name=_('ROI Analysis'))
    type = models.CharField(
        max_length=50,
        choices=[
            ('optimization', 'OptimizationCosts'),
            ('original', 'OriginalInferenceCosts'),
            ('new', 'NewInferenceCosts')
        ],
        null=False,
        blank=False,
        verbose_name=_('Cost Type')
    )
    total_packs = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name=_('Total Packs'))
    cost_per_pack = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name=_('Cost per Pack'))
    taxes = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False, verbose_name=_('Taxes'))
    num_inferences = models.IntegerField(null=True, blank=True, verbose_name=_('Number of Inferences'))

    class Meta:
        verbose_name = _('ROI Cost Metrics')
        verbose_name_plural = _('ROI Cost Metrics')

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.type != 'optimization' and self.num_inferences is None:
            raise ValidationError(_('num_inferences is required for OriginalInferenceCosts or NewInferenceCosts.'))

    def __str__(self):
        return f"{self.name} - {self.roi_analysis}"

class Configuracio(SingletonModel):
    ultimaSincronitzacio = models.DateTimeField(verbose_name=_('Última sincronització'))

    class Meta:
        verbose_name_plural = _('Configuracions')