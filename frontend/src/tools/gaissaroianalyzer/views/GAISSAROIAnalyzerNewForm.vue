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
        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("ML Tactic and Model Architecture") }}</h3>
        <p>{{ $t('First, please indicate the ML tactic you want to evaluate.') }}</p><br>

        <el-form-item prop="mlTactic">
            <template #label>
                {{ $t('ML Tactic') }}
                <el-tooltip placement="top" :content="$t('ML tactics are optimization techniques applied to machine learning models to enhance efficiency (e.g., pruning). These tactics aim to reduce computational and energy costs while preserving or minimally impacting model performance.')">
                    <el-icon class="info-icon"><InfoFilled /></el-icon>
                </el-tooltip>
            </template>
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

        <el-form-item prop="modelArchitecture">
            <template #label>
                {{ $t('Model Architecture') }}
                <el-tooltip placement="top" :content="$t('Model architecture refers to the specific structure and framework of a machine learning or deep learning system (e.g., SVM, KNN, AlexNet, GoogLeNet). Different architectures have distinct design principles and computational requirements, which influence both their performance and their environmental impact.')">
                    <el-icon class="info-icon"><InfoFilled /></el-icon>
                </el-tooltip>
            </template>
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

        <el-form-item prop="tacticParameter">
            <template #label>
                {{ $t('Tactic Parameter') }}
                <el-tooltip placement="top" :content="$t('Tactic parameters define specific configurations or settings for the selected ML tactic. These parameters directly influence how aggressively the optimization is applied.')">
                    <el-icon class="info-icon"><InfoFilled /></el-icon>
                </el-tooltip>
            </template>
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
            <p>{{ $t("Next, introduce the values for each of the metrics described.") }}</p><br>

            <p v-if="!formData.mlTactic" style="color: grey;">
                {{ $t("Please select an ML tactic and a model architecture to see the applicable metrics.") }}
            </p>

            <el-form-item v-if="formData.mlTactic"
                v-for="metric in applicableMetrics" 
                :key="metric.id">
                <template #label>
                    <span>{{ metric.name }}</span>
                    <el-tooltip v-if="metric.description" placement="top" :content="metric.description">
                        <el-icon class="info-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                </template>
                <el-input-number 
                    v-model="metricValues[metric.id]" 
                    :precision="8" 
                    :step="0.01"
                    :min="metric.min_value !== null ? metric.min_value : 0"
                    :max="metric.max_value !== null ? metric.max_value : undefined"
                    style="width: 200px"></el-input-number>
                <p style="margin-left: 10px">{{ metric.unit }}</p>
                <el-alert v-if="metric.min_value !== null || metric.max_value !== null" type="warning" show-icon :closable="false" style="margin-top: 10px">
                    <p style="font-size: 14px">
                      <template v-if="metric.min_value !== null && metric.max_value !== null">
                        {{ $t(`Valid range: ${metric.min_value} - ${metric.max_value} ${metric.unit || ''}`) }}
                      </template>
                      <template v-else-if="metric.min_value !== null">
                        {{ $t(`Minimum value: ${metric.min_value} ${metric.unit || ''}`) }}
                      </template>
                      <template v-else-if="metric.max_value !== null">
                        {{ $t(`Maximum value: ${metric.max_value} ${metric.unit || ''}`) }}
                      </template>
                    </p>
                </el-alert>
            </el-form-item>
            <br>
        </div>

        <div v-if="hasEnergyRelatedMetrics">
            <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Cost Metrics") }}</h3>
            <p>{{ $t("Next, introduce the metrics to assess the economic impact of applying the tactic and estimate the ROI (Return on Investment) of the approach.") }}</p><br>

            <div v-for="metric in energyRelatedMetrics" :key="`cost-${metric.id}`">
                <h4 v-if="energyRelatedMetrics.length > 1">{{ metric.name }} - {{ $t('Cost Information') }}</h4>
                
                <el-form-item>
                    <template #label>
                        {{ $t('Energy Cost Rate (€/kWh)') }}
                        <el-tooltip placement="top" :content="$t('The cost of the electricity supply used.')">
                            <el-icon class="info-icon"><InfoFilled /></el-icon>
                        </el-tooltip>
                    </template>
                    <el-input-number 
                        v-model="energyCostRates[metric.id]" 
                        :precision="6" 
                        :step="0.001"
                        :min="0"
                        style="width: 200px"></el-input-number>
                </el-form-item>
                
                <el-form-item>
                    <template #label>
                        {{ $t('Implementation Cost (€)') }}
                        <el-tooltip placement="top" :content="$t('The cost associated with implementing the ML tactic, including development, testing, and deployment costs.')">
                            <el-icon class="info-icon"><InfoFilled /></el-icon>
                        </el-tooltip>
                    </template>
                    <el-input-number 
                        v-model="implementationCosts[metric.id]" 
                        :precision="8"
                        :step="0.01"
                        :min="0"
                        style="width: 200px"></el-input-number>
                </el-form-item>
            </div>
            <br>
        </div>

        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Location Information") }}</h3>
        <p>{{ $t("Please specify the country or region where the model is being deployed.") }}</p><br>

        <el-form-item prop="country">
            <template #label>
                {{ $t('Country') }}
                <el-tooltip placement="top" :content="$t('The country or region specified will be used to determine the carbon intensity of the electricity supply.')">
                    <el-icon class="info-icon"><InfoFilled /></el-icon>
                </el-tooltip>
            </template>
            <el-select 
                v-model="formData.country" 
                filterable 
                clearable 
                placeholder="Select country"
                class="model-select">
                <el-option 
                    v-for="country in countries" 
                    :key="country.id" 
                    :label="`${country.name} (${country.country_code})`" 
                    :value="country.id" />
            </el-select>
        </el-form-item>
        <br>

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
import countries from "@/tools/gaissaroianalyzer/services/countries";
import { InfoFilled } from '@element-plus/icons-vue'

export default {
    name: "GAISSAROIAnalyzerNewForm",
    components: { InfoFilled },
    data() {
        return {
            modelArchitectures: [],
            tactics: [],
            tacticParameters: [],
            applicableMetrics: [],
            energyRelatedMetrics: [],
            countries: [],
            formData: {
                modelArchitecture: null,
                mlTactic: null,
                tacticParameter: null,
                country: null,
            },
            metricValues: {},
            energyCostRates: {},
            implementationCosts: {},
            loading: false,
            error: null,
        };
    },
    computed: {
        formIsValid() {
            const basicFormValid = this.formData.modelArchitecture && this.formData.mlTactic && this.formData.tacticParameter && this.formData.country;
            
            // Check if we have metric values for all applicable metrics
            const metricsValid = this.applicableMetrics.every(metric => 
                this.metricValues[metric.id] !== undefined && this.metricValues[metric.id] !== null && this.metricValues[metric.id] > 0);
            
            // Check if energy-related metrics are valid
            const energyMetricsValid = this.energyRelatedMetrics.every(metric => 
                this.energyCostRates[metric.id] !== undefined && this.energyCostRates[metric.id] !== null && this.energyCostRates[metric.id] > 0 &&
                this.implementationCosts[metric.id] !== undefined && this.implementationCosts[metric.id] !== null && this.implementationCosts[metric.id] > 0);
            
            return basicFormValid && metricsValid && energyMetricsValid;
        },
        hasEnergyRelatedMetrics() {
            return this.energyRelatedMetrics.length > 0;
        }
    },
    methods: {
        async fetchTactics() {
            try {
                const response = await mlTactics.list();
                if (response && response.data) {
                    this.tactics = response.data;
                }
            } catch (error) {
                console.error("Error fetching ML tactics:", error);
                this.error = "Failed to load available ML tactics. Please try again."
            }
        },
        async fetchModelArchitecturesForTactic(tacticId) {
            try {
                const response = await modelArchitectures.getCompatibleArchitecturesWithTactic(tacticId);
                if (response && response.data) {
                    this.modelArchitectures = response.data;
                }
            } catch (error) {
                console.error(`Error fetching architectures for tactic ${tacticId}:`, error);
                this.error = "Failed to load compatible model architectures. Please try again.";
            }
        },
        async fetchCountries() {
            try {
                const response = await countries.list();
                if (response && response.data) {
                    this.countries = response.data;
                }
            } catch (error) {
                console.error("Error fetching countries:", error);
                this.error = "Failed to load countries. Please try again.";
            }
        },
        async fetchTacticParameters() {
            if (!this.formData.mlTactic || !this.formData.modelArchitecture) {
                this.tacticParameters = [];
                return;
            }
            
            try {
                const filter = {
                    model_architecture: this.formData.modelArchitecture,
                };
                const response = await tacticParameters.list(this.formData.mlTactic, filter);
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
                this.energyRelatedMetrics = [];
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

                    // Initialize energy-related metrics values
                    this.energyRelatedMetrics = this.applicableMetrics.filter(metric => metric.is_energy_related);

                    this.energyRelatedMetrics.forEach(metric => {
                        if (!this.energyCostRates[metric.id]) {
                            this.energyCostRates[metric.id] = 0;
                        }
                        if (!this.implementationCosts[metric.id]) {
                            this.implementationCosts[metric.id] = 0;
                        }
                    });
                }
            } catch (error) {
                console.error(`Error fetching metrics for tactic ${this.formData.mlTactic}:`, error);
                this.error = "Failed to load applicable metrics. Please try again.";
            }
        },
        handleTacticChange() {
            // Reset model architecture selection and dependent fields
            this.formData.modelArchitecture = null;
            this.formData.tacticParameter = null;
            this.metricValues = {};
            this.energyCostRates = {};
            this.implementationCosts = {};
            this.tacticParameters = [];
            this.applicableMetrics = [];
            this.modelArchitectures = [];
            
            // Fetch architectures compatible with the selected tactic and metrics
            if (this.formData.mlTactic) {
                this.fetchModelArchitecturesForTactic(this.formData.mlTactic);
                this.fetchApplicableMetrics();
            } else {
                this.modelArchitectures = [];
            }
        },
        handleModelArchChange() {
            // Reset tactic parameter selection
            this.formData.tacticParameter = null;
            this.tacticParameters = [];
            
            // Fetch parameters for the selected tactic and architecture combination
            this.fetchTacticParameters();
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
                const metricValuesData = Object.keys(this.metricValues).map(metricId => {
                    const metric = this.applicableMetrics.find(m => m.id === parseInt(metricId));
                    const isEnergyMetric = metric && metric.is_energy_related;
                    
                    // Base metric data
                    let metricData = {
                        metric_id: parseInt(metricId),
                        baselineValue: this.metricValues[metricId]
                    };
                    
                    // Add energy-specific data if applicable
                    if (isEnergyMetric) {
                        metricData.energy_cost_rate = this.energyCostRates[metricId];
                        metricData.implementation_cost = this.implementationCosts[metricId];
                    }
                    
                    return metricData;
                });
                
                const analysisData = {
                    model_architecture_id: parseInt(this.formData.modelArchitecture),
                    tactic_parameter_option_id: parseInt(this.formData.tacticParameter),
                    metric_values_data: metricValuesData,
                    country_id: this.formData.country,
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
                        name: 'GAISSA ROI Analyzer Analysis',
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
                    this.error = "Failed to create ROI analysis. Please check your inputs are properly filled.";
                }
                window.scrollTo({top: 0});
            } finally {
                this.loading = false;
            }
        }
    },
    async mounted() {
        // Load initial data
        await this.fetchTactics();
        await this.fetchCountries();
    }
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

.info-icon {
    margin-left: 6px;
    color: var(--el-color-info);
    cursor: help;
    vertical-align: middle;
}
</style>