<template>
    <div class="roi-analysis-component" :class="{ 'force-mobile': forceMobile }" :id="containerId">
        <!-- Export button at the top right (only shown when showExportButton is true) -->
        <div v-if="showExportButton" class="export-button-container">
            <el-button type="primary" class="action-button export-button" @click="generatePDFReport"
                :loading="pdfGenerating">
                <font-awesome-icon style="margin-right: 6px" :icon="['fas', 'file-pdf']" />
                {{ $t("Generate PDF Report") }}
            </el-button>
        </div>

        <el-row :gutter="20" type="flex" justify="center" class="row-bg">
            <el-col :xs="24" :sm="24" :md="forceMobile ? 24 : 12" :lg="forceMobile ? 24 : 12" :xl="forceMobile ? 24 : 12" class="mobile-card">
                <ModelInformationCard v-if="analysisData" :modelData="analysisData" :formatDate="formatData" />
                <el-card v-else shadow="always" :body-style="{ padding: '20px' }">
                    <div class="loading-placeholder">
                        <p>{{ $t("Loading analysis data...") }}</p>
                    </div>
                </el-card>

                <!-- Source Information card for research-type analyses -->
                <SourceInformationCard v-if="isResearchAnalysis && analysisData?.source"
                    :source="analysisData.source" />

                <!-- Tactic Sources card for calculation-type analyses -->
                <TacticSourcesCard v-if="!isResearchAnalysis" :sources="tacticSources" />
            </el-col>

            <el-col :xs="24" :sm="24" :md="forceMobile ? 24 : 12" :lg="forceMobile ? 24 : 12" :xl="forceMobile ? 24 : 12" class="mobile-card">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <MetricsRadialChart v-if="metricsRadialChartData" :metricsData="metricsRadialChartData" :formatNumber="formatNumber" />
                    <div v-else class="loading-placeholder">
                        <p>{{ $t("Loading metrics data...") }}</p>
                    </div>
                </el-card>
            </el-col>

            <!-- Tactic Metric Results Card -->
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Tactic Metric Results") }}</h2>

                    <div class="view-toggle">
                        <span>{{ $t("View Mode:") }}</span>
                        <el-switch v-model="showVisualMetrics" :active-text="$t('Visual')" :inactive-text="$t('Table')"
                            class="ml-2" />
                    </div>

                    <p class="results-description">
                        {{ $t("This section provides a detailed breakdown of the metric values affected by the tactic. It illustrates specific data about the expected changes in each metric when applying the ML tactic.") }}
                    </p>

                    <!-- Table View -->
                    <div v-if="!showVisualMetrics && analysisData?.metrics_analysis?.length">
                        <el-table :data="analysisData.metrics_analysis" style="width: 100%; margin-top: 15px;">
                            <el-table-column prop="metric_name" :label="$t('Metric')" />
                            <el-table-column prop="baseline_value" :label="$t('Baseline Value')" />
                            <el-table-column prop="expected_reduction_percent" :label="$t('Reduction (%)')" />
                            <el-table-column prop="new_expected_value" :label="$t('New Expected Value')" />
                            <el-table-column prop="unit" :label="$t('Unit')" />
                        </el-table>
                    </div>

                    <!-- Visual View -->
                    <div v-if="showVisualMetrics && analysisData?.metrics_analysis?.length"
                        class="visual-metrics-container">
                        <MetricCard v-for="(metric, index) in analysisData.metrics_analysis" :key="index"
                            :metric="metric" :formatNumber="formatNumber" />
                    </div>

                    <p v-if="!analysisData?.metrics_analysis?.length && !analysisData">{{ $t("Loading tactic results...") }}</p>
                </el-card>
            </el-col>

            <!-- ROI Results Card -->
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" style="margin-top: 20px;">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("ROI Results") }}</h2>

                    <!-- Inferences Input Control -->
                    <div class="inferences-control-container">
                        <p class="inferences-control-label">{{ $t("Number of inferences:") }}</p>
                        <div class="inferences-slider-container">
                            <el-slider v-model="sliderInferenceCount" :min="10000" :max="1000000000" :step="10000"
                                @change="updateInferencesFromSlider" class="inferences-slider" />
                        </div>
                        <div class="inferences-input-container">
                            <el-input-number v-model="inferenceCount" :min="10000" :controls="false"
                                @change="updateInferences" class="inferences-input" />
                        </div>
                    </div>

                    <p class="results-description" v-if="costMetricsResults.length">
                        {{ $t(`This table provides a detailed economic analysis of the applied tactic, showing the
                        estimated cost savings and Return on Investment metrics for
                        ${costMetricsResults[0]?.num_inferences.toLocaleString('en-US')} inferences.`) }}
                    </p>

                    <div v-if="costMetricsResults.length" class="roi-cards-container">
                        <ROIDetailsCard v-for="(metric, index) in costMetricsResults" :key="index" :costMetric="metric"
                            :formatNumber="formatNumber"
                            :tacticName="analysisData?.tactic_parameter_option_details?.tactic_name"
                            :showTitle="costMetricsResults.length > 1" :columnCount="getDescriptionsColumnCount()">
                            <template v-slot:costMetricCard>
                                <MetricCard :metric="metric" :formatNumber="formatNumber" />
                            </template>
                        </ROIDetailsCard>
                    </div>

                    <!-- Emissions Reduction Section -->
                    <div v-if="emissionsData" class="emissions-section" style="margin-top: 30px;">
                        <h3 class="section-title">{{ $t("Environmental Impact") }}</h3>
                        <p class="results-description">
                            {{ $t("This section shows the environmental impact analysis, including CO₂ emissions reduction achieved by applying the ML optimization tactic.") }}
                        </p>
                        <div class="emissions-card-container">
                            <EmissionsReductionCard 
                                :emissionsData="emissionsData"
                                :numInferences="costMetricsResults[0]?.num_inferences || 0"
                                :formatNumber="formatNumber"
                                :showTitle="false"
                                :columnCount="getDescriptionsColumnCount()" />
                        </div>
                    </div>

                    <p v-if="costMetricsResults.length === 0">{{ $t("No energy-related metrics found to calculate ROI.")
                    }}</p>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="forceMobile ? 24 : 12" :lg="forceMobile ? 24 : 12" :xl="forceMobile ? 24 : 12" class="mobile-card" style="margin-top: 20px;">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <ROIEvolutionChart v-if="roiChartData" :chartData="roiChartData" :formatNumber="formatNumber" />
                    <div v-else class="loading-placeholder">
                        <p>{{ $t("Loading ROI evolution data...") }}</p>
                    </div>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="forceMobile ? 24 : 12" :lg="forceMobile ? 24 : 12" :xl="forceMobile ? 24 : 12" class="mobile-card" style="margin-top: 20px;">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <IncomeCostsChart v-if="incomeCostsChartData" :chartData="incomeCostsChartData" :formatNumber="formatNumber" />
                    <div v-else class="loading-placeholder">
                        <p>{{ $t("Loading income costs data...") }}</p>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { formatData } from "@/utils";
import roiAnalyses from "@/tools/gaissaroianalyzer/services/roiAnalyses";
import mlTactics from "@/tools/gaissaroianalyzer/services/mlTactics";

// Import components
import ModelInformationCard from './ModelInformationCard.vue';
import SourceInformationCard from './SourceInformationCard.vue';
import TacticSourcesCard from './TacticSourcesCard.vue';
import MetricsRadialChart from './MetricsRadialChart.vue';
import MetricCard from './MetricCard.vue';
import ROIDetailsCard from './ROIDetailsCard.vue';
import ROIEvolutionChart from './ROIEvolutionChart.vue';
import IncomeCostsChart from './IncomeCostsChart.vue';
import EmissionsReductionCard from './EmissionsReductionCard.vue';

export default {
    name: "ROIAnalysisComponent",
    components: {
        ModelInformationCard,
        SourceInformationCard,
        TacticSourcesCard,
        MetricsRadialChart,
        MetricCard,
        ROIDetailsCard,
        ROIEvolutionChart,
        IncomeCostsChart,
        EmissionsReductionCard
    },
    props: {
        analysisId: {
            type: [String, Number],
            required: true
        },
        showExportButton: {
            type: Boolean,
            default: true
        },
        containerId: {
            type: String,
            default: 'roi-analysis-container'
        },
        forceMobile: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            analysisData: null,
            tacticSources: [],
            showVisualMetrics: true,
            pdfGenerating: false,
            inferenceCount: 100000000
        };
    },
    computed: {
        sliderInferenceCount: {
            get() {
                const max = 1000000000;
                return Math.min(this.inferenceCount, max);
            },
            set(value) {
                this.inferenceCount = value;
            }
        },
        costMetricsResults() {
            if (!this.analysisData?.metrics_analysis) return [];

            return this.analysisData.metrics_analysis.filter(metric =>
                metric.cost_savings && !metric.cost_savings.error
            ).map(metric => {
                const costData = metric.cost_savings;
                
                // Create a metric-compatible object for cost data
                return {
                    // Original cost metric properties
                    metric_name: this.$t('Incurred Cost'),
                    description: this.$t('Total cost associated with running the model for') + ' ' + 
                        this.formatNumber(costData.num_inferences) + ' ' + this.$t('inferences.'),
                    baseline_value: parseFloat(costData.total_baseline_cost),
                    new_expected_value: parseFloat(costData.total_new_cost),
                    unit: '€',
                    expected_reduction_percent: this.calculateCostReductionPercent(
                        parseFloat(costData.total_baseline_cost),
                        parseFloat(costData.total_new_cost)
                    ),
                    higher_is_better: false,
                    
                    // Keep original cost-specific properties for ROIDetailsCard
                    total_new_cost: parseFloat(costData.total_new_cost),
                    total_baseline_cost: parseFloat(costData.total_baseline_cost),
                    baseline_cost_per_inference: parseFloat(costData.baseline_cost_per_inference),
                    new_cost_per_inference: parseFloat(costData.new_cost_per_inference),
                    implementation_cost: parseFloat(costData.implementation_cost),
                    energy_cost_rate: parseFloat(costData.energy_cost_rate || 0),
                    total_savings: parseFloat(costData.total_savings),
                    break_even_inferences: costData.break_even_inferences === 'Infinity' ?
                        costData.break_even_inferences : parseInt(costData.break_even_inferences).toLocaleString(),
                    roi_percentage: parseFloat(costData.roi) * 100,
                    infinite_roi_percentage: parseFloat(costData.infinite_roi) * 100,
                    num_inferences: costData.num_inferences,
                    
                    // Include emissions data if available
                    inferences_carbon_emissions: costData.inferences_carbon_emissions || null
                };
            });
        },
        isResearchAnalysis() {
            return this.analysisData?.analysis_type === 'research';
        },
        incomeCostsChartData() {
            if (!this.costMetricsResults || this.costMetricsResults.length === 0) {
                return null;
            }

            // Use the first metric for the chart
            const metric = this.costMetricsResults[0];

            const optimizationCost = metric.implementation_cost;
            const newCostPerInference = metric.new_cost_per_inference;
            const oldCostPerInference = metric.baseline_cost_per_inference;

            // Parse break-even point, handling "Infinity" string and number formatting
            let breakEvenPoint = metric.break_even_inferences;
            if (typeof breakEvenPoint === 'string') {
                if (breakEvenPoint === 'Infinity') {
                    breakEvenPoint = Infinity;
                } else {
                    // Remove commas and other formatting from the string
                    breakEvenPoint = parseInt(breakEvenPoint.replace(/[^\d]/g, ''));
                }
            }

            // Handle cases where breakEvenPoint is zero, NEGATIVE or INFINITE
            if (!isFinite(breakEvenPoint) || breakEvenPoint <= 0) {
                const maxInferences = 2000000;
                const maxCost = (maxInferences * newCostPerInference) + optimizationCost;
                const income = (maxInferences * oldCostPerInference);

                const incomeData = [[0, 0], [maxInferences, income]];
                const costsData = [[0, optimizationCost], [maxInferences, maxCost]];

                return {
                    incomeData,
                    costsData,
                    maxInferences,
                    breakEvenType: (breakEvenPoint === 0) ? 'zero' : 'infinity',
                };
            }

            // Chart points when breakEvenPoint is POSITIVE 
            const maxInferences = breakEvenPoint * 2; // Extend the chart beyond the Break-Even Point in a defined range
            const maxCost = (maxInferences * newCostPerInference) + optimizationCost;

            const incomeData = [[0, 0], [maxInferences, (maxInferences * oldCostPerInference)]];
            const costsData = [[0, optimizationCost], [maxInferences, maxCost]];

            return {
                incomeData,
                costsData,
                maxInferences,
                breakEvenType: 'normal',
            };
        },
        roiChartData() {
            if (!this.analysisData?.metrics_analysis) {
                return null;
            }

            // Find the first energy metric with ROI evolution data
            const metricWithROIData = this.analysisData.metrics_analysis.find(metric =>
                metric.roi_evolution_chart_data && metric.roi_evolution_chart_data.length > 0
            );

            if (!metricWithROIData) {
                console.warn('No ROI evolution chart data found in metrics analysis');
                return null;
            }

            const roiEvolutionData = metricWithROIData.roi_evolution_chart_data.map(item =>
                [item.inferences, item.roi]
            );

            let maxInferences = 0;
            if (roiEvolutionData.length > 0) {
                maxInferences = Math.max(...roiEvolutionData.map(point => point[0]));
            }

            return {
                roiEvolutionData,
                maxInferences
            };
        },
        metricsRadialChartData() {
            if (!this.analysisData?.metrics_analysis || this.analysisData.metrics_analysis.length === 0) {
                return null;
            }

            const metrics = this.analysisData.metrics_analysis;
            const hasIncurredCost = this.costMetricsResults && this.costMetricsResults.length > 0;

            // Create indicators from metrics (slightly higher than the highest value)
            const indicators = metrics.map(metric => {
                const maxValue = Math.max(
                    parseFloat(metric.baseline_value) || 0,
                    parseFloat(metric.new_expected_value) || 0
                ) * 1.2;

                const displayName = metric.unit ?
                    `${metric.metric_name} (${metric.unit})` :
                    metric.metric_name;

                return {
                    name: displayName,
                    max: maxValue
                };
            });

            // Add incurred cost (of the first cost metric) indicator if exists
            if (hasIncurredCost) {
                const costMetric = this.costMetricsResults[0];
                const maxIncurredCost = Math.max(
                    parseFloat(costMetric.total_baseline_cost) || 0,
                    parseFloat(costMetric.total_new_cost) || 0
                ) * 1.2;

                indicators.push({
                    name: 'Incurred Cost (€)',
                    max: maxIncurredCost
                });
            }

            // Create data series
            const baselineValues = metrics.map(metric => parseFloat(metric.baseline_value) || 0);
            const newValues = metrics.map(metric => parseFloat(metric.new_expected_value) || 0);

            // Add incurred cost values if they exist
            if (hasIncurredCost) {
                const costMetric = this.costMetricsResults[0];
                baselineValues.push(parseFloat(costMetric.total_baseline_cost) || 0);
                newValues.push(parseFloat(costMetric.total_new_cost) || 0);
            }

            return {
                indicators,
                seriesData: [
                    {
                        value: baselineValues,
                        name: 'Baseline',
                        itemStyle: {
                            color: 'orange'
                        }
                    },
                    {
                        value: newValues,
                        name: 'Optimized',
                        itemStyle: {
                            color: 'green'
                        }
                    }
                ],
                legendData: ['Baseline', 'Optimized']
            };
        },
        emissionsData() {
            // Extract emissions data from the first cost metrics result that has emissions data
            if (!this.costMetricsResults || this.costMetricsResults.length === 0) {
                return null;
            }

            const metricWithEmissions = this.costMetricsResults.find(metric => 
                metric.inferences_carbon_emissions && 
                !metric.inferences_carbon_emissions.error
            );

            if (!metricWithEmissions) {
                return null;
            }

            return metricWithEmissions.inferences_carbon_emissions;
        },
    },
    watch: {
        analysisId: {
            immediate: true,
            handler(newId) {
                if (newId) {
                    this.loadAnalysisData();
                }
            }
        }
    },
    methods: {
        formatData,
        calculateCostReductionPercent(baselineCost, newCost) {
            // Handle cases where baseline cost is zero or non-numeric
            if (isNaN(baselineCost) || isNaN(newCost)) return 0;
            if (baselineCost === 0) {
                return -Infinity;
            }

            const reduction = baselineCost - newCost;
            const percentage = (reduction / baselineCost) * 100;

            return percentage.toFixed(2);
        },
        async updateInferencesFromSlider(value) {
            // We need to treat the slider value separately to allow a greater range for the input container
            this.inferenceCount = value;
            await this.updateInferences();
        },
        async updateInferences() {
            // Ensure inferenceCount is at least 10000
            if (this.inferenceCount < 10000) {
                this.inferenceCount = 10000;
            }

            try {
                // Re-fetch the analysis with the new inference count
                if (!this.analysisId) return;

                const data = await roiAnalyses.getAnalysis(this.analysisId, { num_inferences: this.inferenceCount });
                if (data) {
                    this.analysisData = data;
                }
            } catch (error) {
                console.error('Error updating inferences count:', error);
                ElMessage({
                    message: this.$t('Failed to update with new inference count.'),
                    type: 'error',
                    duration: 3000
                });
            }
        },
        formatNumber(value) {
            if (value === null || value === undefined || isNaN(value)) {
                return 'N/A';
            }

            // Scientific notation for very small values
            if (Math.abs(value) < 0.00001 && value !== 0) {
                return value.toExponential(4);
            }

            if (Math.abs(value) >= 1000000000) {
                return (value / 1000000000).toLocaleString('en-US', { maximumFractionDigits: 1 }) + 'B';
            } else if (Math.abs(value) >= 1000000) {
                return (value / 1000000).toLocaleString('en-US', { maximumFractionDigits: 1 }) + 'M';
            } else if (Math.abs(value) >= 1000) {
                return (value / 1000).toLocaleString('en-US', { maximumFractionDigits: 1 }) + 'K';
            } else if (Math.abs(value) >= 1) {
                return value.toLocaleString('en-US', { maximumFractionDigits: 2 });
            } else if (Math.abs(value) >= 0.01) {
                return value.toLocaleString('en-US', { maximumFractionDigits: 4 });
            } else {
                return value.toLocaleString('en-US', { maximumFractionDigits: 6 });
            }
        },
        getDescriptionsColumnCount() {
            return window.innerWidth < 992 ? 1 : 2;
        },
        async loadAnalysisData() {
            try {
                if (!this.analysisId) return;

                // Include inference count in the request
                const data = await roiAnalyses.getAnalysis(this.analysisId, { num_inferences: this.inferenceCount });
                if (data) {
                    this.analysisData = data;

                    // For calculation-type analyses, fetch the sources for the tactic
                    if (!this.isResearchAnalysis) {
                        try {
                            const tacticId = this.analysisData.tactic_parameter_option_details?.tactic;
                            if (tacticId) {
                                const resultTactic = await mlTactics.getById(tacticId);
                                this.tacticSources = resultTactic?.sources || [];
                            } else {
                                this.tacticSources = [];
                            }
                        } catch (tacticError) {
                            console.error("Error loading tactic sources:", tacticError);
                            this.tacticSources = [];
                        }
                    }
                }
            } catch (error) {
                console.error("Error loading analysis data:", error);
                ElMessage({
                    message: this.$t('Failed to load ROI analysis data. Please try again.'),
                    type: 'error',
                    duration: 3000
                });
            }
        },
        async generatePDFReport() {
            this.pdfGenerating = true;

            try {
                // Give charts time to fully render before capturing
                await new Promise(resolve => setTimeout(resolve, 500));

                // Dynamically import PDF service only when needed
                const { default: pdfReportService } = await import("@/tools/gaissaroianalyzer/services/pdfReportService");

                // Generate file name based on analysis data
                const fileName = `roi-analysis-${this.analysisData.id}-${this.analysisData.model_architecture_name}-${this.analysisData.tactic_parameter_option_details.tactic_name}.pdf`.replace(/\s+/g, '-').toLowerCase();

                // Generate the PDF
                const result = await pdfReportService.generatePDFReport(
                    this.analysisData,
                    this.containerId,
                    fileName
                );

                if (result) {
                    ElMessage({
                        message: this.$t('PDF report generated successfully!'),
                        type: 'success',
                        duration: 5000,
                        showClose: true
                    });
                } else {
                    throw new Error('PDF generation failed');
                }
            } catch (error) {
                console.error("Error generating PDF report:", error);
                ElMessage({
                    message: this.$t('Failed to generate PDF report. Please try again.'),
                    type: 'error',
                    duration: 5000,
                    showClose: true
                });
            } finally {
                this.pdfGenerating = false;
            }
        }
    }
};
</script>

<style scoped>
.roi-analysis-component {
    padding: 20px;
}

.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin-bottom: 20px;
}

.results-description {
    margin-bottom: 10px;
}

.mobile-card {
    margin-bottom: 20px;
}

.el-button {
    background-color: var(--gaissa_green);
    color: white;
    border-color: var(--gaissa_green);
}

.inferences-control-container {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 12px;
    background-color: #f9f9f9;
    border-radius: 8px;
    border: 1px solid #eee;
}

.inferences-control-label {
    font-weight: bold;
    margin-right: 12px;
    min-width: 150px;
    margin-bottom: 0;
}

.inferences-slider-container {
    flex-grow: 1;
    margin-right: 20px;
}

.inferences-input-container {
    width: 150px;
}

.roi-cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.emissions-section {
    border-top: 1px solid #eee;
    padding-top: 20px;
}

.emissions-card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.view-toggle {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    justify-content: flex-end;
}

.visual-metrics-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
    margin-top: 20px;
}

.export-button-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
}

.action-button {
    display: flex;
    align-items: center;
    gap: 8px;
}

@media (max-width: 1320px) {
    .visual-metrics-container {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 992px) {
    .inferences-control-container {
        flex-direction: column;
        align-items: stretch;
    }

    .inferences-control-label {
        margin-bottom: 10px;
    }

    .inferences-slider-container {
        margin-right: 0;
        margin-bottom: 10px;
    }

    .inferences-input-container {
        width: 100%;
    }
}

/* Force mobile layout styles - apply mobile layout regardless of screen size */
.roi-analysis-component.force-mobile .visual-metrics-container {
    grid-template-columns: 1fr;
}

.roi-analysis-component.force-mobile .inferences-control-container {
    flex-direction: column;
    align-items: stretch;
}

.roi-analysis-component.force-mobile .inferences-control-label {
    margin-bottom: 10px;
}

.roi-analysis-component.force-mobile .inferences-slider-container {
    margin-right: 0;
    margin-bottom: 10px;
}

.roi-analysis-component.force-mobile .inferences-input-container {
    width: 100%;
}

.loading-placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 200px;
    color: #666;
    font-style: italic;
}
</style>
