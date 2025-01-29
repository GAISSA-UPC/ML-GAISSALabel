<template>
    <div class="roi-inference-pre">
        <h1>{{ $t("ROI Inference Optimization Calculator") }}</h1>
        <h2>{{ $t("Consult a new ROI Analysis") }}</h2>

        <p class="description">
            {{ $t("This page allows you to consult the previously calculated Return on Investment (ROI) of your models' Inferences.") }}
        </p>

        <el-form label-position="top" class="form-container">
            <h3 class="section-title">{{ $t("Model") }}</h3>
            <p class="field-description">{{ $t("Please, indicate the model you are interested in.") }}</p>
            <el-form-item>
                <el-select v-model="selectedModel" @change="onModelChange" placeholder="Select" class="full-width"
                    filterable>
                    <el-option v-for="(model, i) in models" :key="i" :value="model.id" :label="model.nom" />
                </el-select>
            </el-form-item>

            <div v-if="selectedModel !== null">
                <h3 class="section-title">{{ $t("Optimization Technique") }}</h3>
                <p class="field-description">{{ $t("Please, indicate the optimization technique you are interested in.")
                    }}</p>
                <el-form-item>
                    <el-select v-model="selectedOptimizationTechnique" @change="onOptimizationTechniqueChange"
                        placeholder="Select" class="full-width">
                        <el-option v-for="(technique, i) in optimizationTechniques" :key="i" :value="technique.id"
                            :label="technique.name" />
                    </el-select>
                </el-form-item>
            </div>
            <div v-if="selectedOptimizationTechnique !== null && optimizationTechniqueParameters.length > 0">
                <h3 class="section-title">{{ $t("Technique Parameters") }}</h3>
                <p class="field-description">{{ $t("Please, specify the parameters for the chosen technique.") }}</p>
                <el-form-item>
                    <el-select v-model="selectedOptimizationParameter" @change="onOptimizationParameterChange"
                        placeholder="Select a parameter" class="full-width">
                        <el-option v-for="parameter in optimizationTechniqueParameters" :key="parameter.id"
                            :value="parameter.id" :label="parameter.name" />
                    </el-select>
                </el-form-item>
            </div>

            <div v-if="selectedOptimizationTechnique !== null && (optimizationTechniqueParameters.length === 0 || selectedOptimizationParameter !== null)">
                <h3 class="section-title">{{ $t("Analysis") }}</h3>
                <p class="field-description">
                    {{ $t('Now specify the') }} {{ fase }} {{ $t('from which you want to get the evaluation.') }}
                </p>
                <el-form-item>
                    <el-select v-model="selectedExperiment" placeholder="Select" class="full-width">
                        <el-option v-for="(experiment, i) in experiments" :key="i" :value="experiment.id"
                            :label="formatData(experiment.registration_date)" />
                    </el-select>
                </el-form-item>
            </div>

            <el-form-item>
                <el-button @click="calculateROI" color="var(--gaissa_green)" class="submit-button"
                    :disabled="!isFormValid">
                    {{ $t("Load ROI Analysis") }}
                </el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import models from "@/controllers/models";
import optimizationTechniques from "@/controllers/optimizationTechniques";
import techniqueParameters from "@/controllers/techniqueParameters";
import roiAnalyses from "@/controllers/roiAnalyses";
import { formatData } from "@/utils";

export default {
    name: "ROIInferencePre",
    props: {
        fase: { required: true, type: String },
    },
    data() {
        return {
            models: [],
            selectedModel: null,
            optimizationTechniques: [],
            selectedOptimizationTechnique: null,
            experiments: [],
            selectedExperiment: null,
            optimizationTechniqueParameters: [],
            selectedOptimizationParameter: null,
        };
    },
    computed: {
        isFormValid() {
            return (
                this.selectedModel !== null &&
                this.selectedOptimizationTechnique !== null &&
                (this.optimizationTechniqueParameters.length === 0 || this.selectedOptimizationParameter !== null) &&
                this.selectedExperiment !== null
            );
        },
    },
    methods: {
        async refreshModels() {
            const response = await models.list({ has_roi_analysis: "true" });
            this.models = response.data;
        },
        async refreshOptimizationTechniques() {
            const response = await optimizationTechniques.list({ model_id: this.selectedModel });
            this.optimizationTechniques = response.data;
        },
        async refreshOptimizationTechniqueParameters() {
            const response = await techniqueParameters.list({ model_id: this.selectedModel, optimization_technique_id: this.selectedOptimizationTechnique });
            this.optimizationTechniqueParameters = response.data;
        },
        async onModelChange() {
            this.selectedOptimizationTechnique = null;
            this.optimizationTechniqueParameters = [];
            this.selectedOptimizationParameter = null;
            this.experiments = [];
            this.selectedExperiment = null;
            await this.refreshOptimizationTechniques();
        },
        async onOptimizationTechniqueChange() {
            this.selectedOptimizationParameter = null;
            this.experiments = [];
            this.selectedExperiment = null;

            await this.refreshOptimizationTechniqueParameters();

            if (this.optimizationTechniqueParameters.length === 0) {
                await this.refreshExperiments();
            }
        },
        async onOptimizationParameterChange() {
            this.experiments = [];
            this.selectedExperiment = null;
            await this.refreshExperiments();
        },
        async refreshExperiments() {
            let params = {
                optimization_technique_id: this.selectedOptimizationTechnique,
            };
            if (this.selectedOptimizationParameter) {
                params.technique_parameter_id = this.selectedOptimizationParameter;
            }
            if (this.selectedModel && this.selectedOptimizationTechnique) {
                const response = await roiAnalyses.listByModel(this.selectedModel, params);
                this.experiments = response.data;
            } else {
                this.experiments = [];
            }
        },
        async calculateROI() {
            this.$router.push({
                name: "ROI Inference Analysis",
                params: {
                    id_model: this.selectedModel,
                    id_experiment: this.selectedExperiment,
                },
            });
        },
        formatData,
    },
    async mounted() {
        await this.refreshModels();
    },
};
</script>

<style scoped>
.form-container {
    max-width: 600px;
    margin: 0;
}

.section-title {
    color: var(--gaissa_green);
    font-weight: bold;
    margin-top: 20px;
}

.field-description {
    margin-bottom: 10px;
}

.full-width {
    width: 100%;
}

.submit-button {
    margin-top: 20px;
    background-color: var(--gaissa_green);
    color: white;
}
</style>