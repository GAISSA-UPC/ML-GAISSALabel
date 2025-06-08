from .calculator_codecarbon_adapter import get_efficiency_results
from ..models import TransformacioMetrica


def calculateEfficiency(endpoint, data):
    # Agafem les transformacions de les mètriques x CodeCarbon
    transformacions_objs = TransformacioMetrica.objects.filter(eina__nom='CodeCarbon')
    transformacions = {transf.metrica.id: transf.valor for transf in transformacions_objs}

    # Fem servir el generador de resultats d'eficiència basat en CodeCarbon
    return get_efficiency_results(endpoint, data, transformacions)
