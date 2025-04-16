<template>
    <LabelInfo :fase="$t('Inference')"/>
</template>

<script>
import LabelInfo from "@/tools/gaissalabel/components/LabelInfo.vue";
export default {
    name: "TrainingLabelInfo",
    components: {LabelInfo}
};
</script>

<style>
</style>