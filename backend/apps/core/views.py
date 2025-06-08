import pytz
from rest_framework import viewsets, mixins, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Administrador, Configuracio, Country, CarbonIntensity
from .serializers import LoginAdminSerializer, ConfiguracioSerializer, CountrySerializer, CarbonIntensitySerializer
from . import permissions


class LoginAdminView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Admin login view for authentication."""
    queryset = Administrador.objects.all()
    serializer_class = LoginAdminSerializer
    models = Administrador


class ConfiguracioView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """Configuration singleton view."""
    queryset = Configuracio.objects.all()
    serializer_class = ConfiguracioSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    
    def get_object(self):
        """Return the singleton configuration object."""
        return Configuracio.objects.get_or_create()[0]


class CountryView(viewsets.ModelViewSet):
    """API endpoint for countries list."""
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country_code']
    ordering_fields = ['name', 'country_code']


class CarbonIntensityView(viewsets.ModelViewSet):
    """API endpoint for carbon intensity data."""
    queryset = CarbonIntensity.objects.all()
    serializer_class = CarbonIntensitySerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['country', 'data_year']
    ordering_fields = ['country', 'carbon_intensity', 'data_year']
