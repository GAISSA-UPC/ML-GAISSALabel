from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'models', views.ModelsView, basename='models')
router.register(r'models/(?P<model_id>\d+)/entrenaments', views.EntrenamentsView, basename='entrenaments')
router.register(r'models/(?P<model_id>\d+)/inferencies', views.InferenciesView, basename='inferencies')
router.register(r'qualificacions', views.QualificacionsView, basename='qualificacions')
router.register(r'metriques', views.MetriquesView, basename='metriques')
router.register(r'informacions', views.InfoAddicionalsView, basename='informacions addicionals')
router.register(r'calculadors/inferencia', views.CalculadorInferenciaView, basename='calculador inferencia')
router.register(r'eines', views.EinesCalculView, basename='eines càlcul')
router.register(r'transformacions/metriques', views.TransformacioMetriquesView, basename='transformacions mètriques')
router.register(r'transformacions/informacions', views.TransformacioInformacionsView, basename='transformacions informacions')
router.register(r'login/admins', views.LoginAdminView, basename='login admins')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
