import base64

from rest_framework import viewsets, filters, status, mixins
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from .models import Model, Entrenament, Inferencia, Metrica, InfoAddicional, Qualificacio, Interval
from .serializers import ModelSerializer, EntrenamentSerializer, InferenciaSerializer, MetricaAmbLimitsSerializer, \
    EntrenamentAmbResultatSerializer, InferenciaAmbResultatSerializer, InfoAddicionalSerializer, QualificacioSerializer, \
    IntervalBasicSerializer

from .rating_calculator_adapter import calculateRating
from .label_generator_adapter import generateLabel
from .efficiency_calculator_adapter import calculateEfficiency


class ModelsView(viewsets.ModelViewSet):
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


class EntrenamentsView(viewsets.ModelViewSet):
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
        label, resultatsResponse = generateLabel(qualifFinal, qualifMetriques, resultats_entrenament, entrenament.model, 'Training')

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


class InferenciesView(viewsets.ModelViewSet):
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
        label, resultatsResponse = generateLabel(qualifFinal, qualifMetriques, resultats_inferencia, inferencia.model, 'Inference')

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
    serializer_class = MetricaAmbLimitsSerializer
    queryset = Metrica.objects.all()

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
