from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.gaissa_roi_analyzer.models import ModelArchitecture


class ModelArchitectureModelTest(TestCase):
    """Unit tests for ModelArchitecture model"""

    def setUp(self):
        """Set up test data"""
        self.model_arch = ModelArchitecture.objects.create(
            name="TestNet",
            information="A test neural network architecture"
        )

    def test_model_architecture_creation(self):
        """Test that a ModelArchitecture can be created successfully"""
        self.assertEqual(self.model_arch.name, "TestNet")
        self.assertEqual(self.model_arch.information, "A test neural network architecture")
        self.assertTrue(isinstance(self.model_arch, ModelArchitecture))

    def test_model_architecture_str_representation(self):
        """Test the string representation of ModelArchitecture"""
        self.assertEqual(str(self.model_arch), "TestNet")

    def test_model_architecture_unique_name(self):
        """Test that ModelArchitecture names must be unique"""
        with self.assertRaises(Exception):
            ModelArchitecture.objects.create(name="TestNet")
