<template>
    <!-- Collapsible card - starts collapsed -->
    <el-collapse v-model="activeCollapse" class="analysis-swapper-collapse" v-if="availableParameters.length > 1">
        <el-collapse-item name="swapper">
            <!-- Custom header with icon and title -->
            <template #title>
                <div class="collapse-header">
                    <font-awesome-icon :icon="['fas', 'right-left']" class="header-icon" />
                    <span class="header-text">{{ $t("Switch Analysis Configuration") }}</span>
                </div>
            </template>

            <!-- Swapper content when expanded -->
            <div v-if="error">
                <el-alert :title="error" type="error" :closable="false" />
            </div>

            <div v-else class="swapper-content">
                <!-- Switch Parameter -->
                <div v-if="availableParameters.length > 1" class="swap-row">
                    <label>{{ $t("Parameter:") }}</label>
                    <el-select 
                        v-model="selectedParameter" 
                        @change="switchToParameter"
                        :placeholder="$t('Select different parameter')">
                        <el-option 
                            v-for="param in availableParameters" 
                            :key="param.id" 
                            :label="`${param.name}: ${param.value}`"
                            :value="param.id"
                            :disabled="param.id === currentAnalysis?.tactic_parameter_option" />
                    </el-select>
                </div>

                <!-- Select specific analysis if multiple found -->
                <div v-if="availableAnalyses.length > 1" class="swap-row">
                    <label>{{ $t("Analysis:") }}</label>
                    <el-select 
                        v-model="selectedAnalysisId" 
                        @change="switchToAnalysis"
                        :placeholder="$t('Select analysis')">
                        <el-option 
                            v-for="analysis in availableAnalyses" 
                            :key="analysis.id" 
                            :label="formatAnalysisLabel(analysis)"
                            :value="analysis.id"
                            :disabled="analysis.id === currentAnalysis?.id" />
                    </el-select>
                </div>

                <!-- No alternatives -->
                <div v-if="availableParameters.length <= 1" class="no-alternatives">
                    <p>{{ $t("No alternative parameters available for this configuration") }}</p>
                </div>
            </div>
        </el-collapse-item>
    </el-collapse>
</template>

<script>
import roiAnalyses from "@/tools/gaissaroianalyzer/services/roiAnalyses";
import tacticParameters from "@/tools/gaissaroianalyzer/services/tacticParameters";

export default {
    name: "AnalysisSwapper",
    props: {
        // The current analysis data object passed from parent
        currentAnalysis: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            activeCollapse: [],         // Controls which collapse panel is open ([] = closed, ['swapper'] = open)
            error: null,                // Error message if something goes wrong
            availableParameters: [],    // List of alternative parameters for same tactic/architecture
            selectedParameter: null,    // Currently selected parameter ID
            availableAnalyses: [],      // List of analyses for the selected parameter
            selectedAnalysisId: null    // Currently selected analysis ID
        };
    },
    computed: {
        // What analysis type are we in (calculation or research)
        analysisType() {
            return this.currentAnalysis?.analysis_type;
        }
    },
    watch: {
        // When currentAnalysis changes, reload the alternatives
        currentAnalysis: {
            immediate: true,    // Run on component creation
            handler() {
                if (this.currentAnalysis) {
                    // Reset state when analysis changes
                    this.selectedParameter = null;
                    this.selectedAnalysisId = null;
                    this.availableAnalyses = [];
                    this.error = null;
                    // Load new parameters
                    this.loadParameters();
                }
            }
        }
    },
    methods: {
        // Fetch available parameters for the current tactic and architecture
        async loadParameters() {
            this.error = null;

            try {
                const tacticId = this.currentAnalysis.tactic_parameter_option_details?.tactic;
                const architectureId = this.currentAnalysis.model_architecture;
                
                if (!tacticId || !architectureId) {
                    this.availableParameters = [];
                    return;
                }

                // API filter object
                const filter = {
                    model_architecture: architectureId,
                    analysis_type: this.analysisType
                };

                // Call API to get parameters
                const response = await tacticParameters.list(tacticId, filter);
                
                if (response && response.data) {
                    this.availableParameters = response.data;
                } else {
                    this.availableParameters = [];
                }
            } catch (err) {
                console.error("Error loading parameters:", err);
                this.error = this.$t("Failed to load alternatives");
                this.availableParameters = [];
            }
        },
        
        // When user selects a different parameter, find analyses with that parameter
        async switchToParameter() {
            if (!this.selectedParameter) return;

            try {
                // Find analyses with selected parameter
                const params = {
                    model_architecture: this.currentAnalysis.model_architecture,
                    tactic_parameter_option: this.selectedParameter,
                    analysis_type: this.analysisType
                };

                const response = await roiAnalyses.list(params);
                
                if (response && response.data && response.data.length > 0) {
                    this.availableAnalyses = response.data;
                    
                    // If only one analysis, navigate directly
                    if (response.data.length === 1) {
                        this.$emit('analysisChanged', response.data[0].id);
                    } else {
                        // Multiple analyses found, user needs to select one
                        this.selectedAnalysisId = null;
                    }
                } else {
                    this.availableAnalyses = [];
                    this.$message.warning(this.$t('No analysis found for this parameter'));
                }
            } catch (err) {
                console.error("Error switching parameter:", err);
                this.$message.error(this.$t('Failed to switch configuration'));
                this.availableAnalyses = [];
            }
        },
        
        // When user selects a specific analysis from multiple options
        switchToAnalysis() {
            if (!this.selectedAnalysisId) return;
            this.$emit('analysisChanged', this.selectedAnalysisId);
        },
        
        // Format analysis label to help user distinguish between multiple analyses
        formatAnalysisLabel(analysis) {
            // Show date if it's a calculation analysis
            if (analysis.dateRegistration) {
                const date = new Date(analysis.dateRegistration);
                return `${this.$t("Analysis")} - ${date.toLocaleDateString()}`;
            }
            // Show source name if it's a research analysis
            if (analysis.source_name) {
                return `${analysis.source_name}`;
            }
            // Fallback to ID
            return `${this.$t("Analysis")} #${analysis.id}`;
        }
    }
};
</script>

<style scoped>
/* Use Element Plus collapse, no custom border needed */
.analysis-swapper-collapse {
    margin-top: 20px;
}

/* Custom header styling */
.collapse-header {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
}

.header-icon {
    color: var(--gaissa_green);
    font-size: 1.1rem;
    margin-right: 5px;
}

.header-text {
    font-weight: 600;
    color: #333;
    font-size: 1rem;
}

.alternative-badge {
    margin-left: 10px;
    display: flex;
}

/* Content when expanded */
.swapper-content {
    padding: 10px 0;
}

/* Each swap row */
.swap-row {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px 0;
}

.swap-row label {
    min-width: 100px;
    font-weight: 500;
    color: #555;
}

.swap-row .el-select {
    flex: 1;
    max-width: 400px;
}

/* No alternatives message */
.no-alternatives {
    padding: 10px 0;
    color: #999;
    font-style: italic;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .swap-row {
        flex-direction: column;
        align-items: stretch;
    }

    .swap-row label {
        min-width: unset;
    }

    .swap-row .el-select {
        max-width: 100%;
    }
}
</style>
