from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .models import Model, Entrenament, Inferencia, Metrica, Qualificacio, Interval, ResultatEntrenament, \
    ResultatInferencia, InfoAddicional, ValorInfoEntrenament, ValorInfoInferencia, EinaCalcul, \
    TransformacioMetrica, TransformacioInformacio, Administrador


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

        # Afegim les info de les mètriques
        if resultats_data:
            for metrica, valor in resultats_data.items():
                metrica = get_object_or_404(Metrica, id=metrica)
                ResultatEntrenament.objects.create(entrenament=entrenament, metrica=metrica, valor=valor)

        # Afegim els valors de les informacions addicionals
        if infos_data:
            for info, valor in infos_data.items():
                infoAdd = get_object_or_404(InfoAddicional, id=info)
                ValorInfoEntrenament.objects.create(entrenament=entrenament, infoAddicional=infoAdd, valor=valor)

        return entrenament

    class Meta:
        model = Entrenament
        fields = ('model', 'id', 'dataRegistre', 'resultats', 'resultats_info', 'infoAddicional', 'infoAddicional_valors')


class InferenciaAmbResultatSerializer(serializers.ModelSerializer):
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

        # Afegim les info de les mètriques
        if resultats_data:
            for metrica, valor in resultats_data.items():
                metrica = get_object_or_404(Metrica, id=metrica)
                ResultatInferencia.objects.create(inferencia=inferencia, metrica=metrica, valor=valor)

        # Afegim els valors de les informacions addicionals
        if infos_data:
            for info, valor in infos_data.items():
                infoAdd = get_object_or_404(InfoAddicional, id=info)
                ValorInfoInferencia.objects.create(inferencia=inferencia, infoAddicional=infoAdd, valor=valor)

        return inferencia

    class Meta:
        model = Inferencia
        fields = ('model', 'id', 'dataRegistre', 'resultats', 'resultats_info', 'infoAddicional', 'infoAddicional_valors')


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


class EinaCalculSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = TransformacioMetrica
        fields = '__all__'


class TransformacioInformacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformacioInformacio
        fields = '__all__'


# LOGIN
def validacioLogin(data):
    username = data.get("username", None)
    password = data.get("password", None)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound("No existeix un usuari amb aquest username.")

    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        raise serializers.ValidationError("Contrasenya incorrecta.")
    return user


def creacioLogin(data, user):
    token, created = Token.objects.get_or_create(user=user)
    data['token'] = token.key
    data['created'] = created
    return data


class LoginAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Administrador
        fields = ('username', 'password', 'token')

    def create(self, data):
        user = self.context['user']
        data = creacioLogin(data, user)
        data['user'] = user
        return data

    def validate(self, data):
        user = validacioLogin(data)
        try:
            _ = user.administrador
        except:
            raise NotFound("No existeix un admininstrador amb aquest username.")
        self.context['user'] = user

        return data
