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