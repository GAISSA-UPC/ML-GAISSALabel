<template>
    <h1>{{ $t("Energy label for training") }}</h1><br>
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
                :label="$t('Training')"
                v-show="selectedModel != null"
            >
                <el-select
                    v-model="selectedTraining"
                    @change="canviTraining"
                >
                    <el-option
                        v-for="(training, i) in trainings" :key="i"
                        :value="training.id"
                        :label="formatData(training.dataRegistre)"
                    />
                </el-select>
            </el-form-item>
            <el-button
                @click="generarEtiqueta"
                class="action-button-light"
                v-show="selectedTraining != null"
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
        name: "TrainingPreSaved",
        components: {EnergyLabel},
        data() {
            return {
                models: null,
                selectedModel: null,
                trainings: null,
                selectedTraining: null,
                labelBase64: null
            };
        },
        methods: {
            async refrescaModels() {
                const response = await models.list()
                this.models = response.data
            },
            async refrescaEntrenaments() {
                const response = await trainings.listByModel(this.selectedModel)
                this.trainings = response.data
            },
            async canviModel() {
                await this.refrescaEntrenaments()
                this.selectedTraining = null
                this.labelBase64 = null
            },
            async canviTraining() {
                this.labelBase64 = null
            },
            async generarEtiqueta() {
                const response = await trainings.retrieve(this.selectedModel, this.selectedTraining)
                this.labelBase64 = response.data['energy_label']
            },
            formatData,
        },
        async mounted() {
            await this.refrescaModels();
        },
        beforeUnmount() {
            // Revoke the URL object to free up memory when the component is destroyed
            if (this.pdfURL) {
                URL.revokeObjectURL(this.pdfURL);
            }
        }
    };
</script>

<style>
</style>