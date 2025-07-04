from django.contrib import admin
from .models import (
    ModelArchitecture, TacticSource, ROIMetric, MLTactic, TacticParameterOption,
    ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch,
    AnalysisMetricValue, EnergyAnalysisMetricValue, ExpectedMetricReduction
)


@admin.register(ModelArchitecture)
class ModelArchitectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'information')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(TacticSource)
class TacticSourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(ROIMetric)
class ROIMetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'is_energy_related', 'higher_is_better')
    list_filter = ('is_energy_related', 'higher_is_better')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(MLTactic)
class MLTacticAdmin(admin.ModelAdmin):
    list_display = ('name', 'information')
    search_fields = ('name',)
    filter_horizontal = ('sources', 'compatible_architectures', 'applicable_metrics')
    ordering = ('name',)


@admin.register(TacticParameterOption)
class TacticParameterOptionAdmin(admin.ModelAdmin):
    list_display = ('tactic', 'name', 'value')
    list_filter = ('tactic',)
    search_fields = ('tactic__name', 'name', 'value')
    ordering = ('tactic__name', 'name', 'value')


@admin.register(ROIAnalysis)
class ROIAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_architecture', 'tactic_parameter_option', 'country')
    list_filter = ('model_architecture', 'country')
    search_fields = ('model_architecture__name', 'tactic_parameter_option__tactic__name')
    ordering = ('-id',)


@admin.register(ROIAnalysisCalculation)
class ROIAnalysisCalculationAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_architecture', 'tactic_parameter_option', 'dateRegistration')
    list_filter = ('model_architecture', 'dateRegistration')
    search_fields = ('model_architecture__name', 'tactic_parameter_option__tactic__name')
    ordering = ('-dateRegistration',)


@admin.register(ROIAnalysisResearch)
class ROIAnalysisResearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_architecture', 'tactic_parameter_option', 'source')
    list_filter = ('model_architecture', 'source')
    search_fields = ('model_architecture__name', 'tactic_parameter_option__tactic__name', 'source__title')
    ordering = ('-id',)


@admin.register(AnalysisMetricValue)
class AnalysisMetricValueAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'metric', 'baselineValue')
    list_filter = ('metric', 'analysis__model_architecture')
    search_fields = ('analysis__model_architecture__name', 'metric__name')
    ordering = ('-analysis__id',)


@admin.register(EnergyAnalysisMetricValue)
class EnergyAnalysisMetricValueAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'metric', 'baselineValue', 'energy_cost_rate', 'implementation_cost')
    list_filter = ('metric', 'analysis__model_architecture')
    search_fields = ('analysis__model_architecture__name', 'metric__name')
    ordering = ('-analysis__id',)


@admin.register(ExpectedMetricReduction)
class ExpectedMetricReductionAdmin(admin.ModelAdmin):
    list_display = ('model_architecture', 'tactic_parameter_option', 'metric', 'expectedReductionValue')
    list_filter = ('model_architecture', 'metric')
    search_fields = ('model_architecture__name', 'tactic_parameter_option__tactic__name', 'metric__name')
    ordering = ('model_architecture__name', 'tactic_parameter_option__tactic__name')
