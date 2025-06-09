"""
URL configuration for gaissalabel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
       title="GAISSA Tools",
       default_version='v1',
       description="Comprehensive platform for ML model efficiency assessment and ROI analysis",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Legacy API (for backward compatibility during migration)
    #path('api/', include('api.urls')),
    # New modular apps
    path('api/core/', include('apps.core.urls')),
    path('api/gaissalabel/', include('apps.gaissalabel.urls')),
    path('api/roi/', include('apps.gaissa_roi_analyzer.urls')),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
