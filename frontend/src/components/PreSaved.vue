<template>
    <h1>{{ $t("Energy label for") }} {{ fase }}</h1><br>
    <h2>{{ $t("Create label for dataset model") }}</h2><br>
    <div>
        <el-form label-position="top">
            <el-form-item :label="$t('Model')">
                <el-select
                    v-model="selectedModel"
                    @change="canviModel"
                >
                    <el-option
                        v-for="(model, i) in models" :key="i"
                        :value="model.id"
                        :label="model.nom"
                    />
                </el-select>
            </el-form-item>
            <el-form-item
                :label="fase"
                v-show="selectedModel != null"
            >
                <el-select
                    v-model="selectedExperiment"
                    @change="canviExperiment"
                >
                    <el-option
                        v-for="(experiment, i) in experiments" :key="i"
                        :value="experiment.id"
                        :label="formatData(experiment.dataRegistre)"
                    />
                </el-select>
            </el-form-item>
            <el-button
                @click="generarEtiqueta"
                color="var(--gaissa_green)"
                v-show="selectedExperiment != null"
            >
                {{ $t('Generate label') }}
            </el-button>
        </el-form><br>
        <EnergyLabel
            :pdfBase64="labelBase64"
            v-show="labelBase64"
        />
    </div>
</template>

<script>
import models from '@/services/models'
import trainings from '@/services/trainings'
import {formatData} from '@/utils'
import EnergyLabel from "@/components/EnergyLabel.vue";
export default {
    name: "PreSaved",
    components: {EnergyLabel},
    props: {
        fase: {required: true, type: String}
    },
    data() {
        return {
            models: null,
            selectedModel: null,
            experiments: null,
            selectedExperiment: null,
            labelBase64: null
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
            this.experiments = response.data
        },
        async canviModel() {
            await this.refrescaExperiments()
            this.selectedExperiment = null
            this.labelBase64 = null
        },
        async canviExperiment() {
            this.labelBase64 = null
        },
        async generarEtiqueta() {
            let response = null
            if (this.fase === this.$t('Training'))
                response = await trainings.retrieve(this.selectedModel, this.selectedExperiment)
            this.labelBase64 = response.data['energy_label']
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