<template>
    <LabelInfo :fase="$t('Inference')"/>
</template>

<script>
import LabelInfo from "@/components/LabelInfo.vue";
export default {
    name: "TrainingLabelInfo",
    components: {LabelInfo}
};
</script>

<style>
</style>