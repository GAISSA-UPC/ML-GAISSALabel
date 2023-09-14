<template>
    <div>
        <el-slider range disabled :marks="marks" :max="max" :model-value="values"/>
    </div>
</template>

<script>
export default {
    name: "CustomSlider",
    props: {
        values: Object,
        marks: Object,
        max: Number,
        color: Object
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