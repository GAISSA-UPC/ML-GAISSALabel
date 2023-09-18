from django.contrib import admin
from . import models

admin.site.register(models.Model)
admin.site.register(models.Entrenament)
admin.site.register(models.Inferencia)
admin.site.register(models.Metrica)
admin.site.register(models.Qualificacio)
admin.site.register(models.Interval)
admin.site.register(models.ResultatEntrenament)
admin.site.register(models.ResultatInferencia)
