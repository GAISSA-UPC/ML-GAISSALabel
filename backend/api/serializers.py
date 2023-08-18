from rest_framework import serializers

from .models import Model, Entrenament, Metrica, Qualificacio, Interval


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


class MetricaAmbLimitsSerializer(MetricaSerializer):

    class Meta:
        model = Metrica
        fields = '__all__'


class QualificacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualificacio
        fields = '__all__'


class IntervalSerializer(serializers.ModelSerializer):
    limitSuperior = serializers.SerializerMethodField(read_only=True)
    limitInferior = serializers.SerializerMethodField(read_only=True)

    def esInfinit(self, valor):
        threshold = 1e20
        return abs(valor) >= threshold

    def get_limitSuperior(self, interval):
        if self.esInfinit(interval.limitSuperior):
            return float('inf')
        else:
            return interval.limitSuperior

    def get_limitInferior(self, interval):
        if self.esInfinit(interval.limitInferior):
            return float('-inf')
        else:
            return interval.limitInferior


    class Meta:
        model = Interval
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
