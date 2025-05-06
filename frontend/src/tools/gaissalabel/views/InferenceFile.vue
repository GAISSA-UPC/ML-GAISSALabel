<template>
    <FileNewExperiment :fase="$t('Inference')"/>
</template>

<script>
import FileNewExperiment from "@/tools/gaissalabel/components/FileNewExperiment.vue";
export default {
    name: "InferenceFile",
    components: {FileNewExperiment}
};
</script>

<style>
</style>