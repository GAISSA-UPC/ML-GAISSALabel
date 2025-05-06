<template>
    <h1>{{ $t('Welcome to GAISSALabel!') }}</h1><br>
    <h2 style="text-align: justify">{{  $t('The tool you are seeking for to easy assess the footprint of ML models and help you improve your models\' efficiency.') }}</h2><br>

    <h3>{{ $t('GAISSALabel is a tool that can assist you in evaluating both the training and inference phases of any machine learning model. \
    To navigate through the various available pages, utilize the left menu. \
    During both the training and inference phases, you have the capability to generate efficiency results for your models or retrieve existing ones.') }}</h3><br>
    <h3>{{ $t('For now, we have registered') }}</h3><br>
    <el-row justify="center" :gutter="30">
        <el-col :span="8">
            <el-card class="box-card" style="background-color: var(--gaissa_green_light);text-align: center">
                <h1 style="color: var(--gaissa_green)">{{ estadistiques.numModels }}</h1>
                <h2 style="color: var(--gaissa_green)">{{ $t('models') }}</h2>
            </el-card>
        </el-col>
        <el-col :span="8">
            <el-card class="box-card" style="background-color: var(--gaissa_green_light);text-align: center">
                <h1 style="color: var(--gaissa_green)">{{ estadistiques.numEntrenaments }}</h1>
                <h2 style="color: var(--gaissa_green)">{{ $t('trainings') }}</h2>
            </el-card>
        </el-col>
        <el-col :span="8">
            <el-card class="box-card" style="background-color: var(--gaissa_green_light);text-align: center">
                <h1 style="color: var(--gaissa_green)">{{ estadistiques.numInferencies }}</h1>
                <h2 style="color: var(--gaissa_green)">{{ $t('inferences') }}</h2>
            </el-card>
        </el-col>
    </el-row><br>
    <h3>{{ $t('We appreciate your trust. \
    Let us start the journey towards creating more environmentally friendly machine learning models!') }}</h3><br>
</template>

<script>
import estadistiques from "@/controllers/estadistiques";

export default {
    name: "HomeView",
    data() {
        return {
            estadistiques: {},
        };
    },
    methods: {
        async refrescaEstadistiques() {
            const response = await estadistiques.list()
            this.estadistiques = response.data
        },
    },
    async mounted() {
        await this.refrescaEstadistiques();
    },
};
</script>

<style>
h3 {
    text-align: justify
}
</style>
