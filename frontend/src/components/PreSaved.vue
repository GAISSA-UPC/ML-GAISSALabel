<template>
    <h1>{{ $t("Energy label for") }} {{ fase }}</h1><br>
    <h2>{{ $t("Create label for dataset model") }}</h2><br>

    <p style="font-size: 20px">{{ $t('This page allows you to consult the energy efficiency of a') }} {{ fase }} {{ $t(' of a model.') }}</p>
    <br>

    <div>
        <el-form label-position="top">
            <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Model") }}</h3>
            <p>{{ $t('Please, indicate the model you are interested in.') }}</p><br>
            <el-form-item>
                <el-select
                    v-model="selectedModel"
                    @change="canviModel"
                    filterable
                >
                    <el-option
                        v-for="(model, i) in models" :key="i"
                        :value="model.id"
                        :label="model.nom"
                    />
                </el-select>
            </el-form-item><br>
            <div v-show="selectedModel != null">
                <h3 style="color: var(--gaissa_green);font-weight: bold">{{ fase }}</h3>
                <p>{{ $t('Now specify the') }} {{ fase }} {{ $t('from which you want to get the evaluation.') }}</p><br>
                <el-form-item>
                    <el-select
                        v-model="selectedExperiment"
                    >
                        <el-option
                            v-for="(experiment, i) in experiments" :key="i"
                            :value="experiment.id"
                            :label="formatData(experiment.dataRegistre)"
                        />
                    </el-select>
                </el-form-item>
            </div><br>
            <el-button
                @click="mostrarEtiqueta"
                color="var(--gaissa_green)"
                v-show="selectedExperiment != null"
            >
                {{ $t('Generate label') }}
            </el-button>
        </el-form><br>
    </div>
</template>

<script>
import models from '@/services/models'
import trainings from '@/services/trainings'
import inferencies from '@/services/inferencies'
import {formatData} from '@/utils'
export default {
    name: "PreSaved",
    props: {
        fase: {required: true, type: String}
    },
    data() {
        return {
            models: null,
            selectedModel: null,
            experiments: null,
            selectedExperiment: null,
        };
    },
    methods: {
        async refrescaModels() {
            const response = await models.list()
            this.models = response.data
        },
        async refrescaExperiments() {
            let response = null
            if (this.fase === this.$t('Training')) response = await trainings.listByModel(this.selectedModel)
            else response = await inferencies.listByModel(this.selectedModel)
            this.experiments = response.data
        },
        async canviModel() {
            await this.refrescaExperiments()
            this.selectedExperiment = null
        },
        async mostrarEtiqueta() {
            if (this.fase === this.$t('Training'))
                this.$router.push({
                    name: 'Label info for training',
                    params: {id_model: this.selectedModel, id_training: this.selectedExperiment}
                })
            else
                this.$router.push({
                    name: 'Label info for inference',
                    params: {id_model: this.selectedModel, id_inference: this.selectedExperiment}
                })

        },
        formatData,
    },
    async mounted() {
        await this.refrescaModels();
    },
};
</script>

<style>
</style>