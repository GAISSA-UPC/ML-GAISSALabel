from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.gaissa_roi_analyzer.models import ModelArchitecture


class ModelArchitectureViewTest(TestCase):
    """Unit tests for ModelArchitecture ViewSet"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.model_arch = ModelArchitecture.objects.create(
            name="TestNet",
            information="A test neural network architecture"
        )

    def test_get_model_architectures_list(self):
        """Test retrieving list of model architectures"""
        response = self.client.get('/api/roi/model-architectures/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "TestNet")

    def test_get_model_architecture_detail(self):
        """Test retrieving a specific model architecture"""
        response = self.client.get(f'/api/roi/model-architectures/{self.model_arch.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "TestNet")
