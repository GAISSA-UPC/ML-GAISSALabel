import base64
import pytz

from rest_framework import viewsets, filters, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from api.models import Model, Entrenament, Inferencia, Metrica, InfoAddicional, Qualificacio, Interval, EinaCalcul, \
    TransformacioMetrica, TransformacioInformacio, Administrador, Configuracio, \
    ModelArchitecture, TacticSource, MLTactic, TacticParameterOption, ROIAnalysis, ROIAnalysisCalculation, \
    ROIAnalysisResearch, ROIMetric, AnalysisMetricValue, ExpectedMetricReduction
from api.serializers import ModelSerializer, EntrenamentSerializer, InferenciaSerializer, MetricaAmbLimitsSerializer, \
    EntrenamentAmbResultatSerializer, InferenciaAmbResultatSerializer, InfoAddicionalSerializer, QualificacioSerializer, \
    IntervalBasicSerializer, MetricaSerializer, EinaCalculBasicSerializer, EinaCalculSerializer, \
    TransformacioMetricaSerializer, TransformacioInformacioSerializer, LoginAdminSerializer, \
    ModelArchitectureSerializer, TacticSourceSerializer, MLTacticSerializer, TacticParameterOptionSerializer, \
    ROIAnalysisSerializer, ROIAnalysisCalculationSerializer, ROIAnalysisResearchSerializer, ROIMetricSerializer, \
    AnalysisMetricValueSerializer, ExpectedMetricReductionSerializer

from api import permissions
from efficiency_calculators.rating_calculator import calculateRating
from efficiency_calculators.label_generator import generateLabel
from efficiency_calculators.efficiency_calculator import calculateEfficiency
from connectors import adaptador_huggingface

class ModelsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    models = Model

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
    models = Entrenament
    serializer_class = EntrenamentSerializer

    def get_queryset(self):
        # Aconseguim el model que ens arriba del paràmetre
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, id=model_id)

        # Filtrem per obtenir l'entrenament corresponent
        return Entrenament.objects.select_related('model').all().filter(model=model)

    def get_serializer_class(self):
        # En cas que sigui retrieve, retornem tota la info, amb el resultat
        if self.action == 'retrieve' or self.action == 'create':
            return EntrenamentAmbResultatSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        # Aconseguir valors de l'entrenament a generar la EL
        entrenament = self.get_object()
        entrenament_data = self.get_serializer(entrenament).data
        resultats_entrenament = entrenament_data['resultats']

        # Aconseguir informació de les mètriques (de training i que tinguin pes)
        metriques = Metrica.objects.filter(fase=Metrica.TRAIN).order_by('-pes').exclude(pes=0)

        # Calcular ratings (amb adaptador)
        qualifFinal, qualifMetriques = calculateRating(resultats_entrenament, metriques)

        # Generar etiqueta i resultats (amb adaptador)
        label, resultatsResponse = generateLabel(qualifFinal, qualifMetriques, resultats_entrenament, entrenament.model, entrenament.id, 'Training')

        # Preparar les dades que es responen al client
        response_data = {
            'energy_label': base64.b64encode(label).decode(),
            'resultats': resultatsResponse,
            'infoEntrenament': entrenament_data
        }
        return Response(response_data)

    def create(self, request, model_id=None, *args, **kwargs):
        # Afegim l'id d'esdeveniment del paràmetre a les dades de la request abans de crear
        data = request.data.copy()
        data['model'] = model_id

        # Equivalent super().create, però amb "data"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class InferenciesView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    models = Inferencia
    serializer_class = InferenciaSerializer

    def get_queryset(self):
        # Aconseguim el model que ens arriba del paràmetre
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, id=model_id)

        # Filtrem per obtenir la inferència corresponent
        return Inferencia.objects.select_related('model').all().filter(model=model)

    def get_serializer_class(self):
        # En cas que sigui retrieve, retornem tota la info, amb el resultat
        if self.action == 'retrieve' or self.action == 'create':
            return InferenciaAmbResultatSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        # Aconseguir valors de la inferència a generar la EL
        inferencia = self.get_object()
        inference_data = self.get_serializer(inferencia).data
        resultats_inferencia = inference_data['resultats']

        # Aconseguir informació de les mètriques (de inferència i que tinguin pes)
        metriques = Metrica.objects.filter(fase=Metrica.INF).order_by('-pes').exclude(pes=0)

        # Calcular ratings (amb adaptador)
        qualifFinal, qualifMetriques = calculateRating(resultats_inferencia, metriques)

        # Generar etiqueta i resultats (amb adaptador)
        label, resultatsResponse = generateLabel(qualifFinal, qualifMetriques, resultats_inferencia, inferencia.model, inferencia.id, 'Inference')

        # Preparar les dades que es responen al client
        response_data = {
            'energy_label': base64.b64encode(label).decode(),
            'resultats': resultatsResponse,
            'infoInferencia': inference_data
        }
        return Response(response_data)

    def create(self, request, model_id=None, *args, **kwargs):
        # Afegim l'id de la inferència del paràmetre a les dades de la request abans de crear
        data = request.data.copy()
        data['model'] = model_id

        # Equivalent super().create, però amb "data"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class QualificacionsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    models = Qualificacio
    serializer_class = QualificacioSerializer
    queryset = Qualificacio.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['ordre']

class MetriquesView(viewsets.ModelViewSet):
    models = Metrica
    queryset = Metrica.objects.all()
    permission_classes = [permissions.IsAdminEditOthersRead]

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

        # Actualitzem els intervals (recuperem la instància i la modifiquem amb els valors donats)
        intervals = data.pop('intervals')
        for intervalJSON in intervals:
            interval = Interval.objects.get(metrica=metrica, qualificacio__id=intervalJSON['qualificacio'])
            serializer = IntervalBasicSerializer(interval, data=intervalJSON, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # Actualitzem la mètrica (equivalent a super.update() amb petites modificacions)
        serializer = self.get_serializer(metrica, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class InfoAddicionalsView(viewsets.ModelViewSet):
    model = InfoAddicional
    serializer_class = InfoAddicionalSerializer
    queryset = InfoAddicional.objects.all()
    permission_classes = [permissions.IsAdminEditOthersRead]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'id': ['exact', 'in'],
        'nom': ['exact', 'in', 'contains'],
        'fase': ['exact', 'in'],
    }
    search_fields = ['nom', 'fase']
    ordering_fields = ['id', 'nom', 'fase']

class CalculadorInferenciaView(mixins.CreateModelMixin, viewsets.GenericViewSet):
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
    models = EinaCalcul
    queryset = EinaCalcul.objects.all()
    serializer_class = EinaCalculSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]

    def get_serializer_class(self):
        if self.action == 'create':
            return EinaCalculBasicSerializer
        else:
            return EinaCalculSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        eina = self.get_object()
        data = request.data.copy()

        # Actualitzem les transformacions de mètriques (recuperem la instància i la modifiquem amb els valors donats)
        TransformacioMetrica.objects.filter(eina=eina).delete()
        transfMetriques = data.pop('transformacionsMetriques', None)
        if transfMetriques:
            for transfMetricaJSON in transfMetriques:
                metrica = get_object_or_404(Metrica, id=transfMetricaJSON['metrica'])
                transfMetrica, created = TransformacioMetrica.objects.get_or_create(eina=eina, metrica=metrica)
                serializer = TransformacioMetricaSerializer(transfMetrica, data=transfMetricaJSON, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        # Actualitzem les transformacions de informacions (recuperem la instància i la modifiquem amb els valors donats)
        TransformacioInformacio.objects.filter(eina=eina).delete()
        transfInformacions = data.pop('transformacionsInformacions', None)
        if transfInformacions:
            for transfInfoJSON in transfInformacions:
                informacio = get_object_or_404(InfoAddicional, id=transfInfoJSON['informacio'])
                transfInfo, created = TransformacioInformacio.objects.get_or_create(eina=eina, informacio=informacio)
                serializer = TransformacioInformacioSerializer(transfInfo, data=transfInfoJSON, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        # Actualitzem l'eina (equivalent a super.update() amb petites modificacions)
        serializer = self.get_serializer(eina, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class LoginAdminView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Administrador.objects.all()
    serializer_class = LoginAdminSerializer
    models = Administrador

class SincroView(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdmin]

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
    def get_serializer_class(self):
        pass

    def list(self, request, *args, **kwargs):
        data = {
            "numModels": Model.objects.count(),
            "numEntrenaments": Entrenament.objects.count(),
            "numInferencies": Inferencia.objects.count(),
        }
        return Response(data, status=status.HTTP_200_OK)

# GAISSA ROI Analyzer Views
class ModelArchitectureView(viewsets.ModelViewSet):
    queryset = ModelArchitecture.objects.all()
    serializer_class = ModelArchitectureSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name', 'information']
    ordering_fields = ['name']

    
    # Define new endpoint to get compatible tactics for a specific architecture
    @action(detail=True, methods=['get'], url_path='compatible-tactics')
    def get_compatible_tactics(self, request, pk=None):
        architecture = self.get_object()
        compatible_tactics = architecture.compatible_tactics.all()
        
        # Serialize the tactics and return them
        serializer = MLTacticSerializer(compatible_tactics, many=True)
        return Response(serializer.data)

class TacticSourceView(viewsets.ModelViewSet):
    queryset = TacticSource.objects.all()
    serializer_class = TacticSourceSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'url']
    search_fields = ['title', 'url']
    ordering_fields = ['title']

class MLTacticView(viewsets.ModelViewSet):
    queryset = MLTactic.objects.all()
    serializer_class = MLTacticSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'sources']
    search_fields = ['name', 'information']
    ordering_fields = ['name']

    # Define new endpoint to get applicable metrics for a specific tactic
    @action(detail=True, methods=['get'], url_path='applicable-metrics')
    def get_applicable_metrics(self, request, pk=None):
        tactic = self.get_object()
        applicable_metrics = tactic.applicable_metrics.all()
        
        # Serialize the metrics and return them
        serializer = ROIMetricSerializer(applicable_metrics, many=True)
        return Response(serializer.data)

class TacticParameterOptionView(viewsets.ModelViewSet):
    queryset = TacticParameterOption.objects.all()
    serializer_class = TacticParameterOptionSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'tactic', 'name', 'value']
    search_fields = ['name', 'value', 'tactic__name']
    ordering_fields = ['tactic__name', 'name', 'value']

class ROIMetricView(viewsets.ModelViewSet):
    queryset = ROIMetric.objects.all()
    serializer_class = ROIMetricSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'unit']
    search_fields = ['name', 'description']
    ordering_fields = ['name']

class ROIAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ROIAnalysis.objects.all()
    serializer_class = ROIAnalysisSerializer
    
    # Allow anyone to create ROI analyses, for other actions use default permissions
    def get_permissions(self):
        if self.action == 'create':
            return []
        return [permissions.IsAdminEditOthersRead()]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'model_architecture': ['exact'],
        'tactic_parameter_option': ['exact'],
        'tactic_parameter_option__tactic': ['exact'],
        'metric_values__metric': ['exact'],
        'roianalysiscalculation__country': ['exact', 'icontains'],
        'roianalysiscalculation__dateRegistration': ['date__gte', 'date__lte'],
    }
    search_fields = [
        'model_architecture__name',
        'tactic_parameter_option__tactic__name',
        'tactic_parameter_option__name',
        'tactic_parameter_option__value',
        'roianalysiscalculation__country'
    ]
    ordering_fields = ['id', 'model_architecture__name', 'tactic_parameter_option__tactic__name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            analysis_type = self.request.data.get('analysis_type', 'calculation')
            if analysis_type == 'calculation':
                return ROIAnalysisCalculationSerializer
            elif analysis_type == 'research':
                return ROIAnalysisResearchSerializer
        if self.action == 'retrieve':
            instance = self.get_object()
            if hasattr(instance, 'roianalysiscalculation'):
                return ROIAnalysisCalculationSerializer
            elif hasattr(instance, 'roianalysisresearch'):
                return ROIAnalysisResearchSerializer
        return ROIAnalysisSerializer

class AnalysisMetricValueView(viewsets.ModelViewSet):
    queryset = AnalysisMetricValue.objects.all()
    serializer_class = AnalysisMetricValueSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['analysis', 'metric']
    ordering_fields = ['analysis', 'metric']

class ExpectedMetricReductionView(viewsets.ModelViewSet):
    queryset = ExpectedMetricReduction.objects.all()
    serializer_class = ExpectedMetricReductionSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['model_architecture', 'tactic_parameter_option', 'metric']
    ordering_fields = ['model_architecture', 'tactic_parameter_option', 'metric']