import base64

from rest_framework import viewsets, filters
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from .models import Model, Entrenament, Metrica, Qualificacio, Interval
from .serializers import ModelSerializer, EntrenamentSerializer, MetricaSerializer, MetricaAmbLimitsSerializer,\
    QualificacioSerializer, IntervalSerializer, EntrenamentAmbResultatSerializer
from .rating_calculator import calculate_ratings
from .label_generator import generate_efficency_label


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

        # Aconseguir valors de l'entrenament que es fa servir de referència (per normalitzar)
        metriques_ref = {'co2_eq_emissions': 149200.0,
                         'size_efficency': 2364.837238605898,
                         'datasets_size_efficency': 266551.5743699732,
                         'downloads': 1172830,
                         'performance_score': 0.8232786885245902
                         }

        # Aconseguir informació de les mètriques (de training i que tinguin pes)
        metriques = Metrica.objects.filter(fase=Metrica.TRAIN).order_by('-pes').exclude(pes=0)
        metriques_info = MetricaAmbLimitsSerializer(metriques, many=True).data

        boundaries = {}         # Intervals de les diferents mètriques
        pesos = {}              # Pesos de les mètriques
        resultats_utils = {}    # Resultats que corresponen a mètriques amb pes != 0
        positius = []           # Quines mètriques tenen impacte positiu en el càlcul
        unitats = {}            # Unitats de les mètriques que en tenen
        noms = {}               # Noms a mostrar de les mètriques
        for metrica in metriques_info:
            id_metrica = metrica['id']

            # Càlcul dels intervals
            intervals = Interval.objects.filter(metrica_id=id_metrica).order_by('qualificacio__ordre')
            intervals_info = IntervalSerializer(intervals, many=True).data
            boundaries[id_metrica] = [
                [interval['limitSuperior'], interval['limitInferior']]
                for interval in intervals_info
            ]

            # Càlcul dels pesos de la mètrica
            pesos[id_metrica] = metrica['pes']

            # Càlcul de resultats útils
            if id_metrica in resultats_entrenament:
                resultats_utils[id_metrica] = resultats_entrenament[id_metrica]

            # Veiem si és positiva o no
            if metrica['influencia'] == Metrica.POSITIVA:
                positius.append(id_metrica)

            # Guardem la seva unitat
            unitats[id_metrica] = metrica['unitat']

            # Guardem el nom
            noms[id_metrica] = metrica['nom']

        # Aconseguir les possibles qualificacions
        qualificacions = Qualificacio.objects.order_by('ordre')
        qualificacions_info = QualificacioSerializer(qualificacions, many=True).data
        qualificacions_valor = [
            qualificacio['id'] for qualificacio in qualificacions_info
        ]

        qualifFinal, qualifMetriques = calculate_ratings(resultats_utils, metriques_ref, boundaries, pesos, positius, qualificacions_valor)

        # Limitem el nombre de resultats que mostrem a l'EL a 6 màxim (que seran els que tinguis major pes)
        resultats = {
            noms[metrica_id]: {
                'value': resultats_entrenament[metrica_id],
                'unit': unitats[metrica_id],
                'image': Interval.objects.get(metrica__id=metrica_id, qualificacio__id=qualifMetriques[metrica_id]).imatge.read()
            } for metrica_id, qualificacio in list(qualifMetriques.items())[:6]
        }

        label = generate_efficency_label(resultats, qualificacions_valor, qualifFinal, entrenament.model.nom, 'Training')

        response_data = {
            'energy_label': base64.b64encode(label).decode(),
        }
        response_data.update(entrenament_data)
        return Response(response_data)


class MetriquesView(viewsets.ModelViewSet):
    models = Metrica
    serializer_class = MetricaSerializer
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
