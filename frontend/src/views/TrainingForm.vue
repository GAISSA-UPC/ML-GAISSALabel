<template>
    <FormNewExperiment :fase="$t('Training')"/>
</template>

<script>
    import FormNewExperiment from "@/components/FormNewExperiment.vue";
    export default {
        name: "TrainingForm",
        components: {FormNewExperiment}
    };
</script>

<style>
</style>