from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.gaissa_roi_analyzer.models import *
from apps.core.models import Country



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





class ExpectedMetricReductionTest(TestCase):
    """Unit tests for ExpectedMetricReduction model"""
    
    def setUp(self):
        """Set up test data including all related objects"""
        # Create related objects
        self.model_arch = ModelArchitecture.objects.create(
            name="ResNet50",
            information="Deep residual network"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Pruning Research Paper",
            url="https://arxiv.org/abs/1234.5678"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Weight Pruning",
            information="Neural network pruning technique"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity_level",
            value="0.5"
        )
        
        self.roi_metric = ROIMetric.objects.create(
            name="Energy Consumption",
            description="Power usage measurement",
            unit="W",
            is_energy_related=True,
            higher_is_better=False
        )
        
        # Create ExpectedMetricReduction
        self.expected_reduction = ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            metric=self.roi_metric,
            expectedReductionValue=0.25
        )

    def test_expected_metric_reduction_creation_with_setup(self):
        """Test that ExpectedMetricReduction from setUp was created correctly"""
        self.assertEqual(self.expected_reduction.model_architecture, self.model_arch)
        self.assertEqual(self.expected_reduction.tactic_parameter_option, self.param_option)
        self.assertEqual(self.expected_reduction.metric, self.roi_metric)
        self.assertEqual(self.expected_reduction.expectedReductionValue, 0.25)
        self.assertTrue(isinstance(self.expected_reduction, ExpectedMetricReduction))
        self.assertTrue(self.expected_reduction.id)

    def test_foreignkey_relationships(self):
        """Test ForeignKey relationships"""
        # Test forward relationships
        self.assertEqual(self.expected_reduction.model_architecture.name, "ResNet50")
        self.assertEqual(self.expected_reduction.tactic_parameter_option.name, "sparsity_level")
        self.assertEqual(self.expected_reduction.metric.name, "Energy Consumption")
        
        # Test reverse relationships (CASCADE doesn't create reverse related names by default)
        # But we can still access through the foreign key
        self.assertEqual(self.expected_reduction.model_architecture, self.model_arch)
        self.assertEqual(self.expected_reduction.tactic_parameter_option, self.param_option)
        self.assertEqual(self.expected_reduction.metric, self.roi_metric)

    def test_float_field_values(self):
        """Test expectedReductionValue field accepts various float values"""
        test_values = [0.0, 0.00001, 0.5, 0.99, 1.0, 2.5, -0.1]
        
        for i, value in enumerate(test_values):
            # Create new metric for each test to avoid unique constraint
            metric = ROIMetric.objects.create(name=f"Test Metric {i}")
            
            reduction = ExpectedMetricReduction.objects.create(
                model_architecture=self.model_arch,
                tactic_parameter_option=self.param_option,
                metric=metric,
                expectedReductionValue=value
            )
            self.assertEqual(reduction.expectedReductionValue, value)

    def test_unique_together_constraint(self):
        """Test unique_together constraint (model_architecture, tactic_parameter_option, metric)"""
        from django.db import transaction
        
        # This should fail - exact same combination
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                ExpectedMetricReduction.objects.create(
                    model_architecture=self.model_arch,  # Same
                    tactic_parameter_option=self.param_option,  # Same
                    metric=self.roi_metric,  # Same
                    expectedReductionValue=0.4  # Different value doesn't matter
                )
        
        # This should work - different architecture
        new_arch = ModelArchitecture.objects.create(name="VGG16")
        self.ml_tactic.compatible_architectures.add(new_arch)
        
        reduction2 = ExpectedMetricReduction.objects.create(
            model_architecture=new_arch,  # Different
            tactic_parameter_option=self.param_option,  # Same
            metric=self.roi_metric,  # Same
            expectedReductionValue=0.3
        )
        self.assertEqual(reduction2.expectedReductionValue, 0.3)
        
        # This should work - different parameter option
        new_param = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity_level",
            value="0.8"  # Different value
        )
        
        reduction3 = ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,  # Same
            tactic_parameter_option=new_param,  # Different
            metric=self.roi_metric,  # Same
            expectedReductionValue=0.35
        )
        self.assertEqual(reduction3.expectedReductionValue, 0.35)
        
        # This should work - different metric
        new_metric = ROIMetric.objects.create(name="Inference Time", unit="ms")
        
        reduction4 = ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,  # Same
            tactic_parameter_option=self.param_option,  # Same
            metric=new_metric,  # Different
            expectedReductionValue=0.4
        )
        self.assertEqual(reduction4.expectedReductionValue, 0.4)

    def test_cascade_delete_behavior_model_architecture(self):
        """Test CASCADE delete when model_architecture is deleted"""
        reduction_id = self.expected_reduction.id
        arch_id = self.model_arch.id
        
        # Delete the model architecture
        self.model_arch.delete()
        
        # Verify architecture is deleted
        with self.assertRaises(ModelArchitecture.DoesNotExist):
            ModelArchitecture.objects.get(id=arch_id)
        
        # Verify expected reduction is also deleted (CASCADE)
        with self.assertRaises(ExpectedMetricReduction.DoesNotExist):
            ExpectedMetricReduction.objects.get(id=reduction_id)

    def test_cascade_delete_behavior_tactic_parameter_option(self):
        """Test CASCADE delete when tactic_parameter_option is deleted"""
        reduction_id = self.expected_reduction.id
        param_id = self.param_option.id
        
        # Delete the parameter option
        self.param_option.delete()
        
        # Verify parameter option is deleted
        with self.assertRaises(TacticParameterOption.DoesNotExist):
            TacticParameterOption.objects.get(id=param_id)
        
        # Verify expected reduction is also deleted (CASCADE)
        with self.assertRaises(ExpectedMetricReduction.DoesNotExist):
            ExpectedMetricReduction.objects.get(id=reduction_id)

    def test_cascade_delete_behavior_metric(self):
        """Test CASCADE delete when metric is deleted"""
        reduction_id = self.expected_reduction.id
        metric_id = self.roi_metric.id
        
        # Delete the metric
        self.roi_metric.delete()
        
        # Verify metric is deleted
        with self.assertRaises(ROIMetric.DoesNotExist):
            ROIMetric.objects.get(id=metric_id)
        
        # Verify expected reduction is also deleted (CASCADE)
        with self.assertRaises(ExpectedMetricReduction.DoesNotExist):
            ExpectedMetricReduction.objects.get(id=reduction_id)

    def test_update_expected_metric_reduction_fields(self):
        """Test updating ExpectedMetricReduction fields"""
        # Create new objects for updating
        new_arch = ModelArchitecture.objects.create(name="MobileNet")
        self.ml_tactic.compatible_architectures.add(new_arch)
        
        new_param = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="quantization_bits",
            value="8"
        )
        
        new_metric = ROIMetric.objects.create(name="Model Size", unit="MB")
        
        # Update the reduction
        self.expected_reduction.model_architecture = new_arch
        self.expected_reduction.tactic_parameter_option = new_param
        self.expected_reduction.metric = new_metric
        self.expected_reduction.expectedReductionValue = 0.75
        self.expected_reduction.save()
        
        # Refresh from database
        self.expected_reduction.refresh_from_db()
        
        self.assertEqual(self.expected_reduction.model_architecture, new_arch)
        self.assertEqual(self.expected_reduction.tactic_parameter_option, new_param)
        self.assertEqual(self.expected_reduction.metric, new_metric)
        self.assertEqual(self.expected_reduction.expectedReductionValue, 0.75)
        
        # Test string representation updated
        expected_str = f"Reduction for Model Size on MobileNet with Weight Pruning - quantization_bits: 8"
        self.assertEqual(str(self.expected_reduction), expected_str)

    def test_delete_expected_metric_reduction(self):
        """Test deleting ExpectedMetricReduction"""
        reduction_id = self.expected_reduction.id
        
        # Delete the reduction
        self.expected_reduction.delete()
        
        # Verify it's deleted
        with self.assertRaises(ExpectedMetricReduction.DoesNotExist):
            ExpectedMetricReduction.objects.get(id=reduction_id)
        
        # Verify related objects still exist (no reverse cascade)
        self.assertTrue(ModelArchitecture.objects.filter(id=self.model_arch.id).exists())
        self.assertTrue(TacticParameterOption.objects.filter(id=self.param_option.id).exists())
        self.assertTrue(ROIMetric.objects.filter(id=self.roi_metric.id).exists())

    def test_field_properties_and_types(self):
        """Test model field properties"""
        arch_field = ExpectedMetricReduction._meta.get_field('model_architecture')
        param_field = ExpectedMetricReduction._meta.get_field('tactic_parameter_option')
        metric_field = ExpectedMetricReduction._meta.get_field('metric')
        value_field = ExpectedMetricReduction._meta.get_field('expectedReductionValue')
        
        # ForeignKey field tests
        self.assertEqual(arch_field.related_model, ModelArchitecture)
        self.assertEqual(arch_field.remote_field.on_delete, models.CASCADE)
        self.assertFalse(arch_field.null)
        
        self.assertEqual(param_field.related_model, TacticParameterOption)
        self.assertEqual(param_field.remote_field.on_delete, models.CASCADE)
        self.assertFalse(param_field.null)
        
        self.assertEqual(metric_field.related_model, ROIMetric)
        self.assertEqual(metric_field.remote_field.on_delete, models.CASCADE)
        self.assertFalse(metric_field.null)
        
        # FloatField tests
        self.assertFalse(value_field.null)
        
        # Test unique_together constraint
        unique_together = ExpectedMetricReduction._meta.unique_together
        self.assertIn(('model_architecture', 'tactic_parameter_option', 'metric'), unique_together)
        



class ROIAnalysisTest(TestCase):
    """Unit tests for ROIAnalysis model"""
    
    def setUp(self):
        """Set up test data including all related objects"""
        # Create related objects
        self.country = Country.objects.create(
            name="Spain",
            country_code="ES"
        )
        
        self.model_arch = ModelArchitecture.objects.create(
            name="ResNet50",
            information="Deep residual network"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Pruning Research Paper",
            url="https://arxiv.org/abs/1234.5678"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Weight Pruning",
            information="Neural network pruning technique"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        # Make the tactic compatible with the architecture
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity_level",
            value="0.5"
        )
        
        # Create ROIAnalysis
        self.roi_analysis = ROIAnalysis.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )

    def test_roi_analysis_creation_with_setup(self):
        """Test that ROIAnalysis from setUp was created correctly"""
        self.assertEqual(self.roi_analysis.model_architecture, self.model_arch)
        self.assertEqual(self.roi_analysis.tactic_parameter_option, self.param_option)
        self.assertEqual(self.roi_analysis.country, self.country)
        self.assertTrue(isinstance(self.roi_analysis, ROIAnalysis))
        self.assertTrue(self.roi_analysis.id)

    def test_foreignkey_relationships(self):
        """Test ForeignKey relationships"""
        # Test forward relationships
        self.assertEqual(self.roi_analysis.model_architecture.name, "ResNet50")
        self.assertEqual(self.roi_analysis.tactic_parameter_option.name, "sparsity_level")
        self.assertEqual(self.roi_analysis.country.name, "Spain")
        
        # Test reverse relationships
        arch_analyses = list(self.model_arch.roi_analyses.all())
        self.assertIn(self.roi_analysis, arch_analyses)
        
        param_analyses = list(self.param_option.roi_analyses.all())
        self.assertIn(self.roi_analysis, param_analyses)
        
        country_analyses = list(self.country.roi_analyses.all())
        self.assertIn(self.roi_analysis, country_analyses)

    def test_compatibility_validation_success(self):
        """Test successful validation when tactic is compatible with architecture"""
        # This should work - architecture is in tactic's compatible list
        analysis = ROIAnalysis(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )
        # Should not raise ValidationError
        analysis.full_clean()

    def test_compatibility_validation_failure(self):
        """Test validation failure when tactic is not compatible with architecture"""
        # Create an incompatible architecture
        incompatible_arch = ModelArchitecture.objects.create(
            name="IncompatibleNet",
            information="Architecture not compatible with pruning"
        )
        # Note: We don't add this to ml_tactic.compatible_architectures
        
        analysis = ROIAnalysis(
            model_architecture=incompatible_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )
        
        with self.assertRaises(ValidationError) as context:
            analysis.full_clean()
        
        # Check error message
        error_message = str(context.exception)
        self.assertIn("not compatible", error_message)
        self.assertIn("Weight Pruning", error_message)
        self.assertIn("IncompatibleNet", error_message)

    def test_protect_foreign_key_behavior(self):
        """Test PROTECT behavior when trying to delete related objects"""
        # Try to delete model_architecture - should fail
        with self.assertRaises(models.ProtectedError):
            self.model_arch.delete()
        
        # Try to delete tactic_parameter_option - should fail
        with self.assertRaises(models.ProtectedError):
            self.param_option.delete()
        
        # Try to delete country - should fail
        with self.assertRaises(models.ProtectedError):
            self.country.delete()

    def test_update_roi_analysis_fields(self):
        """Test updating ROIAnalysis fields"""
        # Create another compatible setup
        new_arch = ModelArchitecture.objects.create(name="MobileNet")
        self.ml_tactic.compatible_architectures.add(new_arch)
        
        new_param = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity_level",
            value="0.8"
        )
        
        new_country = Country.objects.create(name="France", country_code="FR")
        
        # Update the analysis
        self.roi_analysis.model_architecture = new_arch
        self.roi_analysis.tactic_parameter_option = new_param
        self.roi_analysis.country = new_country
        self.roi_analysis.save()
        
        # Refresh from database
        self.roi_analysis.refresh_from_db()
        
        self.assertEqual(self.roi_analysis.model_architecture, new_arch)
        self.assertEqual(self.roi_analysis.tactic_parameter_option, new_param)
        self.assertEqual(self.roi_analysis.country, new_country)

    def test_delete_roi_analysis(self):
        """Test deleting ROIAnalysis"""
        analysis_id = self.roi_analysis.id
        
        # Delete the analysis
        self.roi_analysis.delete()
        
        # Verify it's deleted
        with self.assertRaises(ROIAnalysis.DoesNotExist):
            ROIAnalysis.objects.get(id=analysis_id)
        
        # Verify related objects still exist (PROTECT behavior)
        self.assertTrue(ModelArchitecture.objects.filter(id=self.model_arch.id).exists())
        self.assertTrue(TacticParameterOption.objects.filter(id=self.param_option.id).exists())
        self.assertTrue(Country.objects.filter(id=self.country.id).exists())

    def test_field_properties_and_types(self):
        """Test model field properties"""
        arch_field = ROIAnalysis._meta.get_field('model_architecture')
        param_field = ROIAnalysis._meta.get_field('tactic_parameter_option')
        country_field = ROIAnalysis._meta.get_field('country')
        
        # ForeignKey field tests
        self.assertEqual(arch_field.related_model, ModelArchitecture)
        self.assertEqual(arch_field.remote_field.on_delete, models.PROTECT)
        self.assertEqual(arch_field.remote_field.related_name, 'roi_analyses')
        
        self.assertEqual(param_field.related_model, TacticParameterOption)
        self.assertEqual(param_field.remote_field.on_delete, models.PROTECT)
        self.assertEqual(param_field.remote_field.related_name, 'roi_analyses')
        
        self.assertEqual(country_field.related_model, Country)
        self.assertEqual(country_field.remote_field.on_delete, models.PROTECT)
        self.assertEqual(country_field.remote_field.related_name, 'roi_analyses')
        self.assertTrue(country_field.null)




class ROIAnalysisCalculationTest(TestCase):
    """Unit tests for ROIAnalysisCalculation model (inherits from ROIAnalysis)"""
    
    def setUp(self):
        """Set up test data including all related objects"""
        # Create all required related objects
        self.country = Country.objects.create(name="Germany", country_code="DE")
        
        self.model_arch = ModelArchitecture.objects.create(
            name="VGG16",
            information="VGG architecture"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Quantization Research",
            url="https://arxiv.org/abs/2222.3333"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Quantization",
            information="Neural network quantization"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="bits",
            value="8"
        )
        
        # Create ROIAnalysisCalculation
        self.roi_calculation = ROIAnalysisCalculation.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )

    def test_roi_analysis_calculation_creation_with_setup(self):
        """Test that ROIAnalysisCalculation from setUp was created correctly"""
        self.assertEqual(self.roi_calculation.model_architecture, self.model_arch)
        self.assertEqual(self.roi_calculation.tactic_parameter_option, self.param_option)
        self.assertEqual(self.roi_calculation.country, self.country)
        self.assertTrue(isinstance(self.roi_calculation, ROIAnalysisCalculation))
        self.assertTrue(isinstance(self.roi_calculation, ROIAnalysis))  # Inheritance
        self.assertTrue(self.roi_calculation.id)
        self.assertIsNotNone(self.roi_calculation.dateRegistration)

    def test_date_registration_auto_now_add(self):
        """Test that dateRegistration is automatically set on creation"""
        from django.utils import timezone
        before_creation = timezone.now()
        
        calculation = ROIAnalysisCalculation.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option
        )
        
        after_creation = timezone.now()
        
        # Check that dateRegistration is between before and after
        self.assertGreaterEqual(calculation.dateRegistration, before_creation)
        self.assertLessEqual(calculation.dateRegistration, after_creation)

    def test_inheritance_from_roi_analysis(self):
        """Test that ROIAnalysisCalculation inherits ROIAnalysis functionality"""
        # Test inherited string representation
        expected_str = f"ROI Analysis {self.roi_calculation.id} for {self.model_arch.name} with {self.param_option}"
        self.assertEqual(str(self.roi_calculation), expected_str)
        
        # Test inherited validation
        incompatible_arch = ModelArchitecture.objects.create(name="IncompatibleNet")
        
        calculation = ROIAnalysisCalculation(
            model_architecture=incompatible_arch,
            tactic_parameter_option=self.param_option
        )
        
        with self.assertRaises(ValidationError):
            calculation.full_clean()

    def test_field_properties_and_types(self):
        """Test model field properties specific to ROIAnalysisCalculation"""
        date_field = ROIAnalysisCalculation._meta.get_field('dateRegistration')
        
        # DateTimeField tests
        self.assertTrue(date_field.auto_now_add)
        self.assertFalse(date_field.null)




class ROIAnalysisResearchTest(TestCase):
    """Unit tests for ROIAnalysisResearch model (inherits from ROIAnalysis)"""
    
    def setUp(self):
        """Set up test data including all related objects"""
        # Create all required related objects
        self.country = Country.objects.create(name="Italy", country_code="IT")
        
        self.model_arch = ModelArchitecture.objects.create(
            name="MobileNet",
            information="Mobile architecture"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Distillation Research",
            url="https://arxiv.org/abs/3333.4444"
        )
        
        self.research_source = TacticSource.objects.create(
            title="Specific Research Paper",
            url="https://arxiv.org/abs/5555.6666"
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Knowledge Distillation",
            information="Teacher-student distillation"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="temperature",
            value="4.0"
        )
        
        # Create ROIAnalysisResearch
        self.roi_research = ROIAnalysisResearch.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country,
            source=self.research_source
        )

    def test_roi_analysis_research_creation_with_setup(self):
        """Test that ROIAnalysisResearch from setUp was created correctly"""
        self.assertEqual(self.roi_research.model_architecture, self.model_arch)
        self.assertEqual(self.roi_research.tactic_parameter_option, self.param_option)
        self.assertEqual(self.roi_research.country, self.country)
        self.assertEqual(self.roi_research.source, self.research_source)
        self.assertTrue(isinstance(self.roi_research, ROIAnalysisResearch))
        self.assertTrue(isinstance(self.roi_research, ROIAnalysis))  # Inheritance
        self.assertTrue(self.roi_research.id)

    def test_source_field_is_required(self):
        """Test that source field is required for ROIAnalysisResearch"""
        with self.assertRaises(IntegrityError):
            ROIAnalysisResearch.objects.create(
                model_architecture=self.model_arch,
                tactic_parameter_option=self.param_option,
                country=self.country
                # Missing source
            )

    def test_source_foreignkey_relationship(self):
        """Test ForeignKey relationship with TacticSource"""
        # Test forward relationship
        self.assertEqual(self.roi_research.source.title, "Specific Research Paper")
        
        # Test reverse relationship
        research_analyses = list(self.research_source.roi_analysis_researches.all())
        self.assertIn(self.roi_research, research_analyses)

    def test_protect_source_foreign_key(self):
        """Test PROTECT behavior when trying to delete source"""
        # Try to delete source - should fail
        with self.assertRaises(models.ProtectedError):
            self.research_source.delete()

    def test_inheritance_from_roi_analysis(self):
        """Test that ROIAnalysisResearch inherits ROIAnalysis functionality"""
        # Test inherited string representation
        expected_str = f"ROI Analysis {self.roi_research.id} for {self.model_arch.name} with {self.param_option}"
        self.assertEqual(str(self.roi_research), expected_str)
        
        # Test inherited validation
        incompatible_arch = ModelArchitecture.objects.create(name="IncompatibleNet")
        
        research = ROIAnalysisResearch(
            model_architecture=incompatible_arch,
            tactic_parameter_option=self.param_option,
            source=self.research_source
        )
        
        with self.assertRaises(ValidationError):
            research.full_clean()

    def test_update_roi_analysis_research_fields(self):
        """Test updating ROIAnalysisResearch fields"""
        # Create new source
        new_source = TacticSource.objects.create(
            title="Updated Research",
            url="https://arxiv.org/abs/7777.8888"
        )
        
        # Update the research
        self.roi_research.source = new_source
        self.roi_research.save()
        
        # Refresh from database
        self.roi_research.refresh_from_db()
        
        self.assertEqual(self.roi_research.source, new_source)

    def test_field_properties_and_types(self):
        """Test model field properties specific to ROIAnalysisResearch"""
        source_field = ROIAnalysisResearch._meta.get_field('source')
        
        # ForeignKey field tests
        self.assertEqual(source_field.related_model, TacticSource)
        self.assertEqual(source_field.remote_field.on_delete, models.PROTECT)
        self.assertEqual(source_field.remote_field.related_name, 'roi_analysis_researches')
        self.assertFalse(source_field.null)