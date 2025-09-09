<template>
    <div class="gaissa-roi-analyzer-pre">
        <h1>{{ $t("GAISSA ROI Analyzer") }}</h1>
        <h2>{{ repositoryTitle }}</h2>

        <p class="description">
            {{ repositoryDescription }}
        </p>

        <el-form label-position="top" class="form-container">
            <h3 class="section-title">{{ $t("Model Architecture") }}</h3>
            <p class="field-description">
                {{ $t("Please, indicate the model architecture you are interested in.") }}
                <el-tooltip v-if="!comparisonMode" placement="top" :content="$t('Model architecture refers to the specific structure and framework of a machine learning or deep learning system (e.g., SVM, KNN, AlexNet, GoogLeNet). Different architectures have distinct design principles and computational requirements, which influence both their performance and their environmental impact.')">
                    <el-icon class="info-icon"><InfoFilled /></el-icon>
                </el-tooltip>
            </p>
            <el-form-item>
                <el-select v-model="selectedModelArchitecture" @change="onModelArchitectureChange" placeholder="Select"
                    filterable>
                    <el-option v-for="(modelArchitecture, i) in modelArchitectures" :key="i" :value="modelArchitecture.id" :label="modelArchitecture.name" />
                </el-select>
            </el-form-item>

            <div v-if="selectedModelArchitecture !== null">
                <h3 class="section-title">{{ $t("ML Tactic") }}</h3>
                <p class="field-description">{{ $t("Please, indicate the ML tactic you are interested in.") }}
                    <el-tooltip v-if="!comparisonMode" placement="top" :content="$t('ML tactics are optimization techniques applied to machine learning models to enhance efficiency (e.g., pruning). These tactics aim to reduce computational and energy costs while preserving or minimally impacting model performance.')">
                        <el-icon class="info-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                </p>
                <el-form-item>
                    <el-select v-model="selectedMlTactic" @change="onMlTacticChange"
                        placeholder="Select">
                        <el-option v-for="(mlTactic, i) in mlTactics" :key="i" :value="mlTactic.id"
                            :label="mlTactic.name" />
                    </el-select>
                </el-form-item>
            </div>
            <div v-if="selectedMlTactic !== null && tacticParameters.length > 0">
                <h3 class="section-title">{{ $t("Tactic Parameter") }}</h3>
                <p class="field-description">{{ $t("Please, specify the parameter for the chosen tactic.") }}
                    <el-tooltip v-if="!comparisonMode" placement="top" :content="$t('Tactic parameters define specific configurations or settings for the selected ML tactic. These parameters directly influence how aggressively the optimization is applied.')">
                        <el-icon class="info-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                </p>
                <el-form-item>
                    <el-select v-model="selectedTacticParameter" @change="onTacticParameterChange"
                        placeholder="Select a parameter">
                        <el-option v-for="parameter in tacticParameters" :key="parameter.id"
                            :value="parameter.id" :label="`${parameter.name}: ${parameter.value}`" />
                    </el-select>
                </el-form-item>
            </div>

            <div v-if="selectedMlTactic !== null && selectedTacticParameter !== null">
                <h3 class="section-title">{{ $t("Analysis") }}</h3>
                <p class="field-description">
                    {{ analysisSelectionDescription }}
                </p>
                <el-form-item>
                    <el-select v-model="selectedExperiment" placeholder="Select">
                        <el-option v-for="(experiment, i) in experiments" :key="i" :value="experiment.id"
                            :label="formatLabel(experiment)" />
                    </el-select>
                </el-form-item>
            </div>

            <el-form-item>
                <el-button @click="loadAnalysis" class="action-button"
                    :disabled="!isFormValid">
                    {{ getButtonText() }}
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
import { InfoFilled } from '@element-plus/icons-vue'

export default {
    name: "AnalysisSelector",
    components: { InfoFilled },
    props: {
        analysisType: { 
            required: true, 
            type: String,
            validator: function (value) {
                return ['calculation', 'research'].includes(value);
            }
        },
        repositoryTitle: {
            required: true, 
            type: String
        },
        repositoryDescription: {
            required: true, 
            type: String
        },
        analysisSelectionDescription: {
            required: true, 
            type: String
        },
        comparisonMode: {
            type: Boolean,
            default: false
        }
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
            analysisSelected: false,
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
    watch: {
        selectedExperiment() {
            // Reset selection feedback when experiment changes
            this.resetSelection();
        },
        async analysisType() {
            // Reset all selections when analysis type changes
            this.selectedModelArchitecture = null;
            this.selectedMlTactic = null;
            this.selectedTacticParameter = null;
            this.selectedExperiment = null;
            this.mlTactics = [];
            this.tacticParameters = [];
            this.experiments = [];
            this.resetSelection();
            
            // Refresh model architectures for the new analysis type
            await this.refreshModelArchitectures();
        }
    },
    methods: {
        async refreshModelArchitectures() {
            const params = {
                analysis_type: this.analysisType
            };
            const response = await modelArchitectures.list(params);
            if (response && response.data) {
                this.modelArchitectures = response.data;
            }
        },
        async refreshMlTactics() {
            const params = {
                analysis_type: this.analysisType
            };
            const response = await mlTactics.getCompatibleTacticsWithArchitecture(this.selectedModelArchitecture, params);
            if (response && response.data) {
                this.mlTactics = response.data;
            }
        },
        async refreshTacticParameters() {
            if (!this.selectedMlTactic) {
                this.tacticParameters = [];
                return;
            }

            const filter = {
                model_architecture: this.selectedModelArchitecture,
                analysis_type: this.analysisType,
            };

            const response = await tacticParameters.list(this.selectedMlTactic, filter);
            if (response && response.data) {
                this.tacticParameters = response.data;
            }
        },
        async onModelArchitectureChange() {
            this.selectedMlTactic = null;
            this.tacticParameters = [];
            this.mlTactics = [];
            this.selectedTacticParameter = null;
            this.experiments = [];
            this.selectedExperiment = null;
            this.resetSelection();
            await this.refreshMlTactics();
        },
        async onMlTacticChange() {
            this.selectedTacticParameter = null;
            this.experiments = [];
            this.tacticParameters = [];
            this.selectedExperiment = null;
            this.resetSelection();

            await this.refreshTacticParameters();
        },
        async onTacticParameterChange() {
            this.experiments = [];
            this.selectedExperiment = null;
            this.resetSelection();
            await this.refreshExperiments();
        },
        async refreshExperiments() {
            let params = {
                model_architecture: this.selectedModelArchitecture,
                tactic: this.selectedMlTactic,
                tactic_parameter_option: this.selectedTacticParameter,
                analysis_type: this.analysisType
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
        formatLabel(experiment) {
            // Format the label differently based on analysis type
            if (this.analysisType === 'calculation' && experiment.dateRegistration) {
                return formatData(experiment.dateRegistration);
            } else if (this.analysisType === 'research' && experiment.source) {
                return experiment.source.title;
            }
            return `Analysis ${experiment.id}`;
        },
        async loadAnalysis() {
            this.analysisSelected = true;

            // Emit the selected analysis ID for parent components that might need it
            this.$emit('analysisSelected', this.selectedExperiment);
            
            // If in comparison mode, don't navigate to the analysis page
            if (this.comparisonMode) {
                return;
            }
            
            this.$router.push({
                name: "GAISSA ROI Analyzer Analysis",
                params: {
                    id_experiment: this.selectedExperiment,
                },
            });
        },
        resetSelection() {
            this.analysisSelected = false;
        },
        getButtonText() {
            if (this.comparisonMode) {
                return this.analysisSelected ? this.$t("Analysis Selected ✓") : this.$t("Select Analysis");
            }
            return this.$t("Load ROI Analysis");
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

.el-select {
    max-width: 600px;
}

.submit-button {
    margin-top: 20px;
    background-color: var(--gaissa_green);
    color: white;
}

.action-button,
.action-button:focus {
    margin-top: 20px;
    background-color: var(--gaissa_green) !important;
    color: white !important;
    border: none;
}

.action-button:hover,
.action-button:active {
    background-color: white !important;
    color: var(--gaissa_green) !important;
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

.info-icon {
    margin-left: 6px;
    color: var(--el-color-info);
    cursor: help;
    vertical-align: middle;
}
</style>
