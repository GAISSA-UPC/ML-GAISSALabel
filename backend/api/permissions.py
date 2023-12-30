from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


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
