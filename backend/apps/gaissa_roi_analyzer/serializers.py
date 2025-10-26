from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    MLPipelineStage, ModelArchitecture, TacticSource, ROIMetric, MLTactic, TacticParameterOption,
    ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch,
    AnalysisMetricValue, EnergyAnalysisMetricValue, ExpectedMetricReduction
)
from apps.core.models import Country
from .calculators.roi_metrics_calculator import ROIMetricsCalculator


class MLPipelineStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLPipelineStage
        fields = '__all__'


class ModelArchitectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelArchitecture
        fields = '__all__'


class TacticSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacticSource
        fields = '__all__'


class ROIMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROIMetric
        fields = '__all__'


class MLTacticSerializer(serializers.ModelSerializer):
    pipeline_stage_name = serializers.CharField(source='pipeline_stage.get_name_display', read_only=True)
    sources = TacticSourceSerializer(many=True, read_only=True)
    source_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TacticSource.objects.all(), write_only=True, source='sources', required=True
    )
    applicable_metrics = ROIMetricSerializer(many=True, read_only=True)
    applicable_metric_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ROIMetric.objects.all(), write_only=True, source='applicable_metrics', required=True
    )
    compatible_architectures = ModelArchitectureSerializer(many=True, read_only=True)
    compatible_architecture_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ModelArchitecture.objects.all(), write_only=True, source='compatible_architectures', required=True
    )

    def validate_applicable_metric_ids(self, value):
        """Ensure at least one ROI metric is provided"""
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one applicable ROI metric must be provided.")
        return value
    
    def validate_compatible_architecture_ids(self, value):
        """Ensure at least one compatible architecture is provided"""
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one compatible model architecture must be provided.")
        return value

    class Meta:
        model = MLTactic
        fields = [
            'id', 'name', 'information', 'pipeline_stage', 'pipeline_stage_name',
            'sources', 'source_ids', 
            'applicable_metrics', 'applicable_metric_ids',
            'compatible_architectures', 'compatible_architecture_ids'
        ]


class TacticParameterOptionSerializer(serializers.ModelSerializer):
    tactic_name = serializers.CharField(source='tactic.name', read_only=True)
    tactic_id = serializers.PrimaryKeyRelatedField(
        queryset=MLTactic.objects.all(), write_only=True, source='tactic'
    )

    class Meta:
        model = TacticParameterOption
        fields = ['id', 'tactic', 'tactic_id', 'tactic_name', 'name', 'value']
        read_only_fields = ['tactic'] # tactic is set via tactic_id


class AnalysisMetricValueSerializer(serializers.ModelSerializer):
    metric_name = serializers.CharField(source='metric.name', read_only=True)
    metric_id = serializers.PrimaryKeyRelatedField(
        queryset=ROIMetric.objects.all(), write_only=True, source='metric'
    )

    class Meta:
        model = AnalysisMetricValue
        fields = ['id', 'analysis', 'metric', 'metric_id', 'metric_name', 'baselineValue']
        read_only_fields = ['metric'] # metric is set via metric_id


class EnergyAnalysisMetricValueSerializer(serializers.ModelSerializer):
    metric_name = serializers.CharField(source='metric.name', read_only=True)
    metric_id = serializers.PrimaryKeyRelatedField(
        queryset=ROIMetric.objects.all(), write_only=True, source='metric'
    )
    cost_savings = serializers.SerializerMethodField(read_only=True)
    implementation_cost = serializers.SerializerMethodField(read_only=True)
    energy_cost_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EnergyAnalysisMetricValue
        fields = ['id', 'analysis', 'metric', 'metric_id', 'metric_name', 'baselineValue', 
                 'energy_cost_rate', 'implementation_cost', 'cost_savings']
        read_only_fields = ['metric'] # metric is set via metric_id

    def get_implementation_cost(self, obj):
        """Format implementation_cost to remove trailing zeros"""
        return obj.implementation_cost.normalize()
    
    def get_energy_cost_rate(self, obj):
        """Format energy_cost_rate to remove trailing zeros"""
        return obj.energy_cost_rate.normalize()

    def get_cost_savings(self, obj):
        # Default calculation for 100 million inferences if not specified
        num_inferences = self.context.get('num_inferences', 100000000)
        
        try:
            expected_reduction = ExpectedMetricReduction.objects.get(
                model_architecture=obj.analysis.model_architecture,
                tactic_parameter_option=obj.analysis.tactic_parameter_option,
                metric=obj.metric
            )
            
            # Use the calculator to get cost savings
            calculator = ROIMetricsCalculator()
            return calculator.calculate_cost_savings(
                obj,
                expected_reduction.expectedReductionValue,
                num_inferences
            )
        except ExpectedMetricReduction.DoesNotExist:
            return {'error': f"No expected reduction found for this metric ({obj.metric.name})"}
        except Exception as e:
            return {'error': str(e)}


class ROIAnalysisSerializer(serializers.ModelSerializer):
    model_architecture_name = serializers.CharField(source='model_architecture.name', read_only=True)
    tactic_parameter_option_details = TacticParameterOptionSerializer(source='tactic_parameter_option', read_only=True)
    metric_values = AnalysisMetricValueSerializer(many=True, read_only=True)
    metrics_analysis = serializers.SerializerMethodField(read_only=True)
    analysis_type = serializers.SerializerMethodField(read_only=True)
    country = serializers.SerializerMethodField(read_only=True)
    
    # Fields from subclasses
    dateRegistration = serializers.SerializerMethodField(read_only=True)
    source = serializers.SerializerMethodField(read_only=True)

    # Writeable fields for relations
    model_architecture_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelArchitecture.objects.all(), write_only=True, source='model_architecture'
    )
    tactic_parameter_option_id = serializers.PrimaryKeyRelatedField(
        queryset=TacticParameterOption.objects.all(), write_only=True, source='tactic_parameter_option'
    )
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), write_only=True, source='country', required=False
    )
    # For creating metric values alongside analysis
    metric_values_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = ROIAnalysis
        fields = [
            'id', 'model_architecture', 'model_architecture_id', 'model_architecture_name',
            'tactic_parameter_option', 'tactic_parameter_option_id', 'tactic_parameter_option_details',
            'metric_values', 'metric_values_data', 'metrics_analysis', 'dateRegistration', 'country', 
            'country_id', 'source', 'analysis_type'
        ]
        read_only_fields = ['model_architecture', 'tactic_parameter_option', 'country']
    
    def get_metrics_analysis(self, obj):
        # Get the num_inferences from the context if available, otherwise use default
        num_inferences = self.context.get('num_inferences', 100000000)
        calculator = ROIMetricsCalculator()
        return calculator.calculate_metrics_for_analysis(obj.id, num_inferences)
    
    def get_dateRegistration(self, obj):
        if hasattr(obj, 'roianalysiscalculation'):
            return obj.roianalysiscalculation.dateRegistration
        return None
        
    def get_country(self, obj):
        country = obj.country
        return {
            'id': country.id,
            'name': country.name,
            'country_code': country.country_code
        } if country else None
        
    def get_source(self, obj):
        if hasattr(obj, 'roianalysisresearch'):
            source = obj.roianalysisresearch.source
            return {
                'id': source.id,
                'title': source.title,
                'url': source.url
            } if source else None
        return None
        
    def get_analysis_type(self, obj):
        """
        Return the analysis type as a string: 'calculation' or 'research'
        """
        if hasattr(obj, 'roianalysiscalculation'):
            return 'calculation'
        elif hasattr(obj, 'roianalysisresearch'):
            return 'research'
        return None

    def validate(self, data):
        """Check compatibility between the selected tactic and model architecture."""
        model_architecture = data.get('model_architecture')
        tactic_parameter_option = data.get('tactic_parameter_option')

        if model_architecture and tactic_parameter_option:
            tactic = tactic_parameter_option.tactic
            if not tactic.compatible_architectures.filter(pk=model_architecture.pk).exists():
                raise ValidationError(
                    _("The selected tactic '%(tactic)s' is not compatible with the model architecture '%(arch)s'.") % {
                        'tactic': tactic.name,
                        'arch': model_architecture.name
                    }
                )

        return data

    def _validate_metric_values_against_expected_reduction(self, metric_values_data, model_architecture, tactic_parameter_option):
        """Method to validate metric values against ExpectedMetricReduction."""
        if not metric_values_data:
            raise ValidationError("Missing Metrics data for validation.")

        if not model_architecture or not tactic_parameter_option:
            raise ValidationError("Missing Model Architecture or Tactic Parameter Option for validation.")

        metrics_to_create = []
        tactic = tactic_parameter_option.tactic
        
        # Get all the required metrics for this tactic
        required_metrics = tactic.applicable_metrics.all()
        provided_metric_ids = [int(metric_data.get('metric_id')) for metric_data in metric_values_data if metric_data.get('metric_id')]
        
        # Check if all required metrics are provided
        missing_metrics = []
        for required_metric in required_metrics:
            if required_metric.id not in provided_metric_ids:
                missing_metrics.append(required_metric.name)
        
        if missing_metrics:
            raise ValidationError(
                _("Missing required metrics for tactic '%(tactic)s': %(metrics)s") % {
                    'tactic': tactic.name,
                    'metrics': ", ".join(missing_metrics)
                }
            )
        
        for metric_data in metric_values_data:
            metric_id = metric_data.get('metric_id')
            baseline_value = metric_data.get('baselineValue')
            if metric_id is None or baseline_value is None:
                 raise ValidationError("Each entry in metric_values_data must include 'metric_id' and 'baselineValue'.")

            # Validate metric existence
            try:
                metric = ROIMetric.objects.get(pk=metric_id)
            except ROIMetric.DoesNotExist:
                raise ValidationError(f"ROIMetric with id {metric_id} does not exist.")
                
            # Constraint 3: Check if the metric is applicable for the tactic
            if not tactic.applicable_metrics.filter(pk=metric.pk).exists():
                raise ValidationError(
                    _("The metric '%(metric)s' is not applicable for the tactic '%(tactic)s'.") % {
                        'metric': metric.name,
                        'tactic': tactic.name
                    }
                )

            # Constraint 2: ExpectedMetricReduction existence check
            exists = ExpectedMetricReduction.objects.filter(
                model_architecture=model_architecture,
                tactic_parameter_option=tactic_parameter_option,
                metric=metric
            ).exists()
            if not exists:
                raise ValidationError(
                    f"No matching ExpectedMetricReduction found for the combination of "
                    f"Model Architecture '{model_architecture}', "
                    f"Tactic Parameter Option '{tactic_parameter_option}', and Metric '{metric}'."
                )
                
            # Constraint 5: Validate baseline value against min/max if set
            if metric.min_value is not None and baseline_value < metric.min_value:
                raise ValidationError(
                    _("The baseline value %(value)s for metric '%(metric)s' is below the minimum allowed value %(min)s.") % {
                        'value': baseline_value,
                        'metric': metric.name,
                        'min': metric.min_value
                    }
                )
                
            if metric.max_value is not None and baseline_value > metric.max_value:
                raise ValidationError(
                    _("The baseline value %(value)s for metric '%(metric)s' exceeds the maximum allowed value %(max)s.") % {
                        'value': baseline_value,
                        'metric': metric.name,
                        'max': metric.max_value
                    }
                )

            # Check if energy-related metrics have energy cost information
            if metric.is_energy_related:
                energy_cost_rate = metric_data.get('energy_cost_rate')
                implementation_cost = metric_data.get('implementation_cost')
                if energy_cost_rate is None or implementation_cost is None:
                    raise ValidationError(
                        f"Energy-related metric '{metric.name}' requires 'energy_cost_rate' and 'implementation_cost' values."
                    )
                metrics_to_create.append({
                    'metric': metric, 
                    'baselineValue': baseline_value,
                    'is_energy_related': True,
                    'energy_cost_rate': energy_cost_rate,
                    'implementation_cost': implementation_cost
                })
            else:
                metrics_to_create.append({'metric': metric, 'baselineValue': baseline_value, 'is_energy_related': False})
        return metrics_to_create

    def create(self, validated_data):
        metric_values_data = validated_data.pop('metric_values_data', [])
        model_architecture = validated_data.get('model_architecture')
        tactic_parameter_option = validated_data.get('tactic_parameter_option')

        # Validate metric values against expected reductions
        metrics_to_create = self._validate_metric_values_against_expected_reduction(
            metric_values_data, model_architecture, tactic_parameter_option
        )

        # If validation passed, create the analysis and then the metric values
        analysis = ROIAnalysis.objects.create(**validated_data)
        
        for metric_info in metrics_to_create:
            # Create the appropriate metric value type based on whether it's energy-related
            if metric_info['is_energy_related']:
                EnergyAnalysisMetricValue.objects.create(
                    analysis=analysis,
                    metric=metric_info['metric'],
                    baselineValue=metric_info['baselineValue'],
                    energy_cost_rate=metric_info['energy_cost_rate'],
                    implementation_cost=metric_info['implementation_cost']
                )
            else:
                AnalysisMetricValue.objects.create(
                    analysis=analysis,
                    metric=metric_info['metric'],
                    baselineValue=metric_info['baselineValue']
                )
        return analysis


class AnalysisListSerializer(serializers.ModelSerializer):
    """
    A simplified return serializer for ROI Analysis list views.
    """
    model_architecture_name = serializers.CharField(source='model_architecture.name', read_only=True)
    tactic_name = serializers.CharField(source='tactic_parameter_option.tactic.name', read_only=True)
    parameter_name = serializers.CharField(source='tactic_parameter_option.name', read_only=True)
    parameter_value = serializers.CharField(source='tactic_parameter_option.value', read_only=True)
    analysis_type = serializers.SerializerMethodField(read_only=True)
    country = serializers.SerializerMethodField(read_only=True)
    
    # Fields from subclasses
    dateRegistration = serializers.SerializerMethodField(read_only=True)
    source = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ROIAnalysis
        fields = [
            'id', 'model_architecture', 'model_architecture_name',
            'tactic_name', 'parameter_name', 'parameter_value',
            'dateRegistration', 'country', 'source', 'analysis_type'
        ]
    
    def get_dateRegistration(self, obj):
        if hasattr(obj, 'roianalysiscalculation'):
            return obj.roianalysiscalculation.dateRegistration
        return None
    
    def get_country(self, obj):
        country = obj.country
        return {
            'id': country.id,
            'name': country.name,
            'country_code': country.country_code
        } if country else None
        
    def get_analysis_type(self, obj):
        """
        Return the analysis type as a string: 'calculation' or 'research'
        """
        if hasattr(obj, 'roianalysiscalculation'):
            return 'calculation'
        elif hasattr(obj, 'roianalysisresearch'):
            return 'research'
        return None
        
    def get_source(self, obj):
        if hasattr(obj, 'roianalysisresearch'):
            source = obj.roianalysisresearch.source
            return {
                'id': source.id,
                'title': source.title
            } if source else None
        return None


class ROIAnalysisCalculationSerializer(ROIAnalysisSerializer):
    
    class Meta(ROIAnalysisSerializer.Meta):
        model = ROIAnalysisCalculation
        fields = ROIAnalysisSerializer.Meta.fields + ['dateRegistration']

    def create(self, validated_data):
        metric_values_data = validated_data.pop('metric_values_data', [])
        model_architecture = validated_data.get('model_architecture')
        tactic_parameter_option = validated_data.get('tactic_parameter_option')

        # Validate metric values against expected reductions
        metrics_to_create = self._validate_metric_values_against_expected_reduction(
            metric_values_data, model_architecture, tactic_parameter_option
        )

        # If validation passed, create the specific analysis type and then the metric values
        analysis = ROIAnalysisCalculation.objects.create(**validated_data)
        
        for metric_info in metrics_to_create:
            # Create the appropriate metric value type based on whether it's energy-related
            if metric_info['is_energy_related']:
                EnergyAnalysisMetricValue.objects.create(
                    analysis=analysis,
                    metric=metric_info['metric'],
                    baselineValue=metric_info['baselineValue'],
                    energy_cost_rate=metric_info['energy_cost_rate'],
                    implementation_cost=metric_info['implementation_cost']
                )
            else:
                AnalysisMetricValue.objects.create(
                    analysis=analysis,
                    metric=metric_info['metric'],
                    baselineValue=metric_info['baselineValue']
                )
        return analysis


class ROIAnalysisResearchSerializer(ROIAnalysisSerializer):
     source_id = serializers.PrimaryKeyRelatedField(
          queryset=TacticSource.objects.all(), write_only=True, source='source'
     )
     
     class Meta(ROIAnalysisSerializer.Meta):
        model = ROIAnalysisResearch
        fields = ROIAnalysisSerializer.Meta.fields + ['source', 'source_id']

     def create(self, validated_data):
        metric_values_data = validated_data.pop('metric_values_data', [])
        model_architecture = validated_data.get('model_architecture')
        tactic_parameter_option = validated_data.get('tactic_parameter_option')

        # Validate metric values against expected reductions
        metrics_to_create = self._validate_metric_values_against_expected_reduction(
            metric_values_data, model_architecture, tactic_parameter_option
        )

        # If validation passed, create the specific analysis type and then the metric values
        analysis = ROIAnalysisResearch.objects.create(**validated_data)
        
        for metric_info in metrics_to_create:
            # Create the appropriate metric value type based on whether it's energy-related
            if metric_info['is_energy_related']:
                EnergyAnalysisMetricValue.objects.create(
                    analysis=analysis,
                    metric=metric_info['metric'],
                    baselineValue=metric_info['baselineValue'],
                    energy_cost_rate=metric_info['energy_cost_rate'],
                    implementation_cost=metric_info['implementation_cost']
                )
            else:
                AnalysisMetricValue.objects.create(
                    analysis=analysis,
                    metric=metric_info['metric'],
                    baselineValue=metric_info['baselineValue']
                )
        return analysis


class ExpectedMetricReductionSerializer(serializers.ModelSerializer):
    model_architecture_name = serializers.CharField(source='model_architecture.name', read_only=True)
    tactic_parameter_option_details = TacticParameterOptionSerializer(source='tactic_parameter_option', read_only=True)
    metric_name = serializers.CharField(source='metric.name', read_only=True)

    # Writeable fields for relations
    model_architecture_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelArchitecture.objects.all(), write_only=True, source='model_architecture'
    )
    tactic_parameter_option_id = serializers.PrimaryKeyRelatedField(
        queryset=TacticParameterOption.objects.all(), write_only=True, source='tactic_parameter_option'
    )
    metric_id = serializers.PrimaryKeyRelatedField(
        queryset=ROIMetric.objects.all(), write_only=True, source='metric'
    )

    class Meta:
        model = ExpectedMetricReduction
        fields = [
            'id', 'model_architecture', 'model_architecture_id', 'model_architecture_name',
            'tactic_parameter_option', 'tactic_parameter_option_id', 'tactic_parameter_option_details',
            'metric', 'metric_id', 'metric_name', 'expectedReductionValue'
        ]
        read_only_fields = ['model_architecture', 'tactic_parameter_option', 'metric']
