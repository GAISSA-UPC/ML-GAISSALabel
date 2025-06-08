from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    ModelArchitecture, TacticSource, MLTactic, TacticParameterOption, 
    ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch, ROIMetric, 
    AnalysisMetricValue, EnergyAnalysisMetricValue, ExpectedMetricReduction
)
from .serializers import (
    ModelArchitectureSerializer, TacticSourceSerializer, MLTacticSerializer, 
    TacticParameterOptionSerializer, ROIAnalysisSerializer, AnalysisListSerializer, 
    ROIAnalysisCalculationSerializer, ROIAnalysisResearchSerializer, ROIMetricSerializer,
    AnalysisMetricValueSerializer, EnergyAnalysisMetricValueSerializer, 
    ExpectedMetricReductionSerializer
)
from apps.core.models import Country, CarbonIntensity
from apps.core.serializers import CountrySerializer, CarbonIntensitySerializer
from apps.core import permissions


class ModelArchitectureView(viewsets.ModelViewSet):
    """ViewSet for ML model architectures in ROI analysis."""
    queryset = ModelArchitecture.objects.all()
    serializer_class = ModelArchitectureSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'information']
    ordering_fields = ['name']

    def get_queryset(self):
        """Filter model architectures by analysis type if analysis_type parameter is provided."""
        queryset = super().get_queryset()
        
        analysis_type = self.request.query_params.get('analysis_type')
        if analysis_type:
            if analysis_type == 'calculation':
                queryset = queryset.filter(roi_analyses__roianalysiscalculation__isnull=False).distinct()
            elif analysis_type == 'research':
                queryset = queryset.filter(roi_analyses__roianalysisresearch__isnull=False).distinct()
                
        return queryset
    
    @action(detail=True, methods=['get'], url_path='compatible-tactics')
    def get_compatible_tactics(self, request, pk=None):
        """Get compatible tactics for a specific architecture."""
        architecture = self.get_object()
        compatible_tactics = architecture.compatible_tactics.all()
                
        # Filter by analysis type if analysis_type parameter is provided
        analysis_type = self.request.query_params.get('analysis_type')
        if analysis_type:
            if analysis_type == 'calculation':
                # Filter to include only tactics that have calculation analyses with this architecture
                compatible_tactics = compatible_tactics.filter(
                    parameter_options__roi_analyses__model_architecture=architecture,
                    parameter_options__roi_analyses__roianalysiscalculation__isnull=False
                ).distinct()
            elif analysis_type == 'research':
                # Filter to include only tactics that have research analyses with this architecture
                compatible_tactics = compatible_tactics.filter(
                    parameter_options__roi_analyses__model_architecture=architecture,
                    parameter_options__roi_analyses__roianalysisresearch__isnull=False
                ).distinct()
        
        # Serialize the tactics and return them
        serializer = MLTacticSerializer(compatible_tactics, many=True)
        return Response(serializer.data)


class TacticSourceView(viewsets.ModelViewSet):
    """ViewSet for tactic sources/references."""
    queryset = TacticSource.objects.all()
    serializer_class = TacticSourceSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'url']
    search_fields = ['title', 'url']
    ordering_fields = ['title']


class MLTacticView(viewsets.ModelViewSet):
    """ViewSet for ML optimization tactics."""
    queryset = MLTactic.objects.all()
    serializer_class = MLTacticSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'sources']
    search_fields = ['name', 'information']
    ordering_fields = ['name']

    @action(detail=True, methods=['get'], url_path='applicable-metrics')
    def get_applicable_metrics(self, request, pk=None):
        """Get applicable metrics for a specific tactic."""
        tactic = self.get_object()
        applicable_metrics = tactic.applicable_metrics.all()
        
        # Serialize the metrics and return them
        serializer = ROIMetricSerializer(applicable_metrics, many=True)
        return Response(serializer.data)


class TacticParameterOptionView(viewsets.ModelViewSet):
    """ViewSet for tactic parameter options."""
    queryset = TacticParameterOption.objects.all()
    serializer_class = TacticParameterOptionSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'tactic', 'name', 'value']
    search_fields = ['name', 'value', 'tactic__name']
    ordering_fields = ['tactic__name', 'name', 'value']

    def get_queryset(self):
        queryset = super().get_queryset()
        tactic_id = self.kwargs.get('tactic_id')
        
        if tactic_id is not None:
            queryset = queryset.filter(tactic_id=tactic_id)
        
        # Check for model_architecture_id in query parameters to filter by ExpectedMetricReduction
        model_architecture_id = self.request.query_params.get('model_architecture')
        if model_architecture_id and tactic_id:
            # Filter to only return parameter options that have an associated ExpectedMetricReduction
            # for the specified model architecture and tactic combination
            parameter_options_with_reductions = ExpectedMetricReduction.objects.filter(
                model_architecture_id=model_architecture_id,
                tactic_parameter_option__tactic_id=tactic_id
            ).values_list('tactic_parameter_option_id', flat=True).distinct()
            
            queryset = queryset.filter(id__in=parameter_options_with_reductions)
        
        # Filter by analysis type if analysis_type parameter is provided
        analysis_type = self.request.query_params.get('analysis_type')
        if analysis_type:
            if analysis_type == 'calculation':
                # Filter to include only parameter options that have calculation analyses with this tactic
                queryset = queryset.filter(roi_analyses__roianalysiscalculation__isnull=False).distinct()
            elif analysis_type == 'research':
                # Filter to include only parameter options that have research analyses with this tactic
                queryset = queryset.filter(roi_analyses__roianalysisresearch__isnull=False).distinct()
        return queryset


class ROIMetricView(viewsets.ModelViewSet):
    """ViewSet for ROI metrics."""
    queryset = ROIMetric.objects.all()
    serializer_class = ROIMetricSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'unit']
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class ROIAnalysisViewSet(viewsets.ModelViewSet):
    """ViewSet for ROI analyses."""
    queryset = ROIAnalysis.objects.all().order_by('-roianalysiscalculation__dateRegistration', '-id')
    
    # Allow anyone to create ROI analyses, for other actions use default permissions
    def get_permissions(self):
        if self.action == 'create':
            # Anyone can create, but ROI must be enabled
            return [permissions.IsGAISSAROIAnalyzerEnabled()]
        else:
            # For other actions, both conditions must be met
            return [permissions.IsAdminEditOthersRead(), permissions.IsGAISSAROIAnalyzerEnabled()]
        
    def get_queryset(self):
        """Filter analyses by type if analysis_type parameter is provided."""
        queryset = super().get_queryset()
        analysis_type = self.request.query_params.get('analysis_type')
        
        if analysis_type:
            if analysis_type == 'calculation':
                # Filter to include only ROIAnalysisCalculation instances
                queryset = queryset.filter(roianalysiscalculation__isnull=False)
            elif analysis_type == 'research':
                # Filter to include only ROIAnalysisResearch instances
                queryset = queryset.filter(roianalysisresearch__isnull=False)
                
        return queryset
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'model_architecture': ['exact'],
        'tactic_parameter_option': ['exact'],
        'tactic_parameter_option__tactic': ['exact'],
        'metric_values__metric': ['exact'],
        'country': ['exact'],
        'country__name': ['exact', 'icontains'],
        'roianalysiscalculation__dateRegistration': ['date__gte', 'date__lte'],
    }
    search_fields = [
        'model_architecture__name',
        'tactic_parameter_option__tactic__name',
        'tactic_parameter_option__name',
        'tactic_parameter_option__value',
        'country__name'
    ]
    ordering_fields = ['id', 'model_architecture__name', 'tactic_parameter_option__tactic__name', 
                      'roianalysiscalculation__dateRegistration']
    ordering = ('-roianalysiscalculation__dateRegistration', '-id')

    def get_serializer_class(self):
        # Use AnalysisListSerializer for list view to improve readability
        if self.action == 'list':
            return AnalysisListSerializer
        
        # For create, update, partial_update operations
        if self.action in ['create', 'update', 'partial_update']:
            analysis_type = self.request.data.get('analysis_type', 'calculation')
            
            # If no analysis_type is provided, determine type by looking at provided fields
            if not analysis_type:
                if 'source_id' in self.request.data:
                    analysis_type = 'research'
                else:
                    analysis_type = 'calculation'

            if analysis_type == 'calculation':
                return ROIAnalysisCalculationSerializer
            elif analysis_type == 'research':
                return ROIAnalysisResearchSerializer
            
        # For retrieve operations
        if self.action == 'retrieve':
            instance = self.get_object()
            if hasattr(instance, 'roianalysiscalculation'):
                return ROIAnalysisCalculationSerializer
            elif hasattr(instance, 'roianalysisresearch'):
                return ROIAnalysisResearchSerializer
            
        return ROIAnalysisSerializer
        
    def get_object(self):
        obj = super().get_object()
        if hasattr(obj, 'roianalysiscalculation'):
            return obj.roianalysiscalculation
        elif hasattr(obj, 'roianalysisresearch'):
            return obj.roianalysisresearch
        return obj
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        
        # Allow custom number of inferences for cost savings calculations
        num_inferences = self.request.query_params.get('num_inferences')
        if num_inferences:
            try:
                context['num_inferences'] = int(num_inferences)
            except ValueError:
                pass  # Use the default value
        
        return context


class AnalysisMetricValueView(viewsets.ModelViewSet):
    """ViewSet for analysis metric values."""
    queryset = AnalysisMetricValue.objects.all()
    serializer_class = AnalysisMetricValueSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis', 'metric']
    ordering_fields = ['analysis', 'metric']


class EnergyAnalysisMetricValueView(viewsets.ModelViewSet):
    """ViewSet for energy analysis metric values."""
    queryset = EnergyAnalysisMetricValue.objects.all()
    serializer_class = EnergyAnalysisMetricValueSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis', 'metric']
    ordering_fields = ['analysis', 'metric']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        
        # Allow custom number of inferences for cost savings calculations
        num_inferences = self.request.query_params.get('num_inferences')
        if num_inferences:
            try:
                context['num_inferences'] = int(num_inferences)
            except ValueError:
                pass  # Use the default value
        
        return context


class ExpectedMetricReductionView(viewsets.ModelViewSet):
    """ViewSet for expected metric reductions."""
    queryset = ExpectedMetricReduction.objects.all()
    serializer_class = ExpectedMetricReductionSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['model_architecture', 'tactic_parameter_option', 'metric']
    ordering_fields = ['model_architecture', 'tactic_parameter_option', 'metric']


class CountryView(viewsets.ModelViewSet):
    """API endpoint for countries list (ROI analyzer context)."""
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country_code']
    ordering_fields = ['name', 'country_code']


class CarbonIntensityView(viewsets.ModelViewSet):
    """API endpoint for carbon intensity data (ROI analyzer context)."""
    queryset = CarbonIntensity.objects.all()
    serializer_class = CarbonIntensitySerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['country', 'data_year']
    ordering_fields = ['country', 'carbon_intensity', 'data_year']
