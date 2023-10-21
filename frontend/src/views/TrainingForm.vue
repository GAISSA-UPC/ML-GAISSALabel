<template>
    <FormNewExperiment :fase="$t('Training')" :dadesInicials="dadesInicials"/>
</template>

<script>
    import FormNewExperiment from "@/components/FormNewExperiment.vue";
    export default {
        name: "TrainingForm",
        components: {FormNewExperiment},
        computed: {
            dadesInicials() {
                const dades = this.$route.params.dadesInicials
                return (dades) ? JSON.parse(dades) : null;
            },
        }
    };
</script>

<style>
</style>