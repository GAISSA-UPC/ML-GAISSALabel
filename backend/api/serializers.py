from rest_framework import serializers

from .models import Model, Entrenament, Metrica, ResultatEntrenament


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class EntrenamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenament
        fields = '__all__'


class MetricaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrica
        fields = '__all__'


class EntrenamentAmbResultatSerializer(serializers.ModelSerializer):
    resultats = serializers.SerializerMethodField(read_only=True)

    def get_resultats(self, entrenament):
        resultats = {}
        for resultat in entrenament.resultats.all():
            resultats[resultat.metrica.id] = resultat.valor
        return resultats

    class Meta:
        model = Entrenament
        fields = ('dataRegistre', 'resultats')
