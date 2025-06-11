import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal

from apps.gaissa_roi_analyzer.models import *
from apps.core.models import Country, Administrador
from apps.gaissa_roi_analyzer.models import ROIAnalysisCalculation, AnalysisMetricValue, EnergyAnalysisMetricValue

User = get_user_model()


class TestGAISSAAPISetup(TestCase):
    """Shared setup for API integration tests"""
    
    def setUp(self):
        """Set up test data and authentication for API tests"""
        self.client = APIClient()
        
        # Create users with different permission levels
        fake_email = f"{str(uuid.uuid4())}@test.com"
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email=fake_email,
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create Administrador instance for admin permissions
        self.admin_profile = Administrador.objects.create(
            user=self.admin_user,
        )
        
        fake_email_regular = f"{str(uuid.uuid4())}@test.com"
        self.regular_user = User.objects.create_user(
            username='regular_user',
            email=fake_email_regular,
            password='testpass123'
        )
        
        # Create basic test data
        self.country = Country.objects.create(name="Spain", country_code="ES")
        
        self.model_arch = ModelArchitecture.objects.create(
            name="ResNet50",
            information="Deep residual network"
        )
        
        self.tactic_source = TacticSource.objects.create(
            title="Test Research Paper",
            url="https://arxiv.org/abs/1234.5678"
        )
        
        self.energy_metric = ROIMetric.objects.create(
            name="Energy Consumption",
            unit="W",
            is_energy_related=True,
            min_value=0.0,
            max_value=2000.0
        )
        
        self.time_metric = ROIMetric.objects.create(
            name="Inference Time",
            unit="ms",
            is_energy_related=False,
            min_value=0.0,
            max_value=1000.0
        )
        
        self.ml_tactic = MLTactic.objects.create(
            name="Weight Pruning",
            information="Neural network pruning"
        )
        self.ml_tactic.sources.add(self.tactic_source)
        self.ml_tactic.compatible_architectures.add(self.model_arch)
        self.ml_tactic.applicable_metrics.add(self.energy_metric, self.time_metric)
        
        self.param_option = TacticParameterOption.objects.create(
            tactic=self.ml_tactic,
            name="sparsity",
            value="0.5"
        )
        
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
            metric=self.time_metric,
            expectedReductionValue=0.20
        )

    def authenticate_as_admin(self):
        """Helper to authenticate as admin user"""
        try:
            # Try JWT authentication first
            refresh = RefreshToken.for_user(self.admin_user)
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        except:
            # Fallback to force_authenticate if JWT is not properly configured
            self.client.force_authenticate(user=self.admin_user)

    def authenticate_as_regular_user(self):
        """Helper to authenticate as regular user"""
        try:
            # Try JWT authentication first
            refresh = RefreshToken.for_user(self.regular_user)
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        except:
            # Fallback to force_authenticate if JWT is not properly configured
            self.client.force_authenticate(user=self.regular_user)

    def logout(self):
        """Helper to logout"""
        self.client.credentials()
        self.client.force_authenticate(user=None)

    def create_additional_test_data(self):
        """Helper to create additional test data for more comprehensive tests"""
        # Create additional model architectures
        self.model_arch_2 = ModelArchitecture.objects.create(
            name="VGG16",
            information="Visual Geometry Group architecture"
        )
        
        # Create additional tactics
        self.quantization_tactic = MLTactic.objects.create(
            name="Quantization",
            information="Reduce precision of weights and activations"
        )
        self.quantization_tactic.sources.add(self.tactic_source)
        self.quantization_tactic.compatible_architectures.add(self.model_arch, self.model_arch_2)
        self.quantization_tactic.applicable_metrics.add(self.energy_metric)
        
        # Create additional metrics
        self.accuracy_metric = ROIMetric.objects.create(
            name="Accuracy",
            unit="%",
            is_energy_related=False,
            min_value=0.0,
            max_value=100.0
        )
        
        # Create additional parameter options
        self.quantization_param = TacticParameterOption.objects.create(
            tactic=self.quantization_tactic,
            name="bits",
            value="8"
        )
        
        # Create additional expected reductions
        self.expected_reduction_quantization = ExpectedMetricReduction.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.quantization_param,
            metric=self.energy_metric,
            expectedReductionValue=0.25
        )

    def create_roi_analysis_data(self):
        """Helper to create ROI analysis test data"""
        
        # Create a calculation analysis using ROIAnalysisCalculation
        self.roi_analysis = ROIAnalysisCalculation.objects.create(
            model_architecture=self.model_arch,
            tactic_parameter_option=self.param_option,
            country=self.country
        )
        
        # Add metric values using EnergyAnalysisMetricValue for energy metrics
        self.analysis_metric_energy = EnergyAnalysisMetricValue.objects.create(
            analysis=self.roi_analysis,
            metric=self.energy_metric,
            baselineValue=100.0,
            energy_cost_rate=0.20,
            implementation_cost=1000.0
        )
        
        # Add metric values using regular AnalysisMetricValue for non-energy metrics
        self.analysis_metric_time = AnalysisMetricValue.objects.create(
            analysis=self.roi_analysis,
            metric=self.time_metric,
            baselineValue=50.0
        )

    def assertResponseHasFields(self, response_data, expected_fields):
        """Helper to assert response has expected fields"""
        for field in expected_fields:
            self.assertIn(field, response_data, f"Field '{field}' missing from response")

    def assertValidationError(self, response, field_name=None):
        """Helper to assert validation error response"""
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        if field_name:
            self.assertIn(field_name, response.data)