from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from .models import Model, Entrenament, Metrica
from .serializers import ModelSerializer, EntrenamentSerializer, MetricaSerializer, EntrenamentAmbResultatSerializer


class ModelsView(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    models = Model


class EntrenamentsView(viewsets.ModelViewSet):
    models = Entrenament
    serializer_class = EntrenamentSerializer

    def get_queryset(self):
        # Aconseguim el model que ens arriba del paràmetre
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, id=model_id)

        # Filtrem per obtenir l'entrenament corresponent
        return Entrenament.objects.select_related('model').all().filter(model=model)

    def get_serializer_class(self):
        # En cas que sigui retrieve, retornem tota la info, amb el resultat
        if self.action == 'retrieve':
            return EntrenamentAmbResultatSerializer
        return self.serializer_class


class MetriquesView(viewsets.ModelViewSet):
    models = Metrica
    serializer_class = MetricaSerializer
    queryset = Metrica.objects.all()
