<template>
    <div class="gaissa-roi-analyzer-pre">
        <h1>{{ $t("GAISSA ROI Analyzer") }}</h1>
        <h2>{{ $t("Analysis Repository") }}</h2>

        <p class="description">
            {{ $t("This page allows you to consult the previously calculated Return on Investment (ROI) of applying a ML tactic to your model architecture.") }}
        </p>

        <el-form label-position="top" class="form-container">
            <h3 class="section-title">{{ $t("Model Architecture") }}</h3>
            <p class="field-description">{{ $t("Please, indicate the model architecture you are interested in.") }}</p>
            <el-form-item>
                <el-select v-model="selectedModelArchitecture" @change="onModelArchitectureChange" placeholder="Select" class="full-width"
                    filterable>
                    <el-option v-for="(modelArchitecture, i) in modelArchitectures" :key="i" :value="modelArchitecture.id" :label="modelArchitecture.name" />
                </el-select>
            </el-form-item>

            <div v-if="selectedModelArchitecture !== null">
                <h3 class="section-title">{{ $t("ML Tactic") }}</h3>
                <p class="field-description">{{ $t("Please, indicate the ML tactic you are interested in.")
                    }}</p>
                <el-form-item>
                    <el-select v-model="selectedMlTactic" @change="onMlTacticChange"
                        placeholder="Select" class="full-width">
                        <el-option v-for="(mlTactic, i) in mlTactics" :key="i" :value="mlTactic.id"
                            :label="mlTactic.name" />
                    </el-select>
                </el-form-item>
            </div>
            <div v-if="selectedMlTactic !== null && tacticParameters.length > 0">
                <h3 class="section-title">{{ $t("Tactic Parameter") }}</h3>
                <p class="field-description">{{ $t("Please, specify the parameter for the chosen tactic.") }}</p>
                <el-form-item>
                    <el-select v-model="selectedTacticParameter" @change="onTacticParameterChange"
                        placeholder="Select a parameter" class="full-width">
                        <el-option v-for="parameter in tacticParameters" :key="parameter.id"
                            :value="parameter.id" :label="`${parameter.name}: ${parameter.value}`" />
                    </el-select>
                </el-form-item>
            </div>

            <div v-if="selectedMlTactic !== null && selectedTacticParameter !== null">
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
                <el-button @click="calculateROI" class="action-button"
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
            modelArchitectures: [],
            selectedModelArchitecture: null,
            mlTactics: [],
            selectedMlTactic: null,
            experiments: [],
            selectedExperiment: null,
            tacticParameters: [],
            selectedTacticParameter: null,
        };
    },
    computed: {
        isFormValid() {
            return (
                this.selectedModelArchitecture !== null &&
                this.selectedMlTactic !== null &&
                this.selectedTacticParameter !== null &&
                this.selectedExperiment !== null
            );
        },
    },
    methods: {
        async refreshModelArchitectures() {
            const response = await modelArchitectures.list();
            if (response && response.data) {
                this.modelArchitectures = response.data;
            }
        },
        async refreshMlTactics() {
            const response = await mlTactics.getCompatibleTacticsWithArchitecture(this.selectedModelArchitecture);
            if (response && response.data) {
                this.mlTactics = response.data;
            }
        },
        async refreshTacticParameters() {
            const response = await tacticParameters.list(this.selectedMlTactic);
            if (response && response.data) {
                this.tacticParameters = response.data;
            }
        },
        async onModelArchitectureChange() {
            this.selectedMlTactic = null;
            this.tacticParameters = [];
            this.selectedTacticParameter = null;
            this.experiments = [];
            this.selectedExperiment = null;
            await this.refreshMlTactics();
        },
        async onMlTacticChange() {
            this.selectedTacticParameter = null;
            this.experiments = [];
            this.selectedExperiment = null;

            await this.refreshTacticParameters();
        },
        async onTacticParameterChange() {
            this.experiments = [];
            this.selectedExperiment = null;
            await this.refreshExperiments();
        },
        async refreshExperiments() {
            let params = {
                model_architecture: this.selectedModelArchitecture,
                tactic: this.selectedMlTactic,
                tactic_parameter_option: this.selectedTacticParameter,
            };
            
            if (this.selectedModelArchitecture && this.selectedTacticParameter && this.selectedMlTactic) {
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
        await this.refreshModelArchitectures();
    },
};
</script>

<style scoped>
h1 {
    color: var(--gaissa_green);
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.description {
    margin-bottom: 20px;
    margin-top: 20px;
    font-size: 20px;
}

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

.action-button {
    margin-top: 20px;
    background-color: var(--gaissa_green);
    color: white;
    border: none;
}

.action-button:hover {
    background-color: var(--gaissa_green);
    opacity: 0.9;
}

.action-button.is-disabled,
.action-button.is-disabled:hover,
.action-button.is-disabled:focus {
    background-color: #c0c4cc !important;
    color: white !important;
    cursor: not-allowed !important;
    opacity: 0.7;
}
</style>