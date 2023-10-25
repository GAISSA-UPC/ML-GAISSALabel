from rest_framework import serializers

from django.shortcuts import get_object_or_404

from .models import Model, Entrenament, Inferencia, Metrica, Qualificacio, Interval, ResultatEntrenament, \
    ResultatInferencia, InfoAddicional


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class EntrenamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenament
        fields = '__all__'


class InferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inferencia
        fields = '__all__'


class MetricaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrica
        fields = '__all__'


class QualificacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualificacio
        fields = '__all__'


class IntervalBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interval
        fields = ('qualificacio', 'limitSuperior', 'limitInferior')


class IntervalSerializer(IntervalBasicSerializer):
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


class MetricaAmbLimitsSerializer(MetricaSerializer):
    intervals = IntervalBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Metrica
        fields = '__all__'


class EntrenamentAmbResultatSerializer(serializers.ModelSerializer):
    resultats = serializers.SerializerMethodField(read_only=True)
    resultats_info = serializers.JSONField(write_only=True)

    def get_resultats(self, entrenament):
        resultats = {}
        for resultat in entrenament.resultatsEntrenament.all():
            resultats[resultat.metrica.id] = resultat.valor
        return resultats

    def create(self, validated_data):
        resultats_data = validated_data.pop('resultats_info', None)
        entrenament = super().create(validated_data)

        if resultats_data:
            for metrica, valor in resultats_data.items():
                metrica = get_object_or_404(Metrica, id=metrica)
                ResultatEntrenament.objects.create(entrenament=entrenament, metrica=metrica, valor=valor)

        return entrenament

    class Meta:
        model = Entrenament
        fields = ('model', 'id', 'dataRegistre', 'resultats', 'resultats_info')


class InferenciaAmbResultatSerializer(serializers.ModelSerializer):
    resultats = serializers.SerializerMethodField(read_only=True)
    resultats_info = serializers.JSONField(write_only=True)

    def get_resultats(self, inferencia):
        resultats = {}
        for resultat in inferencia.resultatsInferencia.all():
            resultats[resultat.metrica.id] = resultat.valor
        return resultats

    def create(self, validated_data):
        resultats_data = validated_data.pop('resultats_info', None)
        inferencia = super().create(validated_data)

        if resultats_data:
            for metrica, valor in resultats_data.items():
                metrica = get_object_or_404(Metrica, id=metrica)
                ResultatInferencia.objects.create(inferencia=inferencia, metrica=metrica, valor=valor)

        return inferencia

    class Meta:
        model = Inferencia
        fields = ('model', 'id', 'dataRegistre', 'resultats', 'resultats_info')


class InfoAddicionalSerializer(serializers.ModelSerializer):
    opcions_list = serializers.SerializerMethodField(read_only=True)

    def get_opcions_list(self, infoAdd):
        if infoAdd.opcions:
            return infoAdd.opcions.split(';')
        else:
            return None

    class Meta:
        model = InfoAddicional
        fields = '__all__'
