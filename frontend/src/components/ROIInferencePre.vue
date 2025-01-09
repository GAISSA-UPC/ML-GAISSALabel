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

            <div v-if="selectedOptimizationTechnique !== null && techniqueParameters.length > 0">
                <h3 class="section-title">{{ $t("Technique Parameters") }}</h3>
                <p class="field-description">{{ $t("Please, specify the parameters for the chosen technique.") }}</p>
                <el-form-item>
                    <el-select v-model="selectedParameter" @change="onParameterChange" placeholder="Select"
                        class="full-width">
                        <el-option v-for="(option, i) in techniqueParameters[0].options" :key="i" :value="option.value"
                            :label="option.label" />
                    </el-select>
                </el-form-item>
            </div>

            <div v-if="selectedModel !== null && (techniqueParameters.length === 0 || selectedParameter !== null)">
                <h3 class="section-title">{{ $t("Analysis") }}</h3>
                <p class="field-description">
                    {{ $t('Now specify the') }} {{ fase }} {{ $t('from which you want to get the evaluation.') }}
                </p>
                <el-form-item>
                    <el-select v-model="selectedExperiment" placeholder="Select"
                        class="full-width">
                        <el-option v-for="(experiment, i) in experiments" :key="i" :value="experiment.id"
                            :label="formatData(experiment.dataRegistre)" />
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
import inferencies from "@/controllers/inferencies";
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
            techniqueParameters: [],
            selectedParameter: null,
            experiments: [],
            selectedExperiment: null,
        };
    },
    computed: {
        isFormValid() {
            return (
                this.selectedModel !== null &&
                this.selectedOptimizationTechnique !== null &&
                (this.techniqueParameters.length === 0 || this.selectedParameter !== null) &&
                this.selectedExperiment !== null
            );
        },
    },
    methods: {
        async refrescaModels() {
            const response = await models.list();
            this.models = response.data;
        },
        async refrescaExperiments() {
            const response = await inferencies.listByModel(this.selectedModel);
            this.experiments = response.data;
        },
        async onModelChange() {
            this.selectedOptimizationTechnique = null;
            this.techniqueParameters = [];
            this.selectedParameter = null;
            this.experiments = [];
            this.selectedExperiment = null;

            await this.refrescaExperiments();

            // Fetch optimization techniques for the selected model (replace with your actual API call)
            // Example:
            this.optimizationTechniques = [
                { id: "dynamic_quantization", name: "Dynamic Quantization" },
                { id: "local_pruning", name: "Local Pruning" },
                { id: "global_pruning", name: "Global Pruning" },
            ];

            this.techniqueParameters = [
                    {
                        id: "temp",
                        label: "temp",
                        options: [
                            { label: "25%", value: 0.25 },
                            { label: "50%", value: 0.5 },
                            { label: "75%", value: 0.75 },
                        ],
                    },
                ];
        },
        async onOptimizationTechniqueChange() {
            this.selectedParameter = null;
            this.experiments = this.experiments//.filter(experiment => experiment.optimization_technique === this.selectedOptimizationTechnique);
            this.selectedExperiment = null;

            if (this.selectedOptimizationTechnique === "local_pruning" || this.selectedOptimizationTechnique === "global_pruning") {
                this.techniqueParameters = [
                    {
                        id: "pruning_percentage",
                        label: "Pruning Percentage",
                        options: [
                            { label: "25%", value: 0.25 },
                            { label: "50%", value: 0.5 },
                            { label: "75%", value: 0.75 },
                        ],
                    },
                ];
            } else {
                this.techniqueParameters = [];
            }
        },
        async onParameterChange() {
            this.experiments = this.experiments//.filter(experiment => experiment.parameter === this.selectedParameter);
            this.selectedExperiment = null;
        },
        async calculateROI() {
            this.$router.push({
                name: "ROI Inference Analysis",
                params: {
                    id_model: this.selectedModel,
                    optimization_technique: this.selectedOptimizationTechnique,
                    technique_param: this.selectedParameter,
                    id_experiment: this.selectedExperiment,
                },
            });
        },
        formatData,
    },
    async mounted() {
        await this.refrescaModels();
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