from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound, ValidationError

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from api.models import Model, Entrenament, Inferencia, Metrica, Qualificacio, Interval, ResultatEntrenament, \
    ResultatInferencia, InfoAddicional, ValorInfoEntrenament, ValorInfoInferencia, EinaCalcul, TransformacioMetrica, \
    TransformacioInformacio, Administrador, ModelArchitecture, TacticSource, MLTactic, TacticParameterOption, \
    ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch, ROIMetric, AnalysisMetricValue, ExpectedMetricReduction, \
    Configuracio, Administrador

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

class EinaCalculBasicSerializer(serializers.ModelSerializer):
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

# GAISSA ROI Analyzer Serializers
class ModelArchitectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelArchitecture
        fields = '__all__'

class TacticSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacticSource
        fields = '__all__'

class MLTacticSerializer(serializers.ModelSerializer):
    sources = TacticSourceSerializer(many=True, read_only=True)
    source_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TacticSource.objects.all(), write_only=True, source='sources', required=True
    )

    class Meta:
        model = MLTactic
        fields = ['id', 'name', 'information', 'sources', 'source_ids']

class TacticParameterOptionSerializer(serializers.ModelSerializer):
    tactic_name = serializers.CharField(source='tactic.name', read_only=True)
    tactic_id = serializers.PrimaryKeyRelatedField(
        queryset=MLTactic.objects.all(), write_only=True, source='tactic'
    )

    class Meta:
        model = TacticParameterOption
        fields = ['id', 'tactic', 'tactic_id', 'tactic_name', 'name', 'value']
        read_only_fields = ['tactic'] # tactic is set via tactic_id

class ROIMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROIMetric
        fields = '__all__'

class AnalysisMetricValueSerializer(serializers.ModelSerializer):
    metric_name = serializers.CharField(source='metric.name', read_only=True)
    metric_id = serializers.PrimaryKeyRelatedField(
        queryset=ROIMetric.objects.all(), write_only=True, source='metric'
    )

    class Meta:
        model = AnalysisMetricValue
        fields = ['id', 'analysis', 'metric', 'metric_id', 'metric_name', 'baselineValue']
        read_only_fields = ['metric'] # metric is set via metric_id

class ROIAnalysisSerializer(serializers.ModelSerializer):
    model_architecture_name = serializers.CharField(source='model_architecture.name', read_only=True)
    tactic_parameter_option_details = TacticParameterOptionSerializer(source='tactic_parameter_option', read_only=True)
    metric_values = AnalysisMetricValueSerializer(many=True, read_only=True)
    
    # Fields from subclasses
    dateRegistration = serializers.SerializerMethodField(read_only=True)
    country = serializers.SerializerMethodField(read_only=True)
    source = serializers.SerializerMethodField(read_only=True)

    # Writeable fields for relations
    model_architecture_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelArchitecture.objects.all(), write_only=True, source='model_architecture'
    )
    tactic_parameter_option_id = serializers.PrimaryKeyRelatedField(
        queryset=TacticParameterOption.objects.all(), write_only=True, source='tactic_parameter_option'
    )
    # For creating metric values alongside analysis
    metric_values_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = ROIAnalysis
        fields = [
            'id', 'model_architecture', 'model_architecture_id', 'model_architecture_name',
            'tactic_parameter_option', 'tactic_parameter_option_id', 'tactic_parameter_option_details',
            'metric_values', 'metric_values_data', 'dateRegistration', 'country', 'source'
        ]
        read_only_fields = ['model_architecture', 'tactic_parameter_option']
    
    def get_dateRegistration(self, obj):
        if hasattr(obj, 'roianalysiscalculation'):
            return obj.roianalysiscalculation.dateRegistration
        return None
    
    def get_country(self, obj):
        if hasattr(obj, 'roianalysiscalculation'):
            return obj.roianalysiscalculation.country
        return None
        
    def get_source(self, obj):
        if hasattr(obj, 'roianalysisresearch'):
            source = obj.roianalysisresearch.source
            return {
                'id': source.id,
                'title': source.title,
                'url': source.url
            } if source else None
        return None

    def validate(self, data):
        """Check compatibility between the selected tactic and model architecture."""
        model_architecture = data.get('model_architecture')
        tactic_parameter_option = data.get('tactic_parameter_option')

        if model_architecture and tactic_parameter_option:
            tactic = tactic_parameter_option.tactic
            if not tactic.compatible_architectures.filter(pk=model_architecture.pk).exists():
                raise ValidationError(
                    _("The selected tactic '%(tactic)s' is not compatible with the model architecture '%(arch)s'.") % {
                        'tactic': tactic.name,
                        'arch': model_architecture.name
                    }
                )

        return data

    def _validate_metric_values_against_expected_reduction(self, metric_values_data, model_architecture, tactic_parameter_option):
        """Method to validate metric values against ExpectedMetricReduction."""
        if not metric_values_data:
            raise ValidationError("Missing Metrics data for validation.")

        if not model_architecture or not tactic_parameter_option:
            raise ValidationError("Missing Model Architecture or Tactic Parameter Option for validation.")

        metrics_to_create = []
        tactic = tactic_parameter_option.tactic
        
        for metric_data in metric_values_data:
            metric_id = metric_data.get('metric_id')
            baseline_value = metric_data.get('baselineValue')
            if metric_id is None or baseline_value is None:
                 raise ValidationError("Each entry in metric_values_data must include 'metric_id' and 'baselineValue'.")

            # Validate metric existence
            try:
                metric = ROIMetric.objects.get(pk=metric_id)
            except ROIMetric.DoesNotExist:
                raise ValidationError(f"ROIMetric with id {metric_id} does not exist.")
                
            # Constraint 3: Check if the metric is applicable for the tactic
            if not tactic.applicable_metrics.filter(pk=metric.pk).exists():
                raise ValidationError(
                    _("The metric '%(metric)s' is not applicable for the tactic '%(tactic)s'.") % {
                        'metric': metric.name,
                        'tactic': tactic.name
                    }
                )

            # Constraint 2: ExpectedMetricReduction existence check
            exists = ExpectedMetricReduction.objects.filter(
                model_architecture=model_architecture,
                tactic_parameter_option=tactic_parameter_option,
                metric=metric
            ).exists()
            if not exists:
                raise ValidationError(
                    f"No matching ExpectedMetricReduction found for the combination of "
                    f"Model Architecture '{model_architecture}', "
                    f"Tactic Parameter Option '{tactic_parameter_option}', and Metric '{metric}'."
                )

            metrics_to_create.append({'metric': metric, 'baselineValue': baseline_value})
        return metrics_to_create

    def create(self, validated_data):
        metric_values_data = validated_data.pop('metric_values_data', [])
        model_architecture = validated_data.get('model_architecture')
        tactic_parameter_option = validated_data.get('tactic_parameter_option')

        # Validate metric values against expected reductions
        metrics_to_create = self._validate_metric_values_against_expected_reduction(
            metric_values_data, model_architecture, tactic_parameter_option
        )

        # If validation passed, create the analysis and then the metric values
        analysis = ROIAnalysis.objects.create(**validated_data)
        for metric_info in metrics_to_create:
            AnalysisMetricValue.objects.create(
                analysis=analysis,
                metric=metric_info['metric'],
                baselineValue=metric_info['baselineValue']
            )
        return analysis

class ROIAnalysisCalculationSerializer(ROIAnalysisSerializer):
    country = serializers.CharField(max_length=255, required=True)
    
    class Meta(ROIAnalysisSerializer.Meta):
        model = ROIAnalysisCalculation
        fields = ROIAnalysisSerializer.Meta.fields + ['dateRegistration', 'country']

    def create(self, validated_data):
        metric_values_data = validated_data.pop('metric_values_data', [])
        model_architecture = validated_data.get('model_architecture')
        tactic_parameter_option = validated_data.get('tactic_parameter_option')

        # Validate metric values against expected reductions
        metrics_to_create = self._validate_metric_values_against_expected_reduction(
            metric_values_data, model_architecture, tactic_parameter_option
        )

        # If validation passed, create the specific analysis type and then the metric values
        analysis = ROIAnalysisCalculation.objects.create(**validated_data)
        for metric_info in metrics_to_create:
            AnalysisMetricValue.objects.create(
                analysis=analysis,
                metric=metric_info['metric'],
                baselineValue=metric_info['baselineValue']
            )
        return analysis

class ROIAnalysisResearchSerializer(ROIAnalysisSerializer):
     class Meta(ROIAnalysisSerializer.Meta):
        model = ROIAnalysisResearch
        fields = ROIAnalysisSerializer.Meta.fields + ['source']

     def create(self, validated_data):
        metric_values_data = validated_data.pop('metric_values_data', [])
        model_architecture = validated_data.get('model_architecture')
        tactic_parameter_option = validated_data.get('tactic_parameter_option')

        # Validate metric values against expected reductions
        metrics_to_create = self._validate_metric_values_against_expected_reduction(
            metric_values_data, model_architecture, tactic_parameter_option
        )

        # If validation passed, create the specific analysis type and then the metric values
        analysis = ROIAnalysisResearch.objects.create(**validated_data)
        for metric_info in metrics_to_create:
            AnalysisMetricValue.objects.create(
                analysis=analysis,
                metric=metric_info['metric'],
                baselineValue=metric_info['baselineValue']
            )
        return analysis

class ExpectedMetricReductionSerializer(serializers.ModelSerializer):
    model_architecture_name = serializers.CharField(source='model_architecture.name', read_only=True)
    tactic_parameter_option_details = TacticParameterOptionSerializer(source='tactic_parameter_option', read_only=True)
    metric_name = serializers.CharField(source='metric.name', read_only=True)

    # Writeable fields for relations
    model_architecture_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelArchitecture.objects.all(), write_only=True, source='model_architecture'
    )
    tactic_parameter_option_id = serializers.PrimaryKeyRelatedField(
        queryset=TacticParameterOption.objects.all(), write_only=True, source='tactic_parameter_option'
    )
    metric_id = serializers.PrimaryKeyRelatedField(
        queryset=ROIMetric.objects.all(), write_only=True, source='metric'
    )

    class Meta:
        model = ExpectedMetricReduction
        fields = [
            'id', 'model_architecture', 'model_architecture_id', 'model_architecture_name',
            'tactic_parameter_option', 'tactic_parameter_option_id', 'tactic_parameter_option_details',
            'metric', 'metric_id', 'metric_name', 'expectedReductionValue'
        ]
        read_only_fields = ['model_architecture', 'tactic_parameter_option', 'metric']

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