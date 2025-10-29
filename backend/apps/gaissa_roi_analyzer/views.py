from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    MLPipelineStage, ModelArchitecture, TacticSource, MLTactic, TacticParameterOption, 
    ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch, ROIMetric, 
    AnalysisMetricValue, EnergyAnalysisMetricValue, ExpectedMetricReduction
)
from .serializers import (
    MLPipelineStageSerializer, ModelArchitectureSerializer, TacticSourceSerializer, MLTacticSerializer, 
    TacticParameterOptionSerializer, ROIAnalysisSerializer, AnalysisListSerializer, 
    ROIAnalysisCalculationSerializer, ROIAnalysisResearchSerializer, ROIMetricSerializer,
    AnalysisMetricValueSerializer, EnergyAnalysisMetricValueSerializer, 
    ExpectedMetricReductionSerializer
)
from apps.core import permissions


class MLPipelineStageView(viewsets.ModelViewSet):
    """ViewSet for ML pipeline stages."""
    queryset = MLPipelineStage.objects.all()
    serializer_class = MLPipelineStageSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name']
    ordering = ['id']


class ModelArchitectureView(viewsets.ModelViewSet):
    """ViewSet for ML model architectures in ROI analysis."""
    queryset = ModelArchitecture.objects.all()
    serializer_class = ModelArchitectureSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'information']
    ordering_fields = ['id', 'name']
    ordering = ['id']

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
    ordering_fields = ['id', 'title']
    ordering = ['id']


class MLTacticView(viewsets.ModelViewSet):
    """ViewSet for ML optimization tactics."""
    queryset = MLTactic.objects.all()
    serializer_class = MLTacticSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'sources', 'pipeline_stage']
    search_fields = ['name', 'information']
    ordering_fields = ['id', 'name']
    ordering = ['id']

    def get_queryset(self):
        """Filter ML tactics by analysis type if analysis_type parameter is provided."""
        queryset = super().get_queryset()
        
        # Optimize: Use select_related for ForeignKey and prefetch_related for ManyToMany
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related('pipeline_stage').prefetch_related(
                'sources',
                'applicable_metrics',
                'compatible_architectures'
            )
        
        analysis_type = self.request.query_params.get('analysis_type')
        if analysis_type:
            if analysis_type == 'calculation':
                queryset = queryset.filter(
                    parameter_options__roi_analyses__roianalysiscalculation__isnull=False
                ).distinct()
            elif analysis_type == 'research':
                queryset = queryset.filter(
                    parameter_options__roi_analyses__roianalysisresearch__isnull=False
                ).distinct()
                
        return queryset

    @action(detail=True, methods=['get'], url_path='applicable-metrics')
    def get_applicable_metrics(self, request, pk=None):
        """Get applicable metrics for a specific tactic."""
        tactic = self.get_object()
        applicable_metrics = tactic.applicable_metrics.all().order_by('id')
        
        # Serialize the metrics and return them
        serializer = ROIMetricSerializer(applicable_metrics, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='compatible-architectures')
    def get_compatible_architectures(self, request, pk=None):
        """Get compatible model architectures for a specific tactic."""
        tactic = self.get_object()
        compatible_architectures = tactic.compatible_architectures.all()
        
        # Filter by analysis type if analysis_type parameter is provided
        analysis_type = self.request.query_params.get('analysis_type')
        if analysis_type:
            if analysis_type == 'calculation':
                # Filter to include only architectures that have calculation analyses with this tactic
                compatible_architectures = compatible_architectures.filter(
                    roi_analyses__tactic_parameter_option__tactic=tactic,
                    roi_analyses__roianalysiscalculation__isnull=False
                ).distinct()
            elif analysis_type == 'research':
                # Filter to include only architectures that have research analyses with this tactic
                compatible_architectures = compatible_architectures.filter(
                    roi_analyses__tactic_parameter_option__tactic=tactic,
                    roi_analyses__roianalysisresearch__isnull=False
                ).distinct()
        
        # Serialize the architectures and return them
        serializer = ModelArchitectureSerializer(compatible_architectures, many=True)
        return Response(serializer.data)


class TacticParameterOptionView(viewsets.ModelViewSet):
    """ViewSet for tactic parameter options."""
    queryset = TacticParameterOption.objects.all()
    serializer_class = TacticParameterOptionSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'tactic', 'name', 'value']
    search_fields = ['name', 'value', 'tactic__name']
    ordering_fields = ['id', 'tactic__name', 'name', 'value']
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Optimize: Use select_related for nested ForeignKeys (tactic and pipeline_stage)
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related('tactic', 'tactic__pipeline_stage')
        
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
        if analysis_type and model_architecture_id:
            if analysis_type == 'calculation':
                # Filter to include only parameter options that have calculation analyses 
                # for this specific model architecture
                queryset = queryset.filter(
                    roi_analyses__roianalysiscalculation__isnull=False,
                    roi_analyses__model_architecture_id=model_architecture_id
                ).distinct()
            elif analysis_type == 'research':
                # Filter to include only parameter options that have research analyses
                # for this specific model architecture
                queryset = queryset.filter(
                    roi_analyses__roianalysisresearch__isnull=False,
                    roi_analyses__model_architecture_id=model_architecture_id
                ).distinct()
        elif analysis_type:
            # If analysis_type is provided but no model_architecture, filter without architecture constraint
            if analysis_type == 'calculation':
                queryset = queryset.filter(roi_analyses__roianalysiscalculation__isnull=False).distinct()
            elif analysis_type == 'research':
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
    ordering_fields = ['id', 'name']
    ordering = ['id']


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
        
        # Optimize: Eagerly load all related data to avoid N+1 queries
        if self.action in ['list', 'retrieve']:
            # Use select_related for ForeignKey and OneToOne relationships
            queryset = queryset.select_related(
                'model_architecture',
                'tactic_parameter_option',
                'tactic_parameter_option__tactic',
                'tactic_parameter_option__tactic__pipeline_stage',
                'country',
                'roianalysiscalculation',
                'roianalysisresearch',
                'roianalysisresearch__source'
            )
            
            # Only prefetch metric_values for detail view (retrieve action)
            # AnalysisListSerializer doesn't use metric_values
            if self.action == 'retrieve':
                queryset = queryset.prefetch_related(
                    'metric_values',
                    'metric_values__metric',
                )
        
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
    ordering_fields = ['id', 'analysis', 'metric']
    ordering = ['id']
    
    def get_queryset(self):
        """Optimize queryset with select_related for related objects."""
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related('metric')
        return queryset


class EnergyAnalysisMetricValueView(viewsets.ModelViewSet):
    """ViewSet for energy analysis metric values."""
    queryset = EnergyAnalysisMetricValue.objects.all()
    serializer_class = EnergyAnalysisMetricValueSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSAROIAnalyzerEnabled]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis', 'metric']
    ordering_fields = ['id', 'analysis', 'metric']
    ordering = ['id']
    
    def get_queryset(self):
        """Optimize queryset with select_related for related objects."""
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            # Include nested relationships for the analysis
            queryset = queryset.select_related(
                'analysis',
                'analysis__model_architecture',
                'analysis__tactic_parameter_option',
                'metric'
            )
        return queryset
    
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
    ordering_fields = ['id', 'model_architecture', 'tactic_parameter_option', 'metric']
    ordering = ['id']
    
    def get_queryset(self):
        """Optimize queryset with select_related for related objects."""
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related(
                'model_architecture',
                'tactic_parameter_option',
                'tactic_parameter_option__tactic',  # For tactic_name in nested serializer
                'metric'
            )
        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsGAISSAROIAnalyzerEnabled])
def statistics_view(request):
    """Get aggregated statistics for the GAISSA ROI Analyzer."""
    # Total counts
    total_pipeline_stages = MLPipelineStage.objects.count()
    total_tactics = MLTactic.objects.count()
    total_research_analyses = ROIAnalysisResearch.objects.count()
    total_calculation_analyses = ROIAnalysisCalculation.objects.count()
    
    # Optimize: Prefetch pipeline_stage for tactics to avoid N+1 queries
    stages = MLPipelineStage.objects.all().prefetch_related(
        'tactics',  # Prefetch related tactics for each stage
    )
    stage_breakdown = []
    
    for stage in stages:
        # Use prefetched tactics instead of new query
        tactics_in_stage = stage.tactics.all()
        
        stage_data = {
            'id': stage.id,
            'name': stage.name,
            'tactics_count': tactics_in_stage.count(),  # Use prefetched data
            'research_analyses_count': ROIAnalysisResearch.objects.filter(
                tactic_parameter_option__tactic__pipeline_stage=stage
            ).count(),
            'calculation_analyses_count': ROIAnalysisCalculation.objects.filter(
                tactic_parameter_option__tactic__pipeline_stage=stage
            ).count(),
        }
        stage_breakdown.append(stage_data)
    
    return Response({
        'total_pipeline_stages': total_pipeline_stages,
        'total_tactics': total_tactics,
        'total_research_analyses': total_research_analyses,
        'total_calculation_analyses': total_calculation_analyses,
        'stage_breakdown': stage_breakdown
    })
