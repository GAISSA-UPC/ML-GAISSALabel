<template>
    <h1>{{ $t("GAISSA ROI Analyzer") }}</h1><br>
    <h2>{{ $t("Register a new ROI Analysis") }}</h2><br>

    <div v-if="error">
        <el-alert :title="error" type="error" @close="error = ''"/>
        <br>
    </div>

    <p style="font-size: 20px">{{ $t('This page allows you to evaluate the impact of applying a machine learning tactic on a determined model architecture and calculate the expected Return on Investment (ROI). You may go through the following sections to provide the necessary information.') }}</p>
    <br>

    <el-form label-position="top">
        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Model Architecture and ML Tactic") }}</h3>
        <p>{{ $t('First, please indicate the model architecture you are working with.') }}</p><br>

        <el-form-item :label="$t('Model Architecture')" prop="modelArchitecture">
            <el-select 
                v-model="formData.modelArchitecture" 
                filterable 
                clearable 
                placeholder="Select"
                @change="handleModelArchChange"
                class="model-select">
                <el-option 
                    v-for="model in modelArchitectures" 
                    :key="model.id" 
                    :label="model.name" 
                    :value="model.id" />
            </el-select>
        </el-form-item>

        <el-form-item :label="$t('ML Tactic')" prop="mlTactic">
            <el-select 
                v-model="formData.mlTactic" 
                filterable 
                clearable 
                placeholder="Select"
                @change="handleTacticChange"
                class="model-select">
                <el-option 
                    v-for="tactic in tactics" 
                    :key="tactic.id" 
                    :label="tactic.name" 
                    :value="tactic.id" />
            </el-select>
        </el-form-item>

        <el-form-item :label="$t('Tactic Parameter')" prop="tacticParameter">
            <el-select 
                v-model="formData.tacticParameter" 
                filterable 
                clearable 
                placeholder="Select"
                class="model-select">
                <el-option 
                    v-for="parameter in tacticParameters" 
                    :key="parameter.id" 
                    :label="`${parameter.name}: ${parameter.value}`" 
                    :value="parameter.id" />
            </el-select>
        </el-form-item>
        <br>

        <div>
            <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Tactic Metrics") }}</h3>
            <p>{{ $t("Next, introduce the values for each of the metric described.") }}</p><br>

            <p v-if="!formData.mlTactic" style="color: grey;">
                {{ $t("Please select a model architecture and a machine learning tactic to see the applicable metrics.") }}
            </p>

            <el-form-item v-if="formData.mlTactic"
                v-for="metric in applicableMetrics" 
                :key="metric.id"
                :label="metric.name">
                <el-input-number 
                    v-model="metricValues[metric.id]" 
                    :precision="4" 
                    :step="0.01"
                    :min="0"
                    style="width: 200px"></el-input-number>
                <p style="margin-left: 10px">{{ metric.unit }}</p>
                <el-alert v-if="metric.description" type="info" show-icon :closable="false" style="margin-top: 10px">
                    <p style="font-size: 14px">{{ metric.description }}</p>
                </el-alert>
            </el-form-item>
            <br>
        </div>

        <el-button
            class="action-button"
            @click="generateROI"
            :disabled="!formIsValid || loading"
            :loading="loading">
            {{ $t("Generate ROI Analysis") }}
        </el-button>
    </el-form>
</template>

<script>
import modelArchitectures from "@/tools/gaissaroianalyzer/services/modelArchitectures";
import mlTactics from "@/tools/gaissaroianalyzer/services/mlTactics";
import roiMetrics from "@/tools/gaissaroianalyzer/services/roiMetrics";
import tacticParameters from "@/tools/gaissaroianalyzer/services/tacticParameters";
import roiAnalyses from "@/tools/gaissaroianalyzer/services/roiAnalyses";
import { ElMessage } from 'element-plus';

export default {
    name: "GAISSAROIAnalyzerNewForm",
    data() {
        return {
            modelArchitectures: [],
            tactics: [],
            tacticParameters: [],
            applicableMetrics: [],
            formData: {
                modelArchitecture: null,
                mlTactic: null,
                tacticParameter: null,
            },
            metricValues: {},
            loading: false,
            error: null,
        };
    },
    computed: {
        formIsValid() {
            const basicFormValid = this.formData.modelArchitecture && this.formData.mlTactic && this.formData.tacticParameter;
            
            // Check if we have metric values for all applicable metrics
            const metricsValid = this.applicableMetrics.every(metric => 
                this.metricValues[metric.id] !== undefined && this.metricValues[metric.id] !== null && this.metricValues[metric.id] > 0);
            
            return basicFormValid && metricsValid;
        }
    },
    methods: {
        async fetchModelArchitectures() {
            try {
                const response = await modelArchitectures.list();
                if (response && response.data) {
                    this.modelArchitectures = response.data;
                }
            } catch (error) {
                console.error("Error fetching model architectures:", error);
                this.error = "Failed to load model architectures. Please try again.";
            }
        },
        async fetchTacticsForModelArchitecture(architectureId) {
            try {
                const response = await mlTactics.getCompatibleTacticsWithArchitecture(architectureId);
                if (response && response.data) {
                    this.tactics = response.data;
                }
            } catch (error) {
                console.error(`Error fetching tactics for architecture ${architectureId}:`, error);
                this.error = "Failed to load available ML tactics. Please try again."
            }
        },
        async fetchTacticParameters() {
            if (!this.formData.mlTactic) {
                this.tacticParameters = [];
                return;
            }
            
            try {
                const response = await tacticParameters.list(this.formData.mlTactic);
                if (response && response.data) {
                    this.tacticParameters = response.data;
                }
            } catch (error) {
                console.error(`Error fetching parameters for tactic ${this.formData.mlTactic}:`, error);
                this.error = "Failed to load tactic parameters. Please try again.";
            }
        },
        async fetchApplicableMetrics() {
            if (!this.formData.mlTactic) {
                this.applicableMetrics = [];
                return;
            }
            
            try {
                const response = await roiMetrics.getAplicableMetrics(this.formData.mlTactic);
                if (response) {
                    this.applicableMetrics = response;

                    // Initialize metric values object with default values
                    this.applicableMetrics.forEach(metric => {
                        if (!this.metricValues[metric.id]) {
                            this.metricValues[metric.id] = 0;
                        }
                    });
                }
            } catch (error) {
                console.error(`Error fetching metrics for tactic ${this.formData.mlTactic}:`, error);
                this.error = "Failed to load applicable metrics. Please try again.";
            }
        },
        handleModelArchChange() {
            // Reset tactic selection
            this.formData.mlTactic = null;
            this.formData.tacticParameter = null;
            this.applicableMetrics = [];
            this.tacticParameters = [];
            
            // Fetch tactics compatible with the selected model architecture
            if (this.formData.modelArchitecture) {
                this.fetchTacticsForModelArchitecture(this.formData.modelArchitecture);
            } else {
                this.tactics = [];
            }
        },
        handleTacticChange() {
            // Reset tactic parameter selection and metrics
            this.formData.tacticParameter = null;
            this.metricValues = {};
            
            // Fetch parameters and metrics for the selected tactic
            this.fetchTacticParameters();
            this.fetchApplicableMetrics();
        },
        async generateROI() {
            if (!this.formIsValid) {
                this.error = 'Please fill in all required fields before generating the ROI analysis.';
                console.error(this.error);
                window.scrollTo({top: 0});
                return;
            }
            
            this.loading = true;
            this.error = null;
            
            try {
                const analysisData = {
                    model_architecture_id: parseInt(this.formData.modelArchitecture),
                    tactic_parameter_option_id: parseInt(this.formData.tacticParameter),
                    metric_values_data: Object.keys(this.metricValues).map(metricId => ({
                        metric_id: parseInt(metricId),
                        baselineValue: this.metricValues[metricId]
                    })),
                    country: "Catalunya",
                    analysis_type: "calculation" // Explicitly set analysis type
                };
                                
                //console.log('Sending data to API:', analysisData); // For debugging
                
                const response = await roiAnalyses.createAnalysis(analysisData);
                
                if (response && response.data) {
                    ElMessage({
                        message: 'ROI Analysis created successfully!',
                        type: 'success'
                    });
                    
                    // Redirect to analysis view page
                    this.$router.push({
                        name: 'GAISSA ROI Analyzer',
                        params: {
                            id_experiment: response.data.id 
                        }
                    });
                } else {
                    throw new Error('Invalid response received from server.');
                }
            } catch (error) {
                console.error("Error creating ROI analysis:", error);

                if (error.response && error.response.data) {
                    this.error = `Failed to create ROI analysis: ${JSON.stringify(error.response.data)}`;
                } else {
                    this.error = "Failed to create ROI analysis. Please check your inputs and network connection, and ensure you are logged in.";
                }
                window.scrollTo({top: 0});
            } finally {
                this.loading = false;
            }
        }
    },
    async mounted() {
        // Load initial data
        await this.fetchModelArchitectures();
    }
};
</script>

<style scoped>
h1 {
    color: var(--gaissa_green);
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

p {
    font-size: 18px;
}

.el-select {
    width: 200px;
}

.model-select {
    width: 300px;
}

.action-button {
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