<template>
    <div>
        <el-slider range disabled :marks="marks" :max="max" :model-value="values"/>
    </div>
</template>

<script>
export default {
    name: "CustomSlider",
    props: {
        values: Object, // Values to show in the slider: [min, max]
        marks: Object,  // Points to show in the slider: {0: 'Low', 50: 'Medium', 100: 'High'}
        max: Number,    // Maximum value of the slider: 100
        color: String
    },
    data() {
        return {
            sliderColor: this.color,
        }
    }
}
</script>
<style>
.el-slider__runway.is-disabled .el-slider__bar {
    background-color: v-bind(sliderColor) !important;
}
</style>