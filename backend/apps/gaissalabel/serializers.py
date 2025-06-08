from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import (
    Model, Entrenament, Inferencia, Metrica, Qualificacio, Interval, 
    ResultatEntrenament, ResultatInferencia, InfoAddicional, 
    ValorInfoEntrenament, ValorInfoInferencia, EinaCalcul, 
    TransformacioMetrica, TransformacioInformacio
)


class ModelSerializer(serializers.ModelSerializer):
    """Serializer for ML models in GAISSALabel."""
    
    class Meta:
        model = Model
        fields = '__all__'


class EntrenamentSerializer(serializers.ModelSerializer):
    """Basic serializer for training sessions."""
    
    class Meta:
        model = Entrenament
        fields = '__all__'


class InferenciaSerializer(serializers.ModelSerializer):
    """Basic serializer for inference sessions."""
    
    class Meta:
        model = Inferencia
        fields = '__all__'


class MetricaSerializer(serializers.ModelSerializer):
    """Serializer for creating metrics with intervals."""
    intervals = serializers.ListField(write_only=True)

    def create(self, validated_data):
        intervals_data = validated_data.pop('intervals', None)
        metrica = super().create(validated_data)

        if intervals_data:
            for interval_data in intervals_data:
                qualificacio = interval_data.pop('qualificacio')
                Interval.objects.create(metrica=metrica, qualificacio_id=qualificacio, **interval_data)

        return metrica

    class Meta:
        model = Metrica
        fields = ('id', 'nom', 'fase', 'pes', 'unitat', 'influencia', 'descripcio', 'calcul', 'recomanacions', 'intervals')


class QualificacioSerializer(serializers.ModelSerializer):
    """Serializer for qualification/rating levels."""
    
    class Meta:
        model = Qualificacio
        fields = '__all__'


class IntervalBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for metric intervals."""
    
    class Meta:
        model = Interval
        fields = ('qualificacio', 'limitSuperior', 'limitInferior')


class IntervalSerializer(IntervalBasicSerializer):
    """Extended serializer for metric intervals with infinite value handling."""
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
    """Serializer for metrics with their interval limits."""
    intervals = IntervalBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Metrica
        fields = '__all__'


class EntrenamentAmbResultatSerializer(serializers.ModelSerializer):
    """Serializer for training sessions with results and additional info."""
    resultats = serializers.SerializerMethodField(read_only=True)
    resultats_info = serializers.JSONField(write_only=True)
    infoAddicional = serializers.SerializerMethodField(read_only=True)
    infoAddicional_valors = serializers.JSONField(write_only=True)

    def get_resultats(self, entrenament):
        resultats = {}
        for resultat in entrenament.resultatsEntrenament.all():
            resultats[resultat.metrica.id] = resultat.valor
        return resultats

    def get_infoAddicional(self, entrenament):
        valors = {}
        for valor in entrenament.informacionsEntrenament.all():
            valors[valor.infoAddicional.id] = {
                "nom": valor.infoAddicional.nom,
                "descripcio": valor.infoAddicional.descripcio,
                "valor": valor.valor,
            }
        return valors

    def create(self, validated_data):
        resultats_data = validated_data.pop('resultats_info', None)
        infos_data = validated_data.pop('infoAddicional_valors', None)
        entrenament = super().create(validated_data)

        # Add metric information
        if resultats_data:
            for metrica, valor in resultats_data.items():
                metrica = get_object_or_404(Metrica, id=metrica)
                ResultatEntrenament.objects.create(entrenament=entrenament, metrica=metrica, valor=valor)

        # Add additional information values
        if infos_data:
            for info, valor in infos_data.items():
                infoAdd = get_object_or_404(InfoAddicional, id=info)
                ValorInfoEntrenament.objects.create(entrenament=entrenament, infoAddicional=infoAdd, valor=valor)

        return entrenament

    class Meta:
        model = Entrenament
        fields = ('model', 'id', 'dataRegistre', 'resultats', 'resultats_info', 'infoAddicional', 'infoAddicional_valors')


class InferenciaAmbResultatSerializer(serializers.ModelSerializer):
    """Serializer for inference sessions with results and additional info."""
    resultats = serializers.SerializerMethodField(read_only=True)
    resultats_info = serializers.JSONField(write_only=True)
    infoAddicional = serializers.SerializerMethodField(read_only=True)
    infoAddicional_valors = serializers.JSONField(write_only=True)

    def get_resultats(self, inferencia):
        resultats = {}
        for resultat in inferencia.resultatsInferencia.all():
            resultats[resultat.metrica.id] = resultat.valor
        return resultats

    def get_infoAddicional(self, inferencia):
        valors = {}
        for valor in inferencia.informacionsInferencia.all():
            valors[valor.infoAddicional.id] = {
                "nom": valor.infoAddicional.nom,
                "descripcio": valor.infoAddicional.descripcio,
                "valor": valor.valor,
            }
        return valors

    def create(self, validated_data):
        resultats_data = validated_data.pop('resultats_info', None)
        infos_data = validated_data.pop('infoAddicional_valors', None)
        inferencia = super().create(validated_data)

        # Add metric information
        if resultats_data:
            for metrica, valor in resultats_data.items():
                metrica = get_object_or_404(Metrica, id=metrica)
                ResultatInferencia.objects.create(inferencia=inferencia, metrica=metrica, valor=valor)

        # Add additional information values
        if infos_data:
            for info, valor in infos_data.items():
                infoAdd = get_object_or_404(InfoAddicional, id=info)
                ValorInfoInferencia.objects.create(inferencia=inferencia, infoAddicional=infoAdd, valor=valor)

        return inferencia

    class Meta:
        model = Inferencia
        fields = ('model', 'id', 'dataRegistre', 'resultats', 'resultats_info', 'infoAddicional', 'infoAddicional_valors')


class InfoAddicionalSerializer(serializers.ModelSerializer):
    """Serializer for additional information configuration."""
    opcions_list = serializers.SerializerMethodField(read_only=True)

    def get_opcions_list(self, infoAdd):
        if infoAdd.opcions:
            return infoAdd.opcions.split(';')
        else:
            return None

    class Meta:
        model = InfoAddicional
        fields = '__all__'


class EinaCalculBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for calculation tools."""
    transformacionsMetriques = serializers.ListField(write_only=True, required=False)
    transformacionsInformacions = serializers.ListField(write_only=True, required=False)

    def create(self, validated_data):
        transfMetriques_data = validated_data.pop('transformacionsMetriques', None)
        transfInformacions_data = validated_data.pop('transformacionsInformacions', None)
        eina = super().create(validated_data)

        if transfMetriques_data:
            for transfMetrica_data in transfMetriques_data:
                metrica = transfMetrica_data.pop('metrica')
                TransformacioMetrica.objects.create(eina=eina, metrica_id=metrica, **transfMetrica_data)

        if transfInformacions_data:
            for transfInfo_data in transfInformacions_data:
                informacio = transfInfo_data.pop('informacio')
                TransformacioInformacio.objects.create(eina=eina, informacio_id=informacio, **transfInfo_data)

        return eina

    class Meta:
        model = EinaCalcul
        fields = ('id', 'nom', 'descripcio', 'transformacionsMetriques', 'transformacionsInformacions')


class EinaCalculSerializer(EinaCalculBasicSerializer):
    """Extended serializer for calculation tools with transformations."""
    transformacionsMetriques = serializers.SerializerMethodField(read_only=True)
    transformacionsInformacions = serializers.SerializerMethodField(read_only=True)

    def get_transformacionsMetriques(self, eina):
        transformacions = {}
        for transfMetrica in eina.transformacionsMetriques.all():
            transformacions[transfMetrica.valor] = transfMetrica.metrica.id
        return transformacions

    def get_transformacionsInformacions(self, eina):
        transformacions = {}
        for transfInfo in eina.transformacionsInformacions.all():
            transformacions[transfInfo.valor] = transfInfo.informacio.id
        return transformacions

    class Meta:
        model = EinaCalcul
        fields = ('id', 'nom', 'descripcio', 'transformacionsMetriques', 'transformacionsInformacions')


class TransformacioMetricaSerializer(serializers.ModelSerializer):
    """Serializer for metric transformations."""
    
    class Meta:
        model = TransformacioMetrica
        fields = '__all__'


class TransformacioInformacioSerializer(serializers.ModelSerializer):
    """Serializer for information transformations."""
    
    class Meta:
        model = TransformacioInformacio
        fields = '__all__'
