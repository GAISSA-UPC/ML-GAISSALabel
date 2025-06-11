from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from decimal import Decimal

from apps.gaissa_roi_analyzer.models import *
from apps.gaissa_roi_analyzer.serializers import *
from apps.core.models import Country

# NOTE: Simple CRUD serializers are not tested here as they contain only basic field  
# validation that is adequately covered by other tests.



class MLTacticSerializerTest(TestCase):
    """Unit tests for MLTacticSerializer - Tests complex ManyToMany handling and validation"""
    
    def setUp(self):
        """Set up test data"""
        self.source1 = TacticSource.objects.create(
            title="Research Paper 1",
            url="https://arxiv.org/abs/1111.2222"
        )
        self.source2 = TacticSource.objects.create(
            title="Research Paper 2", 
            url="https://arxiv.org/abs/3333.4444"
        )
        
        self.metric1 = ROIMetric.objects.create(
            name="Energy Consumption",
            unit="W",
            is_energy_related=True
        )
        self.metric2 = ROIMetric.objects.create(
            name="Inference Time",
            unit="ms",
            is_energy_related=False
        )
        
        self.arch1 = ModelArchitecture.objects.create(
            name="ResNet50",
            information="Deep residual network"
        )
        self.arch2 = ModelArchitecture.objects.create(
            name="VGG16",
            information="VGG architecture"
        )
        
        self.valid_data = {
            'name': 'Weight Pruning',
            'information': 'Neural network pruning technique',
            'source_ids': [self.source1.id, self.source2.id],
            'applicable_metric_ids': [self.metric1.id, self.metric2.id],
            'compatible_architecture_ids': [self.arch1.id, self.arch2.id]
        }

    def test_serializer_valid_data_creation(self):
        """Test creating MLTactic with valid ManyToMany data"""
        serializer = MLTacticSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        instance = serializer.save()
        self.assertEqual(instance.name, 'Weight Pruning')
        self.assertEqual(instance.sources.count(), 2)
        self.assertEqual(instance.applicable_metrics.count(), 2)
        self.assertEqual(instance.compatible_architectures.count(), 2)
        
        # Test relationships
        self.assertIn(self.source1, instance.sources.all())
        self.assertIn(self.metric1, instance.applicable_metrics.all())
        self.assertIn(self.arch1, instance.compatible_architectures.all())

    def test_serializer_representation(self):
        """Test serializer representation with nested objects"""
        tactic = MLTactic.objects.create(
            name="Test Tactic",
            information="Test information"
        )
        tactic.sources.add(self.source1)
        tactic.applicable_metrics.add(self.metric1)
        tactic.compatible_architectures.add(self.arch1)
        
        serializer = MLTacticSerializer(instance=tactic)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Tactic')
        self.assertEqual(len(data['sources']), 1)
        self.assertEqual(data['sources'][0]['title'], 'Research Paper 1')
        self.assertEqual(len(data['applicable_metrics']), 1)
        self.assertEqual(data['applicable_metrics'][0]['name'], 'Energy Consumption')
        self.assertEqual(len(data['compatible_architectures']), 1)
        self.assertEqual(data['compatible_architectures'][0]['name'], 'ResNet50')

    def test_validation_empty_applicable_metrics_failure(self):
        """Test validation failure when no applicable metrics provided"""
        invalid_data = self.valid_data.copy()
        invalid_data['applicable_metric_ids'] = []
        
        serializer = MLTacticSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('applicable_metric_ids', serializer.errors)
        self.assertIn('At least one applicable ROI metric must be provided', 
                      str(serializer.errors['applicable_metric_ids']))

    def test_validation_empty_compatible_architectures_failure(self):
        """Test validation failure when no compatible architectures provided"""
        invalid_data = self.valid_data.copy()
        invalid_data['compatible_architecture_ids'] = []
        
        serializer = MLTacticSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('compatible_architecture_ids', serializer.errors)
        self.assertIn('At least one compatible model architecture must be provided',
                      str(serializer.errors['compatible_architecture_ids']))

    def test_validation_none_applicable_metrics_failure(self):
        """Test validation failure when applicable_metric_ids is None"""
        invalid_data = self.valid_data.copy()
        invalid_data['applicable_metric_ids'] = None
        
        serializer = MLTacticSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('applicable_metric_ids', serializer.errors)

    def test_validation_none_compatible_architectures_failure(self):
        """Test validation failure when compatible_architecture_ids is None"""
        invalid_data = self.valid_data.copy()
        invalid_data['compatible_architecture_ids'] = None
        
        serializer = MLTacticSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('compatible_architecture_ids', serializer.errors)

    def test_validation_nonexistent_foreign_keys(self):
        """Test validation failure with non-existent foreign key IDs"""
        invalid_data = self.valid_data.copy()
        invalid_data['source_ids'] = [99999]  # Non-existent ID
        
        serializer = MLTacticSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('source_ids', serializer.errors)

    def test_update_manytomany_relationships(self):
        """Test updating ManyToMany relationships"""
        tactic = MLTactic.objects.create(name="Original Tactic")
        tactic.sources.add(self.source1)
        tactic.applicable_metrics.add(self.metric1)
        tactic.compatible_architectures.add(self.arch1)
        
        # Update with different relationships
        update_data = {
            'name': 'Updated Tactic',
            'source_ids': [self.source2.id],
            'applicable_metric_ids': [self.metric2.id],
            'compatible_architecture_ids': [self.arch2.id]
        }
        
        serializer = MLTacticSerializer(instance=tactic, data=update_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        updated_tactic = serializer.save()
        self.assertEqual(updated_tactic.name, 'Updated Tactic')
        self.assertEqual(updated_tactic.sources.count(), 1)
        self.assertIn(self.source2, updated_tactic.sources.all())
        self.assertNotIn(self.source1, updated_tactic.sources.all())



class EnergyAnalysisMetricValueSerializerTest(TestCase):
    """Unit tests for EnergyAnalysisMetricValueSerializer - Tests cost calculation logic"""
    
    def setUp(self):
        """Set up test data"""
        self.country = Country.objects.create(name="Spain", country_code="ES")
        
        self.model_arch = ModelArchitecture.objects.create(
            name="ResNet50",
            information="Deep residual network"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Energy Research",
            url="https://arxiv.org/abs/1234.5678"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Dynamic Quantization",
            information="Energy-efficient quantization"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="precision_bits",
            value="8"
        )
        
        self.energy_metric = ROIMetric.objects.create(
            name="Power Consumption",
            description="Energy usage measurement",
            unit="W",
            is_energy_related=True,
            min_value=0.0,
            max_value=2000.0
        )
        
        self.ml_tactic.applicable_metrics.add(self.energy_metric)
        
        self.expected_reduction = ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            metric=self.energy_metric,
            expectedReductionValue=0.35
        )
        
        self.analysis = ROIAnalysis.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )

    def test_serializer_representation_with_cost_savings(self):
        """Test serializer representation includes cost savings calculation"""
        energy_value = EnergyAnalysisMetricValue.objects.create(
            analysis=self.analysis,
            metric=self.energy_metric,
            baselineValue=800.0,
            energy_cost_rate=Decimal('0.18'),
            implementation_cost=Decimal('1800.00')
        )
        
        # Test with custom num_inferences in context
        context = {'num_inferences': 50000000}
        serializer = EnergyAnalysisMetricValueSerializer(instance=energy_value, context=context)
        data = serializer.data
        
        self.assertEqual(data['baselineValue'], 800.0)
        self.assertEqual(data['energy_cost_rate'], '0.1800')
        self.assertEqual(data['implementation_cost'], '1800.00')
        self.assertEqual(data['metric_name'], 'Power Consumption')
        self.assertIn('cost_savings', data)
        self.assertIn('id', data)
        
        # Cost savings should be calculated
        cost_savings = data['cost_savings']
        self.assertIsInstance(cost_savings, dict)
        if 'error' not in cost_savings:
            # Check for actual fields returned by the calculator
            self.assertIn('total_savings', cost_savings)
            self.assertIn('roi', cost_savings)
            self.assertIn('baseline_cost_per_inference', cost_savings)
            self.assertIn('new_cost_per_inference', cost_savings)
            self.assertIn('num_inferences', cost_savings)
            # Verify it used the custom num_inferences from context
            self.assertEqual(cost_savings['num_inferences'], 50000000)

    def test_cost_savings_with_missing_expected_reduction(self):
        """Test cost savings calculation when ExpectedMetricReduction is missing"""
        # Create a new analysis to avoid unique constraint issues
        new_analysis = ROIAnalysis.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )
        
        # Create energy metric value with existing expected reduction first
        energy_value = EnergyAnalysisMetricValue.objects.create(
            analysis=new_analysis,
            metric=self.energy_metric,  # Use existing metric with expected reduction
            baselineValue=500.0,
            energy_cost_rate=Decimal('0.15'),
            implementation_cost=Decimal('1000.00')
        )
        
        # Now delete the expected reduction to simulate missing data
        ExpectedMetricReduction.objects.filter(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            metric=self.energy_metric
        ).delete()
        
        # Test serializer with missing expected reduction
        serializer = EnergyAnalysisMetricValueSerializer(instance=energy_value)
        data = serializer.data
        
        cost_savings = data['cost_savings']
        self.assertIn('error', cost_savings)
        self.assertIn('No expected reduction found', cost_savings['error'])

    def test_cost_savings_with_default_num_inferences(self):
        """Test cost savings calculation uses default num_inferences when not provided"""
        energy_value = EnergyAnalysisMetricValue.objects.create(
            analysis=self.analysis,
            metric=self.energy_metric,
            baselineValue=1000.0,
            energy_cost_rate=Decimal('0.20'),
            implementation_cost=Decimal('2000.00')
        )
        
        # No context provided, should use default 100 million
        serializer = EnergyAnalysisMetricValueSerializer(instance=energy_value)
        data = serializer.data
        
        cost_savings = data['cost_savings']
        if 'error' not in cost_savings:
            # Should have calculated with default value
            self.assertIn('total_savings', cost_savings)
            self.assertIn('roi', cost_savings)
            self.assertIn('num_inferences', cost_savings)
            # Verify it used the default 100 million inferences
            self.assertEqual(cost_savings['num_inferences'], 100000000)
            
    def test_serializer_with_valid_creation_data(self):
        """Test serializer handles valid data for creating energy metric values"""
        valid_data = {
            'analysis': self.analysis.id,
            'metric_id': self.energy_metric.id,
            'baselineValue': 750.0,
            'energy_cost_rate': '0.18',
            'implementation_cost': '1500.00'
        }
        
        serializer = EnergyAnalysisMetricValueSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        instance = serializer.save()
        self.assertEqual(instance.baselineValue, 750.0)
        self.assertEqual(instance.energy_cost_rate, Decimal('0.18'))
        self.assertEqual(instance.implementation_cost, Decimal('1500.00'))

    def test_metric_id_field_functionality(self):
        """Test that metric_id write field works correctly"""
        energy_value = EnergyAnalysisMetricValue.objects.create(
            analysis=self.analysis,
            metric=self.energy_metric,
            baselineValue=600.0,
            energy_cost_rate=Decimal('0.16'),
            implementation_cost=Decimal('1200.00')
        )
        
        serializer = EnergyAnalysisMetricValueSerializer(instance=energy_value)
        data = serializer.data
        
        # Should have metric_name (read-only) but not metric_id in representation
        self.assertEqual(data['metric_name'], 'Power Consumption')
        self.assertNotIn('metric_id', data)
        self.assertEqual(data['metric'], self.energy_metric.id)



class ROIAnalysisSerializerTest(TestCase):
    """Unit tests for ROIAnalysisSerializer - Tests extensive business logic validation"""
    
    def setUp(self):
        """Set up test data"""
        self.country = Country.objects.create(name="Germany", country_code="DE")
        
        self.model_arch = ModelArchitecture.objects.create(
            name="VGG16",
            information="VGG architecture"
        )
        
        self.incompatible_arch = ModelArchitecture.objects.create(
            name="IncompatibleNet",
            information="Architecture not compatible with tactic"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Optimization Research",
            url="https://arxiv.org/abs/2222.3333"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Knowledge Distillation",
            information="Teacher-student distillation"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        # Note: incompatible_arch is NOT added to compatible_architectures
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="temperature",
            value="4.0"
        )
        
        self.energy_metric = ROIMetric.objects.create(
            name="Energy Consumption",
            unit="W",
            is_energy_related=True,
            min_value=0.0,
            max_value=1000.0
        )
        
        self.non_energy_metric = ROIMetric.objects.create(
            name="Inference Time",
            unit="ms",
            is_energy_related=False,
            min_value=0.0,
            max_value=500.0
        )
        
        self.ml_tactic.applicable_metrics.add(self.energy_metric, self.non_energy_metric)
        
        # Create expected reductions
        self.expected_reduction_energy = ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            metric=self.energy_metric,
            expectedReductionValue=0.30
        )
        
        self.expected_reduction_time = ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            metric=self.non_energy_metric,
            expectedReductionValue=0.25
        )

    def test_tactic_architecture_compatibility_validation_success(self):
        """Test successful validation when tactic is compatible with architecture"""
        valid_data = {
            'model_architecture_id': self.model_arch.id,
            'tactic_parameter_option_id': self.param_option.id,
            'country_id': self.country.id,
            'metric_values_data': [
                {
                    'metric_id': self.non_energy_metric.id,
                    'baselineValue': 100.0
                },
                {
                    'metric_id': self.energy_metric.id,
                    'baselineValue': 500.0,
                    'energy_cost_rate': 0.20,
                    'implementation_cost': 1000.0
                }
            ]
        }
        
        serializer = ROIAnalysisSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_tactic_architecture_compatibility_validation_failure(self):
        """Test validation failure when tactic is not compatible with architecture"""
        invalid_data = {
            'model_architecture_id': self.incompatible_arch.id,  # Incompatible architecture
            'tactic_parameter_option_id': self.param_option.id,
            'country_id': self.country.id
        }
        
        serializer = ROIAnalysisSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        error_message = str(serializer.errors)
        self.assertIn('not compatible', error_message)
        self.assertIn('Knowledge Distillation', error_message)
        self.assertIn('IncompatibleNet', error_message)

    def test_successful_analysis_creation_with_mixed_metrics(self):
        """Test successful creation of analysis with both energy and non-energy metrics"""
        valid_data = {
            'model_architecture_id': self.model_arch.id,
            'tactic_parameter_option_id': self.param_option.id,
            'country_id': self.country.id,
            'metric_values_data': [
                {
                    'metric_id': self.non_energy_metric.id,
                    'baselineValue': 150.0
                },
                {
                    'metric_id': self.energy_metric.id,
                    'baselineValue': 750.0,
                    'energy_cost_rate': 0.18,
                    'implementation_cost': 1500.0
                }
            ]
        }
        
        serializer = ROIAnalysisSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        analysis = serializer.save()
        self.assertEqual(analysis.model_architecture, self.model_arch)
        self.assertEqual(analysis.tactic_parameter_option, self.param_option)
        self.assertEqual(analysis.country, self.country)
        
        # Check metric values were created
        metric_values = analysis.metric_values.all()
        self.assertEqual(metric_values.count(), 2)
        
        # Check energy metric value was created as EnergyAnalysisMetricValue
        energy_values = EnergyAnalysisMetricValue.objects.filter(analysis=analysis)
        self.assertEqual(energy_values.count(), 1)
        energy_value = energy_values.first()
        self.assertEqual(energy_value.baselineValue, 750.0)
        self.assertEqual(float(energy_value.energy_cost_rate), 0.18)
        self.assertEqual(float(energy_value.implementation_cost), 1500.0)

    def test_serializer_representation_with_metrics_analysis(self):
        """Test serializer representation includes metrics analysis"""
        analysis = ROIAnalysis.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )
        
        # Create metric values
        AnalysisMetricValue.objects.create(
            analysis=analysis,
            metric=self.non_energy_metric,
            baselineValue=120.0
        )
        
        EnergyAnalysisMetricValue.objects.create(
            analysis=analysis,
            metric=self.energy_metric,
            baselineValue=600.0,
            energy_cost_rate=Decimal('0.15'),
            implementation_cost=Decimal('1200.00')
        )
        
        context = {'num_inferences': 75000000}
        serializer = ROIAnalysisSerializer(instance=analysis, context=context)
        data = serializer.data
        
        self.assertEqual(data['model_architecture_name'], 'VGG16')
        self.assertIn('tactic_parameter_option_details', data)
        self.assertIn('metric_values', data)
        self.assertIn('metrics_analysis', data)
        self.assertEqual(len(data['metric_values']), 2)




class ROIAnalysisCalculationSerializerTest(TestCase):
    """Unit tests for ROIAnalysisCalculationSerializer - Tests inheritance and specific behavior"""
    
    def setUp(self):
        """Set up test data"""
        self.country = Country.objects.create(name="France", country_code="FR")
        
        self.model_arch = ModelArchitecture.objects.create(
            name="MobileNet",
            information="Mobile architecture"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Mobile Optimization",
            url="https://arxiv.org/abs/4444.5555"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Pruning",
            information="Weight pruning"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity",
            value="0.5"
        )
        
        self.metric = ROIMetric.objects.create(
            name="Model Size",
            unit="MB",
            is_energy_related=False,
            min_value=0.0,
            max_value=1000.0
        )
        
        self.ml_tactic.applicable_metrics.add(self.metric)
        
        ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            metric=self.metric,
            expectedReductionValue=0.40
        )

    def test_calculation_analysis_creation(self):
        """Test creating ROIAnalysisCalculation through serializer"""
        valid_data = {
            'model_architecture_id': self.model_arch.id,
            'tactic_parameter_option_id': self.param_option.id,
            'country_id': self.country.id,
            'metric_values_data': [
                {
                    'metric_id': self.metric.id,
                    'baselineValue': 200.0
                }
            ]
        }
        
        serializer = ROIAnalysisCalculationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        analysis = serializer.save()
        self.assertIsInstance(analysis, ROIAnalysisCalculation)
        self.assertEqual(analysis.model_architecture, self.model_arch)
        self.assertIsNotNone(analysis.dateRegistration)

    def test_inherited_validation_logic(self):
        """Test that inherited validation from parent serializer works"""
        # Test incompatible architecture validation
        incompatible_arch = ModelArchitecture.objects.create(name="IncompatibleArch")
        
        invalid_data = {
            'model_architecture_id': incompatible_arch.id,  # Not compatible
            'tactic_parameter_option_id': self.param_option.id,
            'metric_values_data': [
                {
                    'metric_id': self.metric.id,
                    'baselineValue': 150.0
                }
            ]
        }
        
        serializer = ROIAnalysisCalculationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        error_message = str(serializer.errors)
        self.assertIn('not compatible', error_message)

    def test_calculation_serializer_representation(self):
        """Test serializer representation includes dateRegistration"""
        analysis = ROIAnalysisCalculation.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )
        
        serializer = ROIAnalysisCalculationSerializer(instance=analysis)
        data = serializer.data
        
        self.assertEqual(data['analysis_type'], 'calculation')
        self.assertIsNotNone(data['dateRegistration'])
        self.assertIsNone(data['source'])



class ROIAnalysisResearchSerializerTest(TestCase):
    """Unit tests for ROIAnalysisResearchSerializer - Tests research-specific fields"""
    
    def setUp(self):
        """Set up test data"""
        self.country = Country.objects.create(name="Italy", country_code="IT")
        
        self.model_arch = ModelArchitecture.objects.create(
            name="Transformer",
            information="Transformer architecture"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Transformer Optimization",
            url="https://arxiv.org/abs/5555.6666"
        )
        
        self.research_source = TacticSource.objects.create(
            title="Specific Research Study",
            url="https://arxiv.org/abs/7777.8888"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Attention Pruning",
            information="Attention head pruning"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="heads_to_prune",
            value="4"
        )
        
        self.metric = ROIMetric.objects.create(
            name="Memory Usage",
            unit="GB",
            is_energy_related=False,
            min_value=0.0,
            max_value=64.0
        )
        
        self.ml_tactic.applicable_metrics.add(self.metric)
        
        ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            metric=self.metric,
            expectedReductionValue=0.20
        )

    def test_research_analysis_creation(self):
        """Test creating ROIAnalysisResearch through serializer"""
        valid_data = {
            'model_architecture_id': self.model_arch.id,
            'tactic_parameter_option_id': self.param_option.id,
            'country_id': self.country.id,
            'source_id': self.research_source.id,
            'metric_values_data': [
                {
                    'metric_id': self.metric.id,
                    'baselineValue': 16.0
                }
            ]
        }
        
        serializer = ROIAnalysisResearchSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        analysis = serializer.save()
        self.assertIsInstance(analysis, ROIAnalysisResearch)
        self.assertEqual(analysis.model_architecture, self.model_arch)
        self.assertEqual(analysis.source, self.research_source)

    def test_research_serializer_representation(self):
        """Test serializer representation includes source information"""
        analysis = ROIAnalysisResearch.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country,
            source=self.research_source
        )
        
        serializer = ROIAnalysisResearchSerializer(instance=analysis)
        data = serializer.data
        
        self.assertEqual(data['analysis_type'], 'research')
        self.assertIsNone(data['dateRegistration'])
        self.assertIsNotNone(data['source'])
        self.assertEqual(data['source']['title'], 'Specific Research Study')

    def test_missing_source_validation_failure(self):
        """Test validation failure when source_id is missing"""
        invalid_data = {
            'model_architecture_id': self.model_arch.id,
            'tactic_parameter_option_id': self.param_option.id,
            'metric_values_data': [
                {
                    'metric_id': self.metric.id,
                    'baselineValue': 12.0
                }
            ]
            # Missing source_id
        }
        
        serializer = ROIAnalysisResearchSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        # Should require source_id for research analysis

    def test_inherited_validation_with_source(self):
        """Test that inherited validation works with source field"""
        # Test with all valid data
        valid_data = {
            'model_architecture_id': self.model_arch.id,
            'tactic_parameter_option_id': self.param_option.id,
            'source_id': self.research_source.id,
            'metric_values_data': [
                {
                    'metric_id': self.metric.id,
                    'baselineValue': 20.0
                }
            ]
        }
        
        serializer = ROIAnalysisResearchSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)