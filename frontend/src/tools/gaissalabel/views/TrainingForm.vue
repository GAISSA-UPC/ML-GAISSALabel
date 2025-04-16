<template>
    <FormNewExperiment :fase="$t('Training')" :dadesInicials="dadesInicials"/>
</template>

<script>
    import FormNewExperiment from "@/tools/gaissalabel/components/FormNewExperiment.vue";
    export default {
        name: "TrainingForm",
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