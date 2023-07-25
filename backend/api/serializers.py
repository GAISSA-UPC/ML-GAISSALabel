import json

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
    limits = serializers.SerializerMethodField()

    def esborrar_claudators(self, obj):
        superior = 1 if obj[0] == '[' else 0
        inferior = -1 if obj[-1] == ']' else None

        return obj[superior:inferior]

    def get_limits(self, metrica):
        resultat = []
        limits = self.esborrar_claudators(metrica.limits)
        for limit in limits.split('], '):
            limit = self.esborrar_claudators(limit)
            limit_splitted = limit.split(', ')
            parcial = []
            parcial.append(float(limit_splitted[0]))
            parcial.append(float(limit_splitted[1]))
            resultat.append(parcial)
        return resultat

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
