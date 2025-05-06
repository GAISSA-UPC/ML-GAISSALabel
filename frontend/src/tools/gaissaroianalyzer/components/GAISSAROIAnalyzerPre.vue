<template>
    <div class="gaissa-roi-analyzer-pre">
        <h1>{{ $t("GAISSA ROI Analyzer") }}</h1>
        <h2>{{ $t("Consult a new ROI Analysis") }}</h2>

        <p class="description">
            {{ $t("This page allows you to consult the previously calculated Return on Investment (ROI) of your models' Inferences.") }}
        </p>

        <el-form label-position="top" class="form-container">
            <h3 class="section-title">{{ $t("Model Architecture") }}</h3>
            <p class="field-description">{{ $t("Please, indicate the model architecture you are interested in.") }}</p>
            <el-form-item>
                <el-select v-model="selectedModel" @change="onModelChange" placeholder="Select" class="full-width"
                    filterable>
                    <el-option v-for="(model, i) in models" :key="i" :value="model.id" :label="model.name" />
                </el-select>
            </el-form-item>

            <div v-if="selectedModel !== null">
                <h3 class="section-title">{{ $t("ML Tactic") }}</h3>
                <p class="field-description">{{ $t("Please, indicate the ML tactic you are interested in.")
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
                <h3 class="section-title">{{ $t("Tactic Parameter") }}</h3>
                <p class="field-description">{{ $t("Please, specify the parameter for the chosen tactic.") }}</p>
                <el-form-item>
                    <el-select v-model="selectedOptimizationParameter" @change="onOptimizationParameterChange"
                        placeholder="Select a parameter" class="full-width">
                        <el-option v-for="parameter in optimizationTechniqueParameters" :key="parameter.id"
                            :value="parameter.id" :label="`${parameter.name}: ${parameter.value}`" />
                    </el-select>
                </el-form-item>
            </div>

            <div v-if="selectedOptimizationTechnique !== null && selectedOptimizationParameter !== null">
                <h3 class="section-title">{{ $t("Analysis") }}</h3>
                <p class="field-description">
                    {{ $t('Now specify the') }} {{ fase }} {{ $t('from which you want to get the evaluation.') }}
                </p>
                <el-form-item>
                    <el-select v-model="selectedExperiment" placeholder="Select" class="full-width">
                        <el-option v-for="(experiment, i) in experiments" :key="i" :value="experiment.id"
                            :label="formatData(experiment.dateRegistration)" />
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
import modelArchitectures from "@/tools/gaissaroianalyzer/services/modelArchitectures";
import mlTactics from "@/tools/gaissaroianalyzer/services/mlTactics";
import tacticParameters from "@/tools/gaissaroianalyzer/services/tacticParameters";
import roiAnalyses from "@/tools/gaissaroianalyzer/services/roiAnalyses";
import { formatData } from "@/utils";

export default {
    name: "GAISSAROIAnalyzerPre",
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
                this.selectedOptimizationParameter !== null &&
                this.selectedExperiment !== null
            );
        },
    },
    methods: {
        async refreshModels() {
            const response = await modelArchitectures.list();
            if (response && response.data) {
                this.models = response.data;
            }
        },
        async refreshOptimizationTechniques() {
            const response = await mlTactics.getCompatibleTacticsWithArchitecture(this.selectedModel);
            if (response && response.data) {
                this.optimizationTechniques = response.data;
            }
        },
        async refreshOptimizationTechniqueParameters() {
            const response = await tacticParameters.list(this.selectedOptimizationTechnique);
            if (response && response.data) {
                this.optimizationTechniqueParameters = response.data;
            }
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
        },
        async onOptimizationParameterChange() {
            this.experiments = [];
            this.selectedExperiment = null;
            await this.refreshExperiments();
        },
        async refreshExperiments() {
            let params = {
                model_architecture_id: this.selectedModel,
                tactic_parameter_option_id: this.selectedOptimizationParameter,
                tactic_id: this.selectedOptimizationTechnique,
            };
            
            if (this.selectedModel && this.selectedOptimizationParameter && this.selectedOptimizationTechnique) {
                const response = await roiAnalyses.list(params);
                if (response && response.data) {
                    this.experiments = response.data;
                }
            } else {
                this.experiments = [];
            }
        },
        async calculateROI() {
            this.$router.push({
                name: "GAISSA ROI Analyzer",
                params: {
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