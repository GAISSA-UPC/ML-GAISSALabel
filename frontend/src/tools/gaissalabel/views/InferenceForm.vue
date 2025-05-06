<template>
    <FormNewExperiment :fase="$t('Inference')" :dadesInicials="dadesInicials"/>
</template>

<script>
import FormNewExperiment from "@/tools/gaissalabel/components/FormNewExperiment.vue";
export default {
    name: "InferenceForm",
    components: {FormNewExperiment},
    computed: {
        dadesInicials() {
            const dades = this.$route.query.dadesInicials
            return (dades) ? JSON.parse(dades) : null;
        },
    }
};
</script>

<style>
</style>