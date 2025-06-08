from rest_framework import serializers
from .models import Administrador, Configuracio, Country, CarbonIntensity


class LoginAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin login."""
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Administrador
        fields = ('username', 'password', 'token')

    def create(self, data):
        user = self.context['user']
        # Import the function from the original location temporarily
        from api.serializers import creacioLogin
        data = creacioLogin(data, user)
        data['user'] = user
        return data

    def validate(self, data):
        # Import the validation function from the original location temporarily
        from api.serializers import validacioLogin
        return validacioLogin(data)


class ConfiguracioSerializer(serializers.ModelSerializer):
    """Serializer for configuration singleton."""
    
    class Meta:
        model = Configuracio
        fields = ['gaissa_label_enabled', 'gaissa_roi_analyzer_enabled', 'ultimaSincronitzacio']


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model."""
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_code']


class CarbonIntensitySerializer(serializers.ModelSerializer):
    """Serializer for CarbonIntensity model."""
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = CarbonIntensity
        fields = ['id', 'country', 'country_name', 'carbon_intensity', 'data_year']
