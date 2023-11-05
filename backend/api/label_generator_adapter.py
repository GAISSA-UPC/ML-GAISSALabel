import base64
from gaissalabel.settings import URL_FRONTEND
from .models import Qualificacio, Metrica, Interval
from .serializers import QualificacioSerializer
from .label_generator import generate_efficency_label


def generateLabel(qualifFinal, qualifMetriques, resultats, model, experiment_id, fase):
    # Adaptem els resultats rebuts al que necessita el label_generator
    # Limitem el nombre de resultats que mostrem a l'EL a 6 màxim (que seran els que tinguis major pes)
    resultats_formatted = {}
    for metrica_id, qualificacio in list(qualifMetriques.items())[:6]:
        metrica = Metrica.objects.get(id=metrica_id)
        resultats_formatted[metrica.nom] = {
            'id': metrica_id,
            'value': resultats[metrica_id],
            'qualificacio': qualifMetriques[metrica_id],
            'unit': metrica.unitat,
            'image': Interval.objects.get(metrica__id=metrica_id, qualificacio__id=qualifMetriques[metrica_id]).imatge.read(),
            'color': Qualificacio.objects.get(id=qualifMetriques[metrica_id]).color,
        }

    # Aconseguir les possibles qualificacions
    qualificacions = Qualificacio.objects.order_by('ordre')
    qualificacions_info = QualificacioSerializer(qualificacions, many=True).data
    qualificacions_valor = [
        qualificacio['id'] for qualificacio in qualificacions_info
    ]

    # Enllaç a la pàgina d'info de l'etiqueta
    url = URL_FRONTEND + '/models/' + str(model.id) + '/' + fase.lower() + 's/' + str(experiment_id)

    # Generació de l'etiqueta a partir del label_generator
    label = generate_efficency_label(resultats_formatted, qualificacions_valor, qualifFinal, model.nom, fase, url)

    # Adaptar resultats
    resultatsResponse = {
        info['id']: {
            'nom': nom_metrica,
            'value': info['value'],
            'qualificacio': info['qualificacio'],
            'unit': info['unit'],
            'image': base64.b64encode(info['image']).decode(),
            'color': info['color'],
        } for nom_metrica, info in resultats_formatted.items()
    }

    return label, resultatsResponse
