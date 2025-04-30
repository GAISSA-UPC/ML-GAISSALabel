from django.contrib import admin
from api import models

# GAISSALabel models
admin.site.register(models.Model)
admin.site.register(models.Entrenament)
admin.site.register(models.Inferencia)
admin.site.register(models.Metrica)
admin.site.register(models.Qualificacio)
admin.site.register(models.Interval)
admin.site.register(models.ResultatEntrenament)
admin.site.register(models.ResultatInferencia)
admin.site.register(models.InfoAddicional)
admin.site.register(models.ValorInfoEntrenament)
admin.site.register(models.ValorInfoInferencia)
admin.site.register(models.EinaCalcul)
admin.site.register(models.TransformacioMetrica)
admin.site.register(models.TransformacioInformacio)
admin.site.register(models.Administrador)
admin.site.register(models.Configuracio)

# GAISSA ROI Analyzer models
admin.site.register(models.ModelArchitecture)
admin.site.register(models.TacticSource)
admin.site.register(models.MLTactic)
admin.site.register(models.TacticParameterOption)
admin.site.register(models.ROIAnalysis)
admin.site.register(models.ROIAnalysisCalculation)
admin.site.register(models.ROIAnalysisResearch)
admin.site.register(models.ROIMetric)
admin.site.register(models.AnalysisMetricValue)
admin.site.register(models.EnergyAnalysisMetricValue)
admin.site.register(models.ExpectedMetricReduction)