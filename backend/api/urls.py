from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'models', views.ModelsView, basename='models')
router.register(r'models/(?P<model_id>\d+)/entrenaments', views.EntrenamentsView, basename='entrenaments')
router.register(r'models/(?P<model_id>\d+)/inferencies', views.InferenciesView, basename='inferencies')
router.register(r'metriques', views.MetriquesView, basename='metriques')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
