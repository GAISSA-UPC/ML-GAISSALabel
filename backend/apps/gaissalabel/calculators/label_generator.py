import base64
import os
from gaissa_tools.settings import URL_FRONTEND
from ..models import Qualificacio, Metrica, Interval
from ..serializers import QualificacioSerializer
from .label_generator_strategy import generate_efficency_label

# Directory of the label design elements
PARTS_DIR = os.path.join(os.path.dirname(__file__), "../label_design")
PARTS_DIR_NUMS = os.path.join(os.path.dirname(__file__), "../label_design/numbers")


def generateLabel(qualifFinal, qualifMetriques, resultats, model, experiment_id, fase):
    # Adaptem els resultats rebuts al que necessita el label_generator
    # Limitem el nombre de resultats que mostrem a l'EL a 6 màxim (que seran els que tinguis major pes)
    resultats_formatted = {}
    for metrica_id, qualificacio in list(qualifMetriques.items())[:6]:
        metrica = Metrica.objects.get(id=metrica_id)
        
        # Handle image reading with fallback to base filename
        image_data = None
        if qualificacio:
            try:
                interval = Interval.objects.get(metrica__id=metrica_id, qualificacio__id=qualifMetriques[metrica_id])
                if interval.imatge:
                    try:
                        # First try to read the file directly
                        with interval.imatge.open('rb') as img_file:
                            image_data = img_file.read()
                    except (FileNotFoundError, OSError):
                        # If file not found, try fallback strategies
                        filename = interval.imatge.name
                        # print(f"Debug: Original filename: {filename}")
                        
                        # Strategy 1: Try the original filename as-is in both directories
                        for search_dir in [PARTS_DIR, PARTS_DIR_NUMS]:
                            file_path = os.path.join(search_dir, filename)
                            # print(f"Debug: Checking original filename at: {file_path}")
                            if os.path.exists(file_path):
                                # print(f"Debug: Found image at: {file_path}")
                                with open(file_path, 'rb') as img_file:
                                    image_data = img_file.read()
                                break
                        
                        # Strategy 2: If not found and filename has extra suffixes, try base name
                        if image_data is None and '_' in filename:
                            parts = filename.split('_')
                            if len(parts) >= 3:
                                # Extract base name (e.g., "CO2_0_something.png" -> "CO2_0.png")
                                base_name = '_'.join(parts[:2]) + '.' + parts[-1].split('.')[-1]
                                # print(f"Debug: Looking for base name: {base_name}")
                                
                                for search_dir in [PARTS_DIR, PARTS_DIR_NUMS]:
                                    base_path = os.path.join(search_dir, base_name)
                                    # print(f"Debug: Checking base name at: {base_path}")
                                    if os.path.exists(base_path):
                                        # print(f"Debug: Found image at: {base_path}")
                                        with open(base_path, 'rb') as img_file:
                                            image_data = img_file.read()
                                        break
                        
                        if image_data is None:
                            print(f"Debug: Image not found in any location for: {filename}")
            except (Interval.DoesNotExist, FileNotFoundError, OSError, AttributeError) as e:
                print(f"Debug: Exception caught: {e}")
                image_data = None
        
        resultats_formatted[metrica.nom] = {
            'id': metrica_id,
            'value': resultats[metrica_id],
            'qualificacio': qualifMetriques[metrica_id],
            'unit': metrica.unitat,
            'image': image_data,
            'color': Qualificacio.objects.get(id=qualifMetriques[metrica_id]).color if qualificacio else None,
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
    resultatsResponse = {}
    for nom_metrica, info in resultats_formatted.items():
        if info['value']:
            resultatsResponse[info['id']] = {
                'nom': nom_metrica,
                'value': info['value'],
                'qualificacio': info['qualificacio'],
                'unit': info['unit'],
                'color': info['color'],
                'image': base64.b64encode(info['image']).decode() if info['image'] else None,
            }

    return label, resultatsResponse
