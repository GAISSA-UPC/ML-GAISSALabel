<template>
    <AnalysisSelector 
        analysis-type="calculation"
        :repository-title="$t('Calculation Analysis Repository')"
        :repository-description="$t('This page allows you to consult previously calculated Return on Investment (ROI) analyses created through the calculation tool. These analyses represent estimations based on data entered in the ROI calculator.')"
        :analysis-selection-description="$t('Select a calculation analysis by its creation date:')"
    />
</template>

<script>
import AnalysisSelector from "@/tools/gaissaroianalyzer/components/AnalysisSelector.vue";

export default {
    name: "GAISSAROIAnalyzerCalculationRepository",
    components: { AnalysisSelector }
}
</script>

<style>
</style>
