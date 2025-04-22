import base64
import pytz

from rest_framework import viewsets, filters, status, mixins
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from api.models import Model, Entrenament, Inferencia, Metrica, InfoAddicional, Qualificacio, Interval, EinaCalcul, \
    TransformacioMetrica, TransformacioInformacio, Administrador, Configuracio, OptimizationTechnique, GAISSAROIAnalysis, GAISSAROICostMetrics, TechniqueParameter
from api.serializers import ModelSerializer, EntrenamentSerializer, InferenciaSerializer, MetricaAmbLimitsSerializer, \
    EntrenamentAmbResultatSerializer, InferenciaAmbResultatSerializer, InfoAddicionalSerializer, QualificacioSerializer, \
    IntervalBasicSerializer, MetricaSerializer, EinaCalculBasicSerializer, EinaCalculSerializer, \
    TransformacioMetricaSerializer, TransformacioInformacioSerializer, LoginAdminSerializer, OptimizationTechniqueSerializer, \
    GAISSAROIAnalysisSerializer, GAISSAROICostMetricsSerializer, TechniqueParameterSerializer

from api import permissions
from efficiency_calculators.rating_calculator import calculateRating
from efficiency_calculators.label_generator import generateLabel
from efficiency_calculators.efficiency_calculator import calculateEfficiency
from efficiency_calculators.roi_calculator import ROICalculator
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

# ROI Views
class TechniqueParameterView(viewsets.ModelViewSet):
    queryset = TechniqueParameter.objects.all()
    serializer_class = TechniqueParameterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        technique_id = self.kwargs.get('optimization_technique_id')
        model_id = self.request.query_params.get('model_id')

        if technique_id:
            queryset = queryset.filter(optimization_technique_id=technique_id)

        if model_id:
            queryset = queryset.filter(gaissaroianalysis__model_id=model_id).distinct()

        return queryset
    
    def perform_create(self, serializer):
        # Automatically set the optimization_technique based on the URL
        if 'optimization_technique_id' in self.kwargs:
            optimization_technique_id = self.kwargs['optimization_technique_id']
            optimization_technique = get_object_or_404(OptimizationTechnique, pk=optimization_technique_id)
            serializer.save(optimization_technique=optimization_technique)
        else:
            serializer.save()

class OptimizationTechniqueView(viewsets.ModelViewSet):
    queryset = OptimizationTechnique.objects.all()
    serializer_class = OptimizationTechniqueSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        model_id = self.request.query_params.get('model_id')

        if model_id:
            queryset = queryset.filter(gaissaroianalysis__model_id=model_id).distinct()

        return queryset

class GAISSAROIAnalysesView(viewsets.ModelViewSet):
    queryset = GAISSAROIAnalysis.objects.all()
    serializer_class = GAISSAROIAnalysisSerializer

    def get_queryset(self):
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, pk=model_id)
        queryset = GAISSAROIAnalysis.objects.filter(model=model)

        # Filter by optimization technique ID
        optimization_technique_id = self.request.query_params.get('optimization_technique_id')
        if optimization_technique_id:
            optimization_technique = get_object_or_404(OptimizationTechnique, pk=optimization_technique_id)
            queryset = queryset.filter(optimization_technique=optimization_technique)

        technique_parameter_id = self.request.query_params.get('technique_parameter_id')
        if technique_parameter_id:
            technique_parameter = get_object_or_404(TechniqueParameter, pk=technique_parameter_id)
            queryset = queryset.filter(technique_parameter = technique_parameter)

        return queryset

    def list(self, request, model_id=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, model_id=None):
        queryset = self.get_queryset()
        gaissa_roi_analysis = get_object_or_404(queryset, pk=pk)

        # Get related data
        model = gaissa_roi_analysis.model
        optimization_technique = gaissa_roi_analysis.optimization_technique
        gaissa_roi_cost_metrics = gaissa_roi_analysis.gaissa_roi_cost_metrics.all()

        calculator = ROICalculator()

        optimization_cost_data = gaissa_roi_cost_metrics.filter(type='optimization').first()
        original_cost_data = gaissa_roi_cost_metrics.filter(type='original').first()
        new_cost_data = gaissa_roi_cost_metrics.filter(type='new').first()

        if not all([optimization_cost_data, original_cost_data, new_cost_data]):
            return Response({"error": "Missing GAISSA ROI cost metrics data."}, status=status.HTTP_400_BAD_REQUEST)

        num_inferences = int(request.query_params.get('num_inferences', 100))

        # Calculate ROI and Break-Even Point
        new_cost_per_inference = calculator._calculate_cost_per_inference(new_cost_data)
        original_cost_per_inference = calculator._calculate_cost_per_inference(original_cost_data)
        roi = calculator.calculate_roi_from_metrics(optimization_cost_data, original_cost_data, new_cost_data, num_inferences)
        roi_infinite = calculator.calculate_roi_from_metrics(optimization_cost_data, original_cost_data, new_cost_data, float('inf'))
        break_even_point = calculator.calculate_break_even_point_from_metrics(optimization_cost_data, original_cost_data, new_cost_data)

        roi_results = [
            {"name": "Optimization Cost", "value": f"{calculator._calculate_total_cost(optimization_cost_data):.4f} €"},
            {"name": "New Cost Per Inference", "value": f"{new_cost_per_inference:.8f} €"},
            {"name": "Original Cost Per Inference", "value": f"{original_cost_per_inference:.8f} €"},
            {"name": "Cost Savings Per Inference", "value": f"{original_cost_per_inference - new_cost_per_inference:.8f} €"},
            {"name": f"ROI (for {num_inferences} inferences)", "value": f"{roi:.6f}"},
            {"name": "ROI (for infinite inferences)", "value": f"{roi_infinite:.6f}"},
            {"name": "Break-Even Point", "value": f"{break_even_point} inferences"},
        ]

        # Calculate ROI Evolution
        roi_evolution_data = calculator.calculate_roi_evolution(optimization_cost_data, original_cost_data, new_cost_data)
        roi_evolution_chart_data = [{"inferences": inferences, "roi": roi} for inferences, roi in roi_evolution_data]

        # Add the calculated ROI results to the response
        serializer = self.get_serializer(gaissa_roi_analysis)
        response_data = serializer.data
        response_data['roi_results'] = roi_results
        response_data['roi_evolution_chart_data'] = roi_evolution_chart_data

        return Response(response_data)
    
    def perform_create(self, serializer):
        # Automatically set the model based on the URL
        if 'model_id' in self.kwargs:
            model_id = self.kwargs['model_id']
            model = get_object_or_404(Model, pk=model_id)
            serializer.save(model=model)
        else:
            serializer.save()
    
class GAISSAROICostMetricsView(viewsets.ModelViewSet):
    queryset = GAISSAROICostMetrics.objects.all()
    serializer_class = GAISSAROICostMetricsSerializer
    permission_classes = [permissions.IsAdminEditOthersRead]

    def get_queryset(self):
        queryset = super().get_queryset()
        gaissa_roi_analysis_id = self.request.query_params.get('gaissa_roi_analysis_id')

        if gaissa_roi_analysis_id:
            queryset = queryset.filter(gaissa_roi_analysis=gaissa_roi_analysis_id)

        return queryset