from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from api.models import Configuracio


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view=None):
        return super().has_permission(request, view) and request.user.is_active


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view=None):
        try:
            return super().has_permission(request, view) and request.user.administrador
        except (ObjectDoesNotExist, AttributeError):
            return False


class IsAdminEditOthersRead(IsAuthenticated):
    def has_permission(self, request, view=None):
        try:
            return (
                request.method in permissions.SAFE_METHODS or
                getattr(request.user, 'administrador', False)
            )
        except (ObjectDoesNotExist, AttributeError):
            return False


class IsToolEnabled(permissions.BasePermission):
    """
    Base class for tool-specific permission checks.
    Must be subclassed with a specific tool_setting attribute.
    """
    tool_setting = None  # Override in subclasses
    
    def has_permission(self, request, view):
        try:
            config = Configuracio.objects.get()
            return getattr(config, self.tool_setting, True)  # Default to True if tool setting doesn't exist
        except Exception:
            return True  # Default to enabled if config doesn't exist


class IsGAISSAROIAnalyzerEnabled(IsToolEnabled):
    """Permission class to check if GAISSA ROI Analyzer is enabled"""
    tool_setting = 'gaissa_roi_analyzer_enabled'


class IsGAISSALabelEnabled(IsToolEnabled):
    """Permission class to check if GAISSALabel is enabled"""
    tool_setting = 'gaissa_label_enabled'

