from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Administrador, Configuracio, Country, CarbonIntensity


class LoginAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin login."""
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Administrador
        fields = ('username', 'password', 'token')

    def create(self, validated_data):
        user = self.context['user']
        # Create or get token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Return the response data
        return {
            'username': validated_data['username'],
            'token': token.key,
            'user': user
        }

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("No existeix un usuari amb aquest username.")

        # Check password
        pwd_valid = check_password(password, user.password)
        if not pwd_valid:
            raise ValidationError("Contrasenya incorrecta.")
        
        # Check if user is an administrator
        try:
            _ = user.administrador
        except:
            raise NotFound("No existeix un admininstrador amb aquest username.")
        
        # Store user in context for create method
        self.context['user'] = user
        
        # Return the original data (not the user object)
        return data


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
