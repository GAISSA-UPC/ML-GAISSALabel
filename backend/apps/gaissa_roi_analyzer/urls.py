from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

# GAISSA ROI Analyzer URLs
router.register(r'pipeline-stages', views.MLPipelineStageView, basename='roi_pipeline_stages')
router.register(r'model-architectures', views.ModelArchitectureView, basename='roi_model_architectures')
router.register(r'sources', views.TacticSourceView, basename='roi_sources')
router.register(r'tactics', views.MLTacticView, basename='roi_tactics')
router.register(r'tactic-parameter-options', views.TacticParameterOptionView, basename='roi_tactic_parameter_options')
router.register(r'tactics/(?P<tactic_id>\d+)/parameter-options', views.TacticParameterOptionView, basename='roi_tactic_parameters')
router.register(r'metrics', views.ROIMetricView, basename='roi_metrics')
router.register(r'analyses', views.ROIAnalysisViewSet, basename='roi_analyses')
router.register(r'analysis-metric-values', views.AnalysisMetricValueView, basename='roi_analysis_metric_values')
router.register(r'energy-metric-values', views.EnergyAnalysisMetricValueView, basename='roi_energy_metric_values')
router.register(r'expected-reductions', views.ExpectedMetricReductionView, basename='roi_expected_reductions')

urlpatterns = [
    path('statistics/', views.statistics_view, name='roi_statistics'),
    path('', include(router.urls)),
]
