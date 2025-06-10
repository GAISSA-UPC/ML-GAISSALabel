from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.gaissa_roi_analyzer.models import *


class ModelArchitectureTest(TestCase):
    """Unit tests for ModelArchitecture model"""
    
    def setUp(self):
        """Set up test data"""
        self.model_arch = ModelArchitecture.objects.create(
            name="TestNet",
            information="A test neural network architecture"
        )

    def test_model_architecture_creation_with_setup(self):
        """Test that ModelArchitecture from setUp was created correctly"""
        self.assertEqual(self.model_arch.name, "TestNet")
        self.assertEqual(self.model_arch.information, "A test neural network architecture")
        self.assertTrue(isinstance(self.model_arch, ModelArchitecture))
        self.assertTrue(self.model_arch.id)

    def test_model_architecture_unique_name_constraint(self):
        """Test unique constraint using setUp data"""
        with self.assertRaises(ValidationError):
            ModelArchitecture.objects.create(name="TestNet") 

    def test_create_model_architecture_name_only(self):
        """Test creating ModelArchitecture with only name (information optional)"""
        model_arch = ModelArchitecture.objects.create(name="AlexNet")
        self.assertEqual(model_arch.name, "AlexNet")
        self.assertIsNone(model_arch.information)

    def test_name_field_is_required(self):
        """Test that name field is required and cannot be empty"""
        with self.assertRaises(ValidationError):
            ModelArchitecture.objects.create(information="Network without name")
        
        with self.assertRaises(ValidationError):
            ModelArchitecture.objects.create(name="", information="Network with empty name")

    def test_name_max_length_valid(self):
        """Test name field with maximum allowed length (255 chars)"""
        long_name = "A" * 255
        model_arch = ModelArchitecture.objects.create(name=long_name)
        self.assertEqual(len(model_arch.name), 255)

    def test_name_max_length_invalid(self):
        """Test name field validation with too long name"""
        too_long_name = "A" * 256
        model_arch = ModelArchitecture(name=too_long_name)
        with self.assertRaises(ValidationError):
            model_arch.full_clean()

    def test_update_model_architecture_fields(self):
        """Test updating ModelArchitecture fields using setUp data"""
        # Update the setUp object
        self.model_arch.name = "UpdatedTestNet"
        self.model_arch.information = "Updated test information"
        self.model_arch.save()
        
        # Refresh from database to ensure it was saved
        self.model_arch.refresh_from_db()
        
        self.assertEqual(self.model_arch.name, "UpdatedTestNet")
        self.assertEqual(self.model_arch.information, "Updated test information")

    def test_delete_model_architecture(self):
        """Test deleting ModelArchitecture using setUp data"""
        model_id = self.model_arch.id
        
        # Delete the setUp object
        self.model_arch.delete()
        
        # Verify it's deleted
        with self.assertRaises(ModelArchitecture.DoesNotExist):
            ModelArchitecture.objects.get(id=model_id)

    def test_field_properties_and_types(self):
        """Test model field properties using setUp data"""
        # Test field properties through model meta
        name_field = ModelArchitecture._meta.get_field('name')
        info_field = ModelArchitecture._meta.get_field('information')
        
        # Name field tests
        self.assertEqual(name_field.max_length, 255)
        self.assertTrue(name_field.unique)
        self.assertFalse(name_field.null)
        
        # Information field tests
        self.assertTrue(info_field.null)
        self.assertTrue(info_field.blank)

    def test_create_multiple_different_architectures(self):
        """Test creating multiple ModelArchitectures with different names"""
        # The setUp already created "TestNet", so create others
        arch1 = ModelArchitecture.objects.create(name="VGG16", information="VGG with 16 layers")
        arch2 = ModelArchitecture.objects.create(name="MobileNet")
        
        # Test all exist and are different
        self.assertEqual(ModelArchitecture.objects.count(), 3)  # setUp + 2 new ones
        self.assertNotEqual(self.model_arch.name, arch1.name)
        self.assertNotEqual(self.model_arch.name, arch2.name)
        self.assertNotEqual(arch1.name, arch2.name)



class TacticSourceTest(TestCase):
    """Unit tests for TacticSource model"""
    
    def setUp(self):
        """Set up test data"""
        self.tactic_source = TacticSource.objects.create(
            title="Deep Learning Research Paper",
            url="https://arxiv.org/abs/1234.5678"
        )
        
    def test_tactic_source_creation_with_setup(self):
        """Test that TacticSource from setUp was created correctly"""
        self.assertEqual(self.tactic_source.title, "Deep Learning Research Paper")
        self.assertEqual(self.tactic_source.url, "https://arxiv.org/abs/1234.5678")
        self.assertTrue(isinstance(self.tactic_source, TacticSource))
        self.assertTrue(self.tactic_source.id)

    def test_title_field_is_required(self):
        """Test that title field is required"""
        with self.assertRaises(ValidationError):
            TacticSource.objects.create(url="https://example.com")

    def test_url_field_is_required(self):
        """Test that url field is required"""
        with self.assertRaises(ValidationError):
            TacticSource.objects.create(title="Test Title")

    def test_title_max_length_valid(self):
        """Test title field with maximum allowed length (255 chars)"""
        long_title = "A" * 255
        source = TacticSource.objects.create(
            title=long_title,
            url="https://example.com"
        )
        self.assertEqual(len(source.title), 255)

    def test_title_max_length_invalid(self):
        """Test title field validation with too long title"""
        too_long_title = "A" * 256
        source = TacticSource(title=too_long_title, url="https://example.com")
        with self.assertRaises(ValidationError):
            source.full_clean()

    def test_url_max_length_valid(self):
        """Test url field with maximum allowed length (500 chars)"""
        # Create a 500 char URL (valid structure)
        long_url = "https://example.com/" + "A" * 480  # 500 total chars
        source = TacticSource.objects.create(
            title="Test Title",
            url=long_url
        )
        self.assertEqual(len(source.url), 500)

    def test_url_field_validation(self):
        """Test URL field accepts valid URLs"""
        valid_urls = [
            "https://arxiv.org/abs/1234.5678",
            "http://example.com",
            "https://www.nature.com/articles/nature12345"
        ]
        
        for i, url in enumerate(valid_urls):
            source = TacticSource.objects.create(
                title=f"Test Title {i}",
                url=url
            )
            self.assertEqual(source.url, url)

    def test_invalid_url_validation(self):
        """Test URL field rejects invalid URLs"""
        source = TacticSource(title="Test", url="not-a-valid-url")
        with self.assertRaises(ValidationError):
            source.full_clean()

    def test_update_tactic_source_fields(self):
        """Test updating TacticSource fields using setUp data"""
        # Update the setUp object
        self.tactic_source.title = "Updated Research Paper"
        self.tactic_source.url = "https://updated-url.com"
        self.tactic_source.save()
        
        # Refresh from database
        self.tactic_source.refresh_from_db()
        
        self.assertEqual(self.tactic_source.title, "Updated Research Paper")
        self.assertEqual(self.tactic_source.url, "https://updated-url.com")

    def test_delete_tactic_source(self):
        """Test deleting TacticSource using setUp data"""
        source_id = self.tactic_source.id
        
        # Delete the setUp object
        self.tactic_source.delete()
        
        # Verify it's deleted
        with self.assertRaises(TacticSource.DoesNotExist):
            TacticSource.objects.get(id=source_id)

    def test_field_properties_and_types(self):
        """Test model field properties"""
        title_field = TacticSource._meta.get_field('title')
        url_field = TacticSource._meta.get_field('url')
        
        # Title field tests
        self.assertEqual(title_field.max_length, 255)
        self.assertFalse(title_field.null)
        
        # URL field tests  
        self.assertEqual(url_field.max_length, 500)
        self.assertFalse(url_field.null)



class ROIMetricTest(TestCase):
    """Unit tests for ROIMetric model"""
    
    def setUp(self):
        """Set up test data"""
        self.roi_metric = ROIMetric.objects.create(
            name="Energy Consumption",
            description="Power usage measurement",
            unit="W",
            is_energy_related=True,
            higher_is_better=False,
            min_value=0.0,
            max_value=1000.0
        )

    def test_roi_metric_creation_with_setup(self):
        """Test that ROIMetric from setUp was created correctly"""
        self.assertEqual(self.roi_metric.name, "Energy Consumption")
        self.assertEqual(self.roi_metric.description, "Power usage measurement")
        self.assertEqual(self.roi_metric.unit, "W")
        self.assertTrue(self.roi_metric.is_energy_related)
        self.assertFalse(self.roi_metric.higher_is_better)
        self.assertEqual(self.roi_metric.min_value, 0.0)
        self.assertEqual(self.roi_metric.max_value, 1000.0)
        self.assertTrue(isinstance(self.roi_metric, ROIMetric))
        self.assertTrue(self.roi_metric.id)

    def test_roi_metric_unique_name_constraint(self):
        """Test unique constraint using setUp data"""
        with self.assertRaises(ValidationError):
            ROIMetric.objects.create(name="Energy Consumption")

    def test_create_roi_metric_name_only(self):
        """Test creating ROIMetric with only required name field"""
        metric = ROIMetric.objects.create(name="Inference Time")
        self.assertEqual(metric.name, "Inference Time")
        self.assertIsNone(metric.description)
        self.assertIsNone(metric.unit)
        self.assertFalse(metric.is_energy_related)  # Default False
        self.assertFalse(metric.higher_is_better)   # Default False
        self.assertIsNone(metric.min_value)
        self.assertIsNone(metric.max_value)

    def test_name_field_is_required(self):
        """Test that name field is required and cannot be empty"""
        with self.assertRaises(ValidationError):
            ROIMetric.objects.create(description="Metric without name")
        
        with self.assertRaises(ValidationError):
            ROIMetric.objects.create(name="", description="Metric with empty name")

    def test_name_max_length_valid(self):
        """Test name field with maximum allowed length (255 chars)"""
        long_name = "A" * 255
        metric = ROIMetric.objects.create(name=long_name)
        self.assertEqual(len(metric.name), 255)

    def test_name_max_length_invalid(self):
        """Test name field validation with too long name"""
        too_long_name = "A" * 256
        metric = ROIMetric(name=too_long_name)
        with self.assertRaises(ValidationError):
            metric.full_clean()

    def test_boolean_field_values(self):
        """Test boolean fields can be set to True"""
        metric = ROIMetric.objects.create(
            name="Boolean Test Metric",
            is_energy_related=True,
            higher_is_better=True
        )
        self.assertTrue(metric.is_energy_related)
        self.assertTrue(metric.higher_is_better)

    def test_float_field_values(self):
        """Test float fields accept numeric values"""
        metric = ROIMetric.objects.create(
            name="Float Test Metric",
            min_value=10.54321,
            max_value=99.9
        )
        self.assertEqual(metric.min_value, 10.54321)
        self.assertEqual(metric.max_value, 99.9)

    def test_update_roi_metric_fields(self):
        """Test updating ROIMetric fields using setUp data"""
        # Update the setUp object
        self.roi_metric.name = "Updated Energy Metric"
        self.roi_metric.description = "Updated description"
        self.roi_metric.unit = "kW"
        self.roi_metric.is_energy_related = False
        self.roi_metric.higher_is_better = True
        self.roi_metric.min_value = 5.0
        self.roi_metric.max_value = 500.0
        self.roi_metric.save()
        
        # Refresh from database
        self.roi_metric.refresh_from_db()
        
        self.assertEqual(self.roi_metric.name, "Updated Energy Metric")
        self.assertEqual(self.roi_metric.description, "Updated description")
        self.assertEqual(self.roi_metric.unit, "kW")
        self.assertFalse(self.roi_metric.is_energy_related)
        self.assertTrue(self.roi_metric.higher_is_better)
        self.assertEqual(self.roi_metric.min_value, 5.0)
        self.assertEqual(self.roi_metric.max_value, 500.0)

    def test_delete_roi_metric(self):
        """Test deleting ROIMetric using setUp data"""
        metric_id = self.roi_metric.id
        
        # Delete the setUp object
        self.roi_metric.delete()
        
        # Verify it's deleted
        with self.assertRaises(ROIMetric.DoesNotExist):
            ROIMetric.objects.get(id=metric_id)

    def test_field_properties_and_types(self):
        """Test model field properties"""
        name_field = ROIMetric._meta.get_field('name')
        description_field = ROIMetric._meta.get_field('description')
        unit_field = ROIMetric._meta.get_field('unit')
        is_energy_field = ROIMetric._meta.get_field('is_energy_related')
        higher_better_field = ROIMetric._meta.get_field('higher_is_better')
        
        # Name field tests
        self.assertEqual(name_field.max_length, 255)
        self.assertTrue(name_field.unique)
        self.assertFalse(name_field.null)
        
        # Description field tests
        self.assertTrue(description_field.null)
        self.assertTrue(description_field.blank)
        
        # Unit field tests
        self.assertEqual(unit_field.max_length, 50)
        self.assertTrue(unit_field.null)
        self.assertTrue(unit_field.blank)
        
        # Boolean field tests
        self.assertFalse(is_energy_field.default)
        self.assertFalse(higher_better_field.default)




class MLTacticTest(TestCase):
    """Unit tests for MLTactic model"""
    
    def setUp(self):
        """Set up test data including related objects"""
        # Create related objects
        self.model_arch1 = ModelArchitecture.objects.create(
            name="ResNet50", 
            information="Deep residual network"
        )
        self.model_arch2 = ModelArchitecture.objects.create(
            name="VGG16", 
            information="VGG architecture"
        )
        
        self.tactic_source1 = TacticSource.objects.create(
            title="Pruning Research Paper",
            url="https://arxiv.org/abs/1234.5678"
        )
        self.tactic_source2 = TacticSource.objects.create(
            title="Quantization Paper",
            url="https://arxiv.org/abs/9876.5432"
        )
        
        self.roi_metric1 = ROIMetric.objects.create(
            name="Energy Consumption",
            unit="W",
            is_energy_related=True
        )
        self.roi_metric2 = ROIMetric.objects.create(
            name="Inference Time",
            unit="ms",
            higher_is_better=False
        )
        
        # Create MLTactic with relationships
        self.ml_tactic = MLTactic.objects.create(
            name="Weight Pruning",
            information="Removes less important weights from neural networks"
        )
        # Add ManyToMany relationships
        self.ml_tactic.sources.add(self.tactic_source1)
        self.ml_tactic.compatible_architectures.add(self.model_arch1)
        self.ml_tactic.applicable_metrics.add(self.roi_metric1)

    def test_ml_tactic_creation_with_setup(self):
        """Test that MLTactic from setUp was created correctly"""
        self.assertEqual(self.ml_tactic.name, "Weight Pruning")
        self.assertEqual(self.ml_tactic.information, "Removes less important weights from neural networks")
        self.assertTrue(isinstance(self.ml_tactic, MLTactic))
        self.assertTrue(self.ml_tactic.id)

    def test_ml_tactic_unique_name_constraint(self):
        """Test unique constraint using setUp data"""
        with self.assertRaises(ValidationError):
            MLTactic.objects.create(name="Weight Pruning")

    def test_create_ml_tactic_name_only(self):
        """Test creating MLTactic with only required name field"""
        tactic = MLTactic.objects.create(name="Quantization")
        self.assertEqual(tactic.name, "Quantization")
        self.assertIsNone(tactic.information)
        # ManyToMany fields should be empty
        self.assertEqual(tactic.sources.count(), 0)
        self.assertEqual(tactic.compatible_architectures.count(), 0)
        self.assertEqual(tactic.applicable_metrics.count(), 0)

    def test_name_field_is_required(self):
        """Test that name field is required and cannot be empty"""
        with self.assertRaises(ValidationError):
            MLTactic.objects.create(information="Tactic without name")
        
        with self.assertRaises(ValidationError):
            MLTactic.objects.create(name="", information="Tactic with empty name")

    def test_name_max_length_valid(self):
        """Test name field with maximum allowed length (255 chars)"""
        long_name = "A" * 255
        tactic = MLTactic.objects.create(name=long_name)
        self.assertEqual(len(tactic.name), 255)

    def test_name_max_length_invalid(self):
        """Test name field validation with too long name"""
        too_long_name = "A" * 256
        tactic = MLTactic(name=too_long_name)
        with self.assertRaises(ValidationError):
            tactic.full_clean()

    def test_manytomany_sources_relationship(self):
        """Test ManyToMany relationship with TacticSource"""
        # Test adding sources
        self.ml_tactic.sources.add(self.tactic_source2)
        self.assertEqual(self.ml_tactic.sources.count(), 2)
        
        # Test getting sources
        sources = list(self.ml_tactic.sources.all())
        self.assertIn(self.tactic_source1, sources)
        self.assertIn(self.tactic_source2, sources)
        
        # Test reverse relationship
        tactics_for_source1 = list(self.tactic_source1.tactics.all())
        self.assertIn(self.ml_tactic, tactics_for_source1)

    def test_manytomany_compatible_architectures_relationship(self):
        """Test ManyToMany relationship with ModelArchitecture"""
        # Test adding architectures
        self.ml_tactic.compatible_architectures.add(self.model_arch2)
        self.assertEqual(self.ml_tactic.compatible_architectures.count(), 2)
        
        # Test getting architectures
        architectures = list(self.ml_tactic.compatible_architectures.all())
        self.assertIn(self.model_arch1, architectures)
        self.assertIn(self.model_arch2, architectures)
        
        # Test reverse relationship
        tactics_for_arch1 = list(self.model_arch1.compatible_tactics.all())
        self.assertIn(self.ml_tactic, tactics_for_arch1)

    def test_manytomany_applicable_metrics_relationship(self):
        """Test ManyToMany relationship with ROIMetric"""
        # Test adding metrics
        self.ml_tactic.applicable_metrics.add(self.roi_metric2)
        self.assertEqual(self.ml_tactic.applicable_metrics.count(), 2)
        
        # Test getting metrics
        metrics = list(self.ml_tactic.applicable_metrics.all())
        self.assertIn(self.roi_metric1, metrics)
        self.assertIn(self.roi_metric2, metrics)
        
        # Test reverse relationship
        tactics_for_metric1 = list(self.roi_metric1.applicable_tactics.all())
        self.assertIn(self.ml_tactic, tactics_for_metric1)

    def test_manytomany_remove_relationships(self):
        """Test removing ManyToMany relationships"""
        # Remove source
        self.ml_tactic.sources.remove(self.tactic_source1)
        self.assertEqual(self.ml_tactic.sources.count(), 0)
        
        # Remove architecture
        self.ml_tactic.compatible_architectures.remove(self.model_arch1)
        self.assertEqual(self.ml_tactic.compatible_architectures.count(), 0)
        
        # Remove metric
        self.ml_tactic.applicable_metrics.remove(self.roi_metric1)
        self.assertEqual(self.ml_tactic.applicable_metrics.count(), 0)

    def test_update_ml_tactic_fields(self):
        """Test updating MLTactic fields using setUp data"""
        # Update the setUp object
        self.ml_tactic.name = "Updated Pruning Technique"
        self.ml_tactic.information = "Updated information about pruning"
        self.ml_tactic.save()
        
        # Refresh from database
        self.ml_tactic.refresh_from_db()
        
        self.assertEqual(self.ml_tactic.name, "Updated Pruning Technique")
        self.assertEqual(self.ml_tactic.information, "Updated information about pruning")
        
        # ManyToMany relationships should remain intact
        self.assertEqual(self.ml_tactic.sources.count(), 1)
        self.assertEqual(self.ml_tactic.compatible_architectures.count(), 1)
        self.assertEqual(self.ml_tactic.applicable_metrics.count(), 1)

    def test_delete_ml_tactic(self):
        """Test deleting MLTactic using setUp data"""
        tactic_id = self.ml_tactic.id
        
        # Delete the setUp object
        self.ml_tactic.delete()
        
        # Verify it's deleted
        with self.assertRaises(MLTactic.DoesNotExist):
            MLTactic.objects.get(id=tactic_id)
        
        # Verify related objects still exist (ManyToMany doesn't cascade delete)
        self.assertTrue(TacticSource.objects.filter(id=self.tactic_source1.id).exists())
        self.assertTrue(ModelArchitecture.objects.filter(id=self.model_arch1.id).exists())
        self.assertTrue(ROIMetric.objects.filter(id=self.roi_metric1.id).exists())

    def test_field_properties_and_types(self):
        """Test model field properties"""
        name_field = MLTactic._meta.get_field('name')
        info_field = MLTactic._meta.get_field('information')
        sources_field = MLTactic._meta.get_field('sources')
        arch_field = MLTactic._meta.get_field('compatible_architectures')
        metrics_field = MLTactic._meta.get_field('applicable_metrics')
        
        # Name field tests
        self.assertEqual(name_field.max_length, 255)
        self.assertTrue(name_field.unique)
        self.assertFalse(name_field.null)
        
        # Information field tests
        self.assertTrue(info_field.null)
        self.assertTrue(info_field.blank)
        
        # ManyToMany field tests
        self.assertEqual(sources_field.related_model, TacticSource)
        self.assertEqual(arch_field.related_model, ModelArchitecture)
        self.assertEqual(metrics_field.related_model, ROIMetric)
        
        # Check related names
        self.assertEqual(sources_field.remote_field.related_name, 'tactics')
        self.assertEqual(arch_field.remote_field.related_name, 'compatible_tactics')
        self.assertEqual(metrics_field.remote_field.related_name, 'applicable_tactics')





class TacticParameterOptionTest(TestCase):
    """Unit tests for TacticParameterOption model"""
    
    def setUp(self):
        """Set up test data including related objects"""
        # Create required related objects first
        self.tactic_source = TacticSource.objects.create(
            title="Pruning Research Paper",
            url="https://arxiv.org/abs/1234.5678"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Weight Pruning",
            information="Neural network weight pruning technique"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        
        # Create TacticParameterOption
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity_level",
            value="0.5"
        )

    def test_tactic_parameter_option_creation_with_setup(self):
        """Test that TacticParameterOption from setUp was created correctly"""
        self.assertEqual(self.param_option.tactic, self.ml_tactic)
        self.assertEqual(self.param_option.name, "sparsity_level")
        self.assertEqual(self.param_option.value, "0.5")
        self.assertTrue(isinstance(self.param_option, TacticParameterOption))
        self.assertTrue(self.param_option.id)

    def test_foreignkey_relationship_with_tactic(self):
        """Test ForeignKey relationship with MLTactic"""
        # Test forward relationship
        self.assertEqual(self.param_option.tactic.name, "Weight Pruning")
        
        # Test reverse relationship
        param_options = list(self.ml_tactic.parameter_options.all())
        self.assertIn(self.param_option, param_options)
        self.assertEqual(self.ml_tactic.parameter_options.count(), 1)

    def test_name_max_length_valid(self):
        """Test name field with maximum allowed length (255 chars)"""
        long_name = "A" * 255
        param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name=long_name,
            value="test_value"
        )
        self.assertEqual(len(param_option.name), 255)

    def test_name_max_length_invalid(self):
        """Test name field validation with too long name"""
        too_long_name = "A" * 256
        param_option = TacticParameterOption(tactic=self.ml_tactic, name=too_long_name, value="test_value")
        with self.assertRaises(ValidationError):
            param_option.full_clean()

    def test_unique_together_constraint(self):
        """Test unique_together constraint (tactic, name, value)"""
        # This should work - different combination
        param_option2 = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity_level",
            value="0.8"  # Different value
        )
        self.assertEqual(param_option2.value, "0.8")
        
        # This should work - different name
        param_option3 = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="quantization_bits",  # Different name
            value="0.5"
        )
        self.assertEqual(param_option3.name, "quantization_bits")
        
        # This should fail - exact same combination
        with self.assertRaises(IntegrityError):
            TacticParameterOption.objects.create(
                tactic=self.ml_tactic,
                name="sparsity_level",  # Same as setUp
                value="0.5"             # Same as setUp
            )

    def test_multiple_parameters_for_same_tactic(self):
        """Test creating multiple parameters for the same tactic"""
        # Create additional parameters
        param2 = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="quantization_bits",
            value="8"
        )
        param3 = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="learning_rate",
            value="0.001"
        )
        
        # Test that tactic has multiple parameters
        self.assertEqual(self.ml_tactic.parameter_options.count(), 3)
        
        # Test that all parameters belong to the same tactic
        all_params = list(self.ml_tactic.parameter_options.all())
        self.assertIn(self.param_option, all_params)
        self.assertIn(param2, all_params)
        self.assertIn(param3, all_params)

    def test_cascade_delete_behavior(self):
        """Test CASCADE delete when tactic is deleted"""
        param_option_id = self.param_option.id
        tactic_id = self.ml_tactic.id
        
        # Delete the tactic
        self.ml_tactic.delete()
        
        # Verify tactic is deleted
        with self.assertRaises(MLTactic.DoesNotExist):
            MLTactic.objects.get(id=tactic_id)
        
        # Verify parameter option is also deleted (CASCADE)
        with self.assertRaises(TacticParameterOption.DoesNotExist):
            TacticParameterOption.objects.get(id=param_option_id)

    def test_update_parameter_option_fields(self):
        """Test updating TacticParameterOption fields using setUp data"""
        # Create another tactic for testing tactic change
        new_tactic = MLTactic.objects.create(name="Quantization")
        new_tactic.sources.add(self.tactic_source)
        
        # Update the setUp object
        self.param_option.tactic = new_tactic
        self.param_option.name = "updated_param"
        self.param_option.value = "updated_value"
        self.param_option.save()
        
        # Refresh from database
        self.param_option.refresh_from_db()
        
        self.assertEqual(self.param_option.tactic, new_tactic)
        self.assertEqual(self.param_option.name, "updated_param")
        self.assertEqual(self.param_option.value, "updated_value")
        
        # Test string representation updated
        self.assertEqual(str(self.param_option), "Quantization - updated_param: updated_value")

    def test_delete_parameter_option(self):
        """Test deleting TacticParameterOption using setUp data"""
        param_id = self.param_option.id
        
        # Delete the setUp object
        self.param_option.delete()
        
        # Verify it's deleted
        with self.assertRaises(TacticParameterOption.DoesNotExist):
            TacticParameterOption.objects.get(id=param_id)
        
        # Verify related tactic still exists (no reverse cascade)
        self.assertTrue(MLTactic.objects.filter(id=self.ml_tactic.id).exists())

    def test_field_properties_and_types(self):
        """Test model field properties"""
        tactic_field = TacticParameterOption._meta.get_field('tactic')
        name_field = TacticParameterOption._meta.get_field('name')
        value_field = TacticParameterOption._meta.get_field('value')
        
        # ForeignKey field tests
        self.assertEqual(tactic_field.related_model, MLTactic)
        self.assertEqual(tactic_field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(tactic_field.remote_field.related_name, 'parameter_options')
        
        # CharField field tests
        self.assertEqual(name_field.max_length, 255)
        self.assertFalse(name_field.null)
        
        self.assertEqual(value_field.max_length, 255)
        self.assertFalse(value_field.null)
        
        # Test unique_together constraint
        unique_together = TacticParameterOption._meta.unique_together
        self.assertIn(('tactic', 'name', 'value'), unique_together)

    def test_different_tactics_same_parameters(self):
        """Test that different tactics can have same parameter name/value combinations"""
        # Create another tactic
        another_tactic = MLTactic.objects.create(name="Quantization")
        another_tactic.sources.add(self.tactic_source)
        
        # This should work - same name/value but different tactic
        param_option2 = TacticParameterOption.objects.create(
            tactic=another_tactic,
            name="sparsity_level",  # Same name as setUp
            value="0.5"             # Same value as setUp
        )
        
        self.assertEqual(param_option2.name, "sparsity_level")
        self.assertEqual(param_option2.value, "0.5")
        self.assertNotEqual(param_option2.tactic, self.param_option.tactic)