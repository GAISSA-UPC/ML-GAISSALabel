import base64
import pytz
from rest_framework import viewsets, filters, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Model, Entrenament, Inferencia, Metrica, InfoAddicional, 
    Qualificacio, Interval, EinaCalcul, TransformacioMetrica, 
    TransformacioInformacio
)
from .serializers import (
    ModelSerializer, EntrenamentSerializer, InferenciaSerializer, 
    MetricaAmbLimitsSerializer, EntrenamentAmbResultatSerializer, 
    InferenciaAmbResultatSerializer, InfoAddicionalSerializer, 
    QualificacioSerializer, IntervalBasicSerializer, MetricaSerializer, 
    EinaCalculBasicSerializer, EinaCalculSerializer, TransformacioMetricaSerializer, 
    TransformacioInformacioSerializer
)
from .calculators.rating_calculator import calculateRating
from .calculators.label_generator import generateLabel
from .calculators.efficiency_calculator import calculateEfficiency
from apps.core.models import Configuracio
from api import permissions
from connectors import adaptador_huggingface


class ModelsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet for ML models in GAISSALabel."""
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    models = Model
    permission_classes = [permissions.IsGAISSALabelEnabled]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'id': ['exact', 'in'],
        'nom': ['exact', 'in', 'contains'],
    }
    search_fields = ['nom']
    ordering_fields = ['nom', 'dataCreacio']

    def get_queryset(self):
        queryset = super().get_queryset()
        has_roi_analysis = self.request.query_params.get('has_roi_analysis')
        if has_roi_analysis == 'true':
            queryset = queryset.filter(gaissa_roi_analyses__isnull=False).distinct()
        return queryset


class EntrenamentsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet for training sessions in GAISSALabel."""
    models = Entrenament
    serializer_class = EntrenamentSerializer
    permission_classes = [permissions.IsGAISSALabelEnabled]

    def get_queryset(self):
        # Get the model from the parameter
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, id=model_id)

        # Filter to get corresponding training sessions
        return Entrenament.objects.select_related('model').all().filter(model=model)

    def get_serializer_class(self):
        # For retrieve or create, return full info with results
        if self.action == 'retrieve' or self.action == 'create':
            return EntrenamentAmbResultatSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        # Get training values to generate Energy Label
        entrenament = self.get_object()
        entrenament_data = self.get_serializer(entrenament).data
        resultats_entrenament = entrenament_data['resultats']

        # Get metric information (training phase and with weight)
        metriques = Metrica.objects.filter(fase=Metrica.TRAIN).order_by('-pes').exclude(pes=0)

        # Calculate ratings (with adapter)
        qualifFinal, qualifMetriques = calculateRating(resultats_entrenament, metriques)

        # Generate label and results (with adapter)
        label, resultatsResponse = generateLabel(qualifFinal, qualifMetriques, resultats_entrenament, entrenament.model, entrenament.id, 'Training')

        # Prepare response data for client
        response_data = {
            'energy_label': base64.b64encode(label).decode(),
            'resultats': resultatsResponse,
            'infoEntrenament': entrenament_data
        }
        return Response(response_data)

    def create(self, request, model_id=None, *args, **kwargs):
        # Add model id from parameter to request data before creating
        data = request.data.copy()
        data['model'] = model_id

        # Equivalent to super().create, but with "data"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InferenciesView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet for inference sessions in GAISSALabel."""
    models = Inferencia
    serializer_class = InferenciaSerializer
    permission_classes = [permissions.IsGAISSALabelEnabled]

    def get_queryset(self):
        # Get the model from the parameter
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, id=model_id)

        # Filter to get corresponding inferences
        return Inferencia.objects.select_related('model').all().filter(model=model)

    def get_serializer_class(self):
        # For retrieve or create, return full info with results
        if self.action == 'retrieve' or self.action == 'create':
            return InferenciaAmbResultatSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        # Get inference values to generate Energy Label
        inferencia = self.get_object()
        inference_data = self.get_serializer(inferencia).data
        resultats_inferencia = inference_data['resultats']

        # Get metric information (inference phase and with weight)
        metriques = Metrica.objects.filter(fase=Metrica.INF).order_by('-pes').exclude(pes=0)

        # Calculate ratings (with adapter)
        qualifFinal, qualifMetriques = calculateRating(resultats_inferencia, metriques)

        # Generate label and results (with adapter)
        label, resultatsResponse = generateLabel(qualifFinal, qualifMetriques, resultats_inferencia, inferencia.model, inferencia.id, 'Inference')

        # Prepare response data for client
        response_data = {
            'energy_label': base64.b64encode(label).decode(),
            'resultats': resultatsResponse,
            'infoInferencia': inference_data
        }
        return Response(response_data)

    def create(self, request, model_id=None, *args, **kwargs):
        # Add inference id from parameter to request data before creating
        data = request.data.copy()
        data['model'] = model_id

        # Equivalent to super().create, but with "data"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class QualificacionsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet for qualification/rating levels."""
    models = Qualificacio
    serializer_class = QualificacioSerializer
    queryset = Qualificacio.objects.all()
    permission_classes = [permissions.IsGAISSALabelEnabled]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['ordre']


class MetriquesView(viewsets.ModelViewSet):
    """ViewSet for metrics configuration."""
    models = Metrica
    queryset = Metrica.objects.all()
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSALabelEnabled]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'id': ['exact', 'in'],
        'nom': ['exact', 'in', 'contains'],
        'fase': ['exact', 'in'],
        'pes': ['exact', 'range'],
        'influencia': ['exact', 'in']
    }
    search_fields = ['nom', 'fase']
    ordering_fields = ['id', 'nom', 'fase', 'pes', 'influencia']

    def get_serializer_class(self):
        if self.action == 'create':
            return MetricaSerializer
        else:
            return MetricaAmbLimitsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        metrica = self.get_object()
        data = request.data.copy()

        # Update intervals (get instance and modify with given values)
        intervals = data.pop('intervals')
        for intervalJSON in intervals:
            interval = Interval.objects.get(metrica=metrica, qualificacio__id=intervalJSON['qualificacio'])
            serializer = IntervalBasicSerializer(interval, data=intervalJSON, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # Update metric (equivalent to super.update() with small modifications)
        serializer = self.get_serializer(metrica, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class InfoAddicionalsView(viewsets.ModelViewSet):
    """ViewSet for additional information configuration."""
    model = InfoAddicional
    serializer_class = InfoAddicionalSerializer
    queryset = InfoAddicional.objects.all()
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSALabelEnabled]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'id': ['exact', 'in'],
        'nom': ['exact', 'in', 'contains'],
        'fase': ['exact', 'in'],
    }
    search_fields = ['nom', 'fase']
    ordering_fields = ['id', 'nom', 'fase']


class CalculadorInferenciaView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet for inference calculator."""
    permission_classes = [permissions.IsGAISSALabelEnabled]
    
    def get_serializer_class(self):
        pass

    def create(self, request, *args, **kwargs):
        endpoint = request.data.get('endpoint')
        data = request.data.get('input')
        if not endpoint or not data:
            return Response("Cal donar els atributs endpoint i input!", status=status.HTTP_400_BAD_REQUEST)
        resultats = calculateEfficiency(endpoint, data)
        return Response(resultats, status=status.HTTP_201_CREATED)


class EinesCalculView(viewsets.ModelViewSet):
    """ViewSet for calculation tools configuration."""
    models = EinaCalcul
    queryset = EinaCalcul.objects.all()
    serializer_class = EinaCalculSerializer
    permission_classes = [permissions.IsAdminEditOthersRead & permissions.IsGAISSALabelEnabled]

    def get_serializer_class(self):
        if self.action == 'create':
            return EinaCalculBasicSerializer
        else:
            return EinaCalculSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        eina = self.get_object()
        data = request.data.copy()

        # Update metric transformations (get instance and modify with given values)
        TransformacioMetrica.objects.filter(eina=eina).delete()
        transfMetriques = data.pop('transformacionsMetriques', None)
        if transfMetriques:
            for transfMetricaJSON in transfMetriques:
                metrica = get_object_or_404(Metrica, id=transfMetricaJSON['metrica'])
                transfMetrica, created = TransformacioMetrica.objects.get_or_create(eina=eina, metrica=metrica)
                serializer = TransformacioMetricaSerializer(transfMetrica, data=transfMetricaJSON, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        # Update information transformations (get instance and modify with given values)
        TransformacioInformacio.objects.filter(eina=eina).delete()
        transfInformacions = data.pop('transformacionsInformacions', None)
        if transfInformacions:
            for transfInfoJSON in transfInformacions:
                informacio = get_object_or_404(InfoAddicional, id=transfInfoJSON['informacio'])
                transfInfo, created = TransformacioInformacio.objects.get_or_create(eina=eina, informacio=informacio)
                serializer = TransformacioInformacioSerializer(transfInfo, data=transfInfoJSON, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        # Update tool (equivalent to super.update() with small modifications)
        serializer = self.get_serializer(eina, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class SincroView(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet for synchronization with external providers."""
    permission_classes = [permissions.IsAdmin & permissions.IsGAISSALabelEnabled]

    def get_serializer_class(self):
        pass

    def list(self, request, *args, **kwargs):
        ultimaSincro = Configuracio.objects.get(id=1).ultimaSincronitzacio
        ultimaSincroFormatted = ultimaSincro.astimezone(pytz.timezone('Europe/Madrid')).strftime('%d-%m-%Y at %H:%M:%S')
        return Response({'Last update': ultimaSincroFormatted,
                         'Providers': ['Hugging Face']},
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        creats, actualitzats = adaptador_huggingface.sincro_huggingFace()
        if creats == 'KO':
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Created models': creats, 'Updated models': actualitzats}, status=status.HTTP_200_OK)


class EstadistiquesView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet for GAISSALabel statistics."""
    permission_classes = [permissions.IsGAISSALabelEnabled]
    
    def get_serializer_class(self):
        pass

    def list(self, request, *args, **kwargs):
        data = {
            "numModels": Model.objects.count(),
            "numEntrenaments": Entrenament.objects.count(),
            "numInferencies": Inferencia.objects.count(),
        }
        return Response(data, status=status.HTTP_200_OK)
