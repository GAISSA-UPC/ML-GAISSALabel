from rest_framework import routers
from django.urls import path, include
from controllers import views

router = routers.DefaultRouter()

# GAISSALabel URLs
router.register(r'models', views.ModelsView, basename='models')
router.register(r'models/(?P<model_id>\d+)/entrenaments', views.EntrenamentsView, basename='entrenaments')
router.register(r'models/(?P<model_id>\d+)/inferencies', views.InferenciesView, basename='inferencies')
router.register(r'qualificacions', views.QualificacionsView, basename='qualificacions')
router.register(r'metriques', views.MetriquesView, basename='metriques')
router.register(r'informacions', views.InfoAddicionalsView, basename='informacions_addicionals')
router.register(r'calculadors/inferencia', views.CalculadorInferenciaView, basename='calculador_inferencia')
router.register(r'eines', views.EinesCalculView, basename='eines_calcul')
router.register(r'login/admins', views.LoginAdminView, basename='login_admins')
router.register(r'sincronitzacio', views.SincroView, basename='sincro')
router.register(r'estadistiques', views.EstadistiquesView, basename='estadistiques')

# GAISSA ROI Analyzer URLs
router.register(r'roi/architectures', views.ModelArchitectureView, basename='roi_architectures')
router.register(r'roi/sources', views.TacticSourceView, basename='roi_sources')
router.register(r'roi/tactics', views.MLTacticView, basename='roi_tactics')
router.register(r'roi/tactic-parameter-options', views.TacticParameterOptionView, basename='roi_tactic_parameter_options')
router.register(r'roi/tactics/(?P<tactic_id>\d+)/parameter-options', views.TacticParameterOptionView, basename='roi_tactic_parameters')
router.register(r'roi/metrics', views.ROIMetricView, basename='roi_metrics')
router.register(r'roi/analyses', views.ROIAnalysisViewSet, basename='roi_analyses')
router.register(r'roi/analysis-metric-values', views.AnalysisMetricValueView, basename='roi_analysis_metric_values')
router.register(r'roi/expected-reductions', views.ExpectedMetricReductionView, basename='roi_expected_reductions')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
