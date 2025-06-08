from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

# Core app URLs
router.register(r'login/admins', views.LoginAdminView, basename='login_admins')
router.register(r'countries', views.CountryView, basename='countries')
router.register(r'carbon-intensities', views.CarbonIntensityView, basename='carbon_intensities')

urlpatterns = [
    path('', include(router.urls)),
    # Add explicit path for configuracio since it's a singleton
    path('configuracio/', views.ConfiguracioView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'})),
]
