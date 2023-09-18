<template>
    <FormNewExperiment :fase="$t('Inference')"/>
</template>

<script>
import FormNewExperiment from "@/components/FormNewExperiment.vue";
export default {
    name: "InferenceForm",
    components: {FormNewExperiment}
};
</script>

<style>
</style>