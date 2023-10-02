<template>
    <FileNewExperiment :fase="$t('Training')"/>
</template>

<script>
import FileNewExperiment from "@/components/FileNewExperiment.vue";
export default {
    name: "TrainingFile",
    components: {FileNewExperiment}
};
</script>

<style>
</style>