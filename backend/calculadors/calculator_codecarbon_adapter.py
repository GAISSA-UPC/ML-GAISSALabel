import requests
import csv
from codecarbon import OfflineEmissionsTracker

output_dir = '.'
output_file = 'emissions.csv'


def query(endpoint, payload):
    response = requests.post(endpoint, json=payload)
    print(payload)
    print(response.status_code)
    return response.json()


def get_efficiency_results(endpoint, data, transformacions):
    # Definir tracker i realitzar la query
    tracker = OfflineEmissionsTracker(
        country_iso_code="CAN",
        output_file=output_file,
        output_dir=output_dir,
    )
    tracker.start()
    print(query(endpoint, data))
    tracker.stop()

    # Recuperar resultats (transformant-los de CSV a array de JSONs)
    dataCSV = []
    with open(output_dir + '/' + output_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dataCSV.append(row)

    # Transformar valors a mètriques de l'aplicació i retornar resultats
    resultats = {}
    for (metrica, transformacio) in transformacions.items():
        resultats[metrica] = dataCSV[-1].get(transformacio)

    return resultats
