from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class ModelArchitecture(models.Model):
    """Model architecture for ML models (e.g., AlexNet, ResNet, etc.)"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Architecture Name'))
    information = models.TextField(null=True, blank=True, verbose_name=_('Information'))

    class Meta:
        verbose_name = _('Model Architecture')
        verbose_name_plural = _('Model Architectures')

    def clean(self):
        super().clean()
        if not self.name or self.name.strip() == '':
            raise ValidationError(_('Name field cannot be empty.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TacticSource(models.Model):
    """Source references for ML tactics (research papers, etc.)"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_('Source Title'))
    url = models.URLField(max_length=500, verbose_name=_('Source URL'))

    class Meta:
        verbose_name = _('Tactic Source')
        verbose_name_plural = _('Tactic Sources')

    def clean(self):
        super().clean()
        if not self.title or self.title.strip() == '':
            raise ValidationError(_('Title field cannot be empty.'))
        if not self.url or self.url.strip() == '':
            raise ValidationError(_('URL field cannot be empty.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ROIMetric(models.Model):
    """Metrics used for ROI analysis (energy consumption, inference time, etc.)"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Metric Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    unit = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Unit'))
    is_energy_related = models.BooleanField(default=False, verbose_name=_('Is Energy Related'))
    higher_is_better = models.BooleanField(default=False, verbose_name=_('Higher is better'))
    min_value = models.FloatField(null=True, blank=True, verbose_name=_('Minimum Value'))
    max_value = models.FloatField(null=True, blank=True, verbose_name=_('Maximum Value'))

    class Meta:
        verbose_name = _('ROI Metric')
        verbose_name_plural = _('ROI Metrics')

    def clean(self):
        super().clean()
        if not self.name or self.name.strip() == '':
            raise ValidationError(_('Name field cannot be empty.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MLTactic(models.Model):
    """ML optimization tactics (pruning, quantization, etc.)"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Tactic Name'))
    information = models.TextField(null=True, blank=True, verbose_name=_('Information'))
    sources = models.ManyToManyField(TacticSource, related_name='tactics', blank=False, verbose_name=_('Sources'))
    compatible_architectures = models.ManyToManyField(ModelArchitecture, related_name='compatible_tactics', blank=True, verbose_name=_('Compatible Architectures'))
    applicable_metrics = models.ManyToManyField(ROIMetric, related_name='applicable_tactics', blank=True, verbose_name=_('Applicable Metrics'))

    class Meta:
        verbose_name = _('ML Tactic')
        verbose_name_plural = _('ML Tactics')

    def clean(self):
        super().clean()
        if not self.name or self.name.strip() == '':
            raise ValidationError(_('Name field cannot be empty.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TacticParameterOption(models.Model):
    """Parameter options for ML tactics (e.g., sparsity levels for pruning)"""
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



class ExpectedMetricReduction(models.Model):
    """Expected metric reduction values for tactic-architecture-metric combinations"""
    id = models.AutoField(primary_key=True)
    model_architecture = models.ForeignKey(ModelArchitecture, on_delete=models.CASCADE, verbose_name=_('Model Architecture'))
    tactic_parameter_option = models.ForeignKey(TacticParameterOption, on_delete=models.CASCADE, verbose_name=_('Tactic Parameter Option'))
    metric = models.ForeignKey(ROIMetric, on_delete=models.CASCADE, verbose_name=_('ROI Metric'))
    expectedReductionValue = models.FloatField(verbose_name=_('Expected Reduction Value'))

    class Meta:
        verbose_name = _('Expected Metric Reduction')
        verbose_name_plural = _('Expected Metric Reductions')
        unique_together = ('model_architecture', 'tactic_parameter_option', 'metric')

    def __str__(self):
        return f"Reduction for {self.metric.name} on {self.model_architecture.name} with {self.tactic_parameter_option}"



class ROIAnalysis(models.Model):
    """Base class for ROI analyses"""
    id = models.AutoField(primary_key=True)
    model_architecture = models.ForeignKey(ModelArchitecture, related_name='roi_analyses', on_delete=models.PROTECT, verbose_name=_('Model Architecture'))
    tactic_parameter_option = models.ForeignKey(TacticParameterOption, related_name='roi_analyses', on_delete=models.PROTECT, verbose_name=_('Tactic Parameter Option'))
    country = models.ForeignKey('core.Country', on_delete=models.PROTECT, related_name='roi_analyses', verbose_name=_('Country of Deployment'), null=True)

    class Meta:
        verbose_name = _('ROI Analysis')
        verbose_name_plural = _('ROI Analyses')

    def clean(self):
        super().clean()
        # Constraint: Check compatibility between MLTactic and ModelArchitecture
        if self.model_architecture_id and self.tactic_parameter_option_id:
            try:
                tactic = self.tactic_parameter_option.tactic
                # Check if the model_architecture is in the tactic's compatible list
                if not tactic.compatible_architectures.filter(pk=self.model_architecture_id).exists():
                    raise ValidationError(
                        _("The selected tactic '%(tactic)s' is not compatible with the model architecture '%(arch)s'.") % {
                            'tactic': tactic.name,
                            'arch': self.model_architecture.name
                        }
                    )
            except MLTactic.DoesNotExist:
                # Should not happen due to ForeignKey
                pass
            except ModelArchitecture.DoesNotExist:
                # Should not happen due to ForeignKey
                pass
            
    def __str__(self):
        return f"ROI Analysis {self.id} for {self.model_architecture.name} with {self.tactic_parameter_option}"


class ROIAnalysisCalculation(ROIAnalysis):
    """ROI analysis based on calculations"""
    dateRegistration = models.DateTimeField(auto_now_add=True, verbose_name=_('Registration Date'))

    class Meta:
        verbose_name = _('ROI Analysis Calculation')
        verbose_name_plural = _('ROI Analysis Calculations')


class ROIAnalysisResearch(ROIAnalysis):
    """ROI analysis based on research papers"""
    source = models.ForeignKey(TacticSource, related_name='roi_analysis_researches', on_delete=models.PROTECT, verbose_name=_('Source'))

    class Meta:
        verbose_name = _('ROI Analysis Research')
        verbose_name_plural = _('ROI Analysis Researches')



class AnalysisMetricValue(models.Model):
    """Metric values for ROI analyses"""
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
        if self.analysis_id and self.metric_id:
            try:
                # Fetch related objects safely
                analysis = ROIAnalysis.objects.select_related('model_architecture', 'tactic_parameter_option').get(pk=self.analysis_id)
                metric = ROIMetric.objects.get(pk=self.metric_id)
                tactic = analysis.tactic_parameter_option.tactic
                
                # Constraint 3: Check if the metric is applicable for the tactic
                if not tactic.applicable_metrics.filter(pk=metric.pk).exists():
                    raise ValidationError(
                        _("The metric '%(metric)s' is not applicable for the tactic '%(tactic)s'.") % {
                            'metric': metric.name,
                            'tactic': tactic.name
                        }
                    )

                # Constraint 2: Ensure a corresponding ExpectedMetricReduction exists
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
                
                # Constraint 4: Ensure energy metrics use EnergyAnalysisMetricValue
                if metric.is_energy_related and self.__class__ == AnalysisMetricValue:
                    raise ValidationError(
                        _("Energy-related metrics must use EnergyAnalysisMetricValue instead of AnalysisMetricValue.")
                    )

                # Constraint 5: Validate baselineValue against min/max range
                if metric.min_value is not None and self.baselineValue < metric.min_value:
                    raise ValidationError(
                        _("The baseline value %(value)s for metric '%(metric)s' is below the minimum allowed value %(min)s.") % {
                            'value': self.baselineValue,
                            'metric': metric.name,
                            'min': metric.min_value
                        }
                    )
                    
                if metric.max_value is not None and self.baselineValue > metric.max_value:
                    raise ValidationError(
                        _("The baseline value %(value)s for metric '%(metric)s' exceeds the maximum allowed value %(max)s.") % {
                            'value': self.baselineValue,
                            'metric': metric.name,
                            'max': metric.max_value
                        }
                    )

            # These exceptions allow the creation of the object when creating the analysis
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


class EnergyAnalysisMetricValue(AnalysisMetricValue):
    """Specialized metric values for energy-related metrics"""
    energy_cost_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=_('Energy Cost Rate (€/kWh)'), help_text=_('The cost per kilowatt-hour of energy in €'))
    implementation_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Implementation Costs (€)'), help_text=_('Additional costs for implementing this energy optimization tactic in €'))

    class Meta:
        verbose_name = _('Energy Metric Analysis Value')
        verbose_name_plural = _('Energy Metric Analysis Values')

    def clean(self):
        super().clean()
        # Ensure this is only used with energy-related metrics
        if self.metric_id and not self.metric.is_energy_related:
            raise ValidationError(_("EnergyAnalysisMetricValue can only be used with energy-related metrics."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

