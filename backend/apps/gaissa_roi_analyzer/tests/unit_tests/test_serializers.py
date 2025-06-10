from django.test import TestCase
from apps.gaissa_roi_analyzer.models import ModelArchitecture
from apps.gaissa_roi_analyzer.serializers import ModelArchitectureSerializer


class ModelArchitectureSerializerTest(TestCase):
    """Unit tests for ModelArchitecture serializer"""

    def setUp(self):
        """Set up test data"""
        self.model_arch_data = {
            'name': 'TestNet',
            'information': 'A test neural network architecture'
        }
        self.new_model_data = {
            'name': 'NewTestNet',
            'information': 'A new test neural network architecture'
        }
        self.model_arch = ModelArchitecture.objects.create(**self.model_arch_data)

    def test_model_architecture_serializer_valid_data(self):
        """Test serializer with valid data"""
        serializer = ModelArchitectureSerializer(data=self.new_model_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_model_architecture_serializer_invalid_data(self):
        """Test serializer with invalid data (missing required name)"""
        invalid_data = {'information': 'Missing name field'}
        serializer = ModelArchitectureSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
