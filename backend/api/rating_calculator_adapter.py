from .models import Interval, Qualificacio
from .serializers import MetricaAmbLimitsSerializer, IntervalSerializer, QualificacioSerializer
from .rating_calculator import calculate_ratings


def calculateRating(resultats, metriques):
    # Aconseguir la informació de les mètriques rebudes
    metriques_info = MetricaAmbLimitsSerializer(metriques, many=True).data

    # Inicialitzar variables a calcular per poder-les donar a la funció de càlcul dels ratings
    boundaries = {}  # Intervals de les diferents mètriques
    pesos = {}  # Pesos de les mètriques
    resultats_utils = {}  # Resultats que corresponen a mètriques amb pes != 0

    # Recull i càlcul de les dades necessàries
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
        if id_metrica in resultats:
            resultats_utils[id_metrica] = resultats[id_metrica]

    # Aconseguir les possibles qualificacions
    qualificacions = Qualificacio.objects.order_by('ordre')
    qualificacions_info = QualificacioSerializer(qualificacions, many=True).data
    qualificacions_valor = [
        qualificacio['id'] for qualificacio in qualificacions_info
    ]

    qualifFinal, qualifMetriques = calculate_ratings(resultats_utils, boundaries, pesos, qualificacions_valor)

    return qualifFinal, qualifMetriques
