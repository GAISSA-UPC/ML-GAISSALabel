<template>
    <ROIInferencePre :fase="$t('ROI Inference Analysis')" />
</template>

<script>
import ROIInferencePre from "@/tools/gaissaroianalyzer/components/ROIInferencePre.vue";
export default {
    name: "ROIInferencePreSaved",
    components: { ROIInferencePre }
}
</script>

<style>
</style>