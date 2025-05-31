<template>
    <AnalysisSelector 
        analysis-type="research"
        :repository-title="$t('Research Analysis Repository')"
        :repository-description="$t('This page allows you to consult research-based Return on Investment (ROI) analyses created by administrators. These analyses are based on real data extracted from research papers and form the foundation for calculation-based estimations.')"
        :analysis-selection-description="$t('Select a research analysis by its source:')"
    />
</template>

<script>
import AnalysisSelector from "@/tools/gaissaroianalyzer/components/AnalysisSelector.vue";

export default {
    name: "GAISSAROIAnalyzerResearchRepository",
    components: { AnalysisSelector }
}
</script>

<style>
</style>
