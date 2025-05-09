<template>
    <div class="gaissa-roi-analyzer" id="roi-analysis-container">
        <h1>{{ $t("GAISSA ROI Analyzer") }}</h1>
        
        <!-- Export button at the top right -->
        <div class="export-button-container">
            <el-button 
                type="primary" 
                class="action-button export-button" 
                @click="generatePDFReport" 
                :loading="pdfGenerating">
                <font-awesome-icon style="margin-right: 6px" :icon="['fas', 'file-pdf']" />
                {{ $t("Generate PDF Report") }}
            </el-button>
        </div>

        <el-row :gutter="20" type="flex" :justify="center" class="row-bg">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Model Information") }}</h2>
                    <el-descriptions v-if="analysisData" :column="1" border>
                        <el-descriptions-item :label="$t('Model architecture')">
                            {{ analysisData.model_architecture_name }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('ML Tactic')">
                            {{ analysisData.tactic_parameter_option_details?.tactic_name }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Tactic parameter')">
                            {{ analysisData.tactic_parameter_option_details?.name }}: {{ analysisData.tactic_parameter_option_details?.value }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Analysis identifier')">
                            {{ analysisData.id }}
                        </el-descriptions-item>
                        <el-descriptions-item v-if="analysisData.dateRegistration" :label="$t('Analysis registration date')">
                            {{ formatData(analysisData.dateRegistration) }}
                        </el-descriptions-item>
                        <el-descriptions-item v-if="analysisData.country" :label="$t('Country deploy')">
                            {{ analysisData.country }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Analysis type')">
                            {{ isResearchAnalysis ? $t('Research') : $t('Calculation') }}
                        </el-descriptions-item>
                    </el-descriptions>
                    <p v-else>{{ $t("Loading model information...") }}</p>
                </el-card>
                
                <!-- Source Information card -->
                <el-card v-if="isResearchAnalysis && analysisData?.source" 
                         shadow="always" 
                         :body-style="{ padding: '20px' }" 
                         style="margin-top: 20px;">
                    <h2 class="section-title">{{ $t("Source Information") }}</h2>
                    <el-descriptions :column="1" border>
                        <el-descriptions-item :label="$t('Title')">
                            {{ analysisData.source.title }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('URL')">
                            <a :href="analysisData.source.url" target="_blank" rel="noopener noreferrer">
                                {{ analysisData.source.url }}
                            </a>
                        </el-descriptions-item>
                    </el-descriptions>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Metrics Chart") }}</h2>
                    <p class="chart-description">
                        {{ $t("This chart illustrates the expected effect of the tactic over a set of the metrics.") }}
                    </p>
                    <div ref="metricsRadialChartContainer" class="chart-container">
                        <!-- Chart will be rendered here -->
                    </div>
                    <p>
                        The chart displays the baseline and new expected values for each metric, allowing the visualization of the impact of the tactic.
                    </p>
                </el-card>
            </el-col>

            <!-- Tactic Metric Results Card -->
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Tactic Metric Results") }}</h2>
                    
                    <div class="view-toggle">
                        <span>{{ $t("View Mode:") }}</span>
                        <el-switch
                            v-model="showVisualMetrics"
                            :active-text="$t('Visual')"
                            :inactive-text="$t('Table')"
                            class="ml-2"
                        />
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
                    <div v-if="showVisualMetrics && analysisData?.metrics_analysis?.length" class="visual-metrics-container">
                        <div v-for="(metric, index) in analysisData.metrics_analysis" :key="index" class="metric-card">

                            <!-- Percentage Change -->
                            <div class="change-indicator">
                                <div class="arrow-container">
                                    <font-awesome-icon v-if="parseFloat(metric.expected_reduction_percent) > 0" :icon="['fas', 'down-long']" 
                                        :class="['change-arrow', isReductionPositive(metric) ? 'positive' : 'negative']"/>
                                    <font-awesome-icon v-else-if="calculateCostReductionPercent(metric) == 0" :icon="['fas', 'equals']" 
                                        class="change-arrow positive"/>
                                    <font-awesome-icon v-else :icon="['fas', 'up-long']" 
                                        :class="['change-arrow', isReductionPositive(metric) ? 'positive' : 'negative']"/>                                     
                                </div>
                                <div :class="['change-percentage', isReductionPositive(metric) ? 'positive' : 'negative']">
                                    {{ this.formatNumber(Math.abs(parseFloat(metric.expected_reduction_percent).toFixed(2))) }}%
                                </div>
                            </div>

                            <div class="metric-data">
                                <!-- Metric Title and Description -->
                                 <div class="metric-info">                                   
                                    <h3 class="metric-title">{{ metric.metric_name }}</h3>
                                    <p class="metric-description">{{ metric.description }}</p>
                                </div>
                                <!-- Metric Comparison Area -->
                                <div class="metric-comparison">                            
                                    <!-- Values Comparison (Right) -->
                                    <div class="values-comparison">
                                        <!-- Optimized Value -->
                                        <div class="value-container optimized">
                                            <div class="value-label">{{ $t("Optimized") }}</div>
                                            <div :class="['value', isReductionPositive(metric) ? 'positive' : 'negative']">
                                                {{ formatNumber(metric.new_expected_value) }} <span class="unit">{{ metric.unit }}</span>
                                            </div>
                                        </div>
                                        
                                        <!-- Non-Optimized Value -->
                                        <div class="value-container baseline">
                                            <div class="value-label">{{ $t("Non-optimized") }}</div>
                                            <div class="value">
                                                {{ formatNumber(metric.baseline_value) }} <span class="unit">{{ metric.unit }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <p v-if="!analysisData?.metrics_analysis?.length && !analysisData">{{ $t("Loading tactic results...") }}</p>
                </el-card>
            </el-col>

            <!-- ROI Results Card -->
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" style="margin-top: 20px;">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("ROI Results") }}</h2>
                    <p class="results-description">
                        {{ $t(`This table provides a detailed economic analysis of the applied tactic, showing the estimated cost savings and Return on Investment metrics for ${costMetricsResults[0]?.num_inferences.toLocaleString()} inferences.`) }}
                    </p>
                    
                    <div v-if="costMetricsResults.length" class="roi-cards-container">
                        <div v-for="(metric, index) in costMetricsResults" :key="index" class="roi-card">
                            <h3 v-if="costMetricsResults.length > 1">{{ metric.metric_name }}</h3>
                            <el-descriptions :column="getDescriptionsColumnCount()" border>
                                <el-descriptions-item :label="$t('Incurred Cost (€)')">
                                    {{ formatNumber(metric.total_new_cost) }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('Non-optimized Incurred Cost (€)')">
                                    {{ formatNumber(metric.total_baseline_cost) }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('Inference Cost (€)')">
                                    {{ formatNumber(metric.new_cost_per_inference) }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('Non-optimized Inference Cost (€)')">
                                    {{ formatNumber(metric.baseline_cost_per_inference) }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('Implementation Cost (€)')">
                                    {{ formatNumber(metric.implementation_cost) }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('Energy Cost (€/kWh)')">
                                    {{ formatNumber(metric.energy_cost_rate) }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('Cost Savings (€)')">
                                    {{ formatNumber(metric.total_savings) }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('Break-Even Point (inferences)')">
                                    {{ metric.break_even_inferences }}
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t(`ROI (for ${metric.num_inferences.toLocaleString()} inferences)`)">
                                    {{ formatNumber(metric.roi_percentage) }}%
                                </el-descriptions-item>
                                <el-descriptions-item :label="$t('ROI (for infinite inferences)')">
                                    {{ formatNumber(metric.infinite_roi_percentage) }}%
                                </el-descriptions-item>
                            </el-descriptions>
                            
                            <!-- Recommendation based on Break-Even Point -->
                            <div class="recommendation-container" v-if="analysisData">
                                <font-awesome-icon v-if="metric.break_even_inferences !== 'Infinity'" :icon="['fas', 'lightbulb']" class="recommendation-icon positive"/>
                                <font-awesome-icon v-else :icon="['fas', 'lightbulb']" class="recommendation-icon negative"/>
                                <div v-if="metric.break_even_inferences !== 'Infinity'" class="recommendation positive">
                                    <strong>We recommend you to apply the tactic {{ analysisData.tactic_parameter_option_details?.tactic_name }}</strong> 
                                    if you expect to perform an amount of inferences higher than {{ metric.break_even_inferences }}.
                                </div>
                                <div v-else class="recommendation negative">
                                    We encourage you to consider a different ML tactic as this one does not provide a positive return on investment.
                                </div>
                            </div>

                            <!-- Incurred Cost Metric Card -->
                            <div class="metric-card">
                                <!-- Percentage Change -->
                                <div class="change-indicator">
                                    <div class="arrow-container">
                                        <font-awesome-icon v-if="calculateCostReductionPercent(metric) > 0" :icon="['fas', 'down-long']" class="change-arrow positive"/>
                                        <font-awesome-icon v-else-if="calculateCostReductionPercent(metric) == 0" :icon="['fas', 'equals']" class="change-arrow positive"/>
                                        <font-awesome-icon v-else :icon="['fas', 'up-long']" class="change-arrow negative"/>
                                    </div>
                                    <div :class="['change-percentage', calculateCostReductionPercent(metric) >= 0 ? 'positive' : 'negative']">
                                        {{ formatNumber(Math.abs(calculateCostReductionPercent(metric))) }}%
                                    </div>
                                </div>

                                <div class="metric-data">
                                    <!-- Metric Title and Description -->
                                    <div class="metric-info">
                                        <h3 class="metric-title">{{ $t('Incurred Cost') }}</h3>
                                        <p class="metric-description">{{ $t('Total cost associated with running the model for') }} {{ this.formatNumber(metric.num_inferences) }} {{ $t('inferences.') }}</p>
                                    </div>
                                    <!-- Metric Comparison Area -->
                                    <div class="metric-comparison">
                                        <div class="values-comparison">
                                            <!-- Optimized Value -->
                                            <div class="value-container optimized">
                                                <div class="value-label">{{ $t("Optimized") }}</div>
                                                <div :class="['value', calculateCostReductionPercent(metric) >= 0 ? 'positive' : 'negative']">
                                                    {{ formatNumber(metric.total_new_cost) }} <span class="unit">€</span>
                                                </div>
                                            </div>
                                            <!-- Non-Optimized Value -->
                                            <div class="value-container baseline">
                                                <div class="value-label">{{ $t("Non-optimized") }}</div>
                                                <div class="value">
                                                    {{ formatNumber(metric.total_baseline_cost) }} <span class="unit">€</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <p v-if="costMetricsResults.length === 0">{{ $t("No energy-related metrics found to calculate ROI.") }}</p>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card" style="margin-top: 20px;">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("ROI Evolution Chart") }}</h2>
                    <p class="chart-description">
                        {{ $t("This chart illustrates the evolution of the Return on Investment (ROI) of the specified technique over a range of inferences.") }}
                    </p>
                    <div ref="roiChartContainer" class="chart-container">
                        <!-- Chart will be rendered here -->
                    </div>
                    <p>
                        The ROI Evolution Chart shows the evolution of the Return on Investment (ROI) over a range of inferences. A positive ROI indicates that you've saved more money than you've spent on optimization and inferences. A negative ROI means you've spent more than you've saved. For example, a positive ROI of 0.5 means that for every €1 you've spent, you've earned/saved €0.5.
                    </p>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card" style="margin-top: 20px;">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Income/Costs Chart") }}</h2>
                    <p class="chart-description">
                        {{ $t("This chart illustrates the evolution of income and costs over a range of inferences for the specified technique.") }}
                    </p>
                    <p>
                        <strong>Income:</strong> how much money you would spend on inferences if you didn't optimize your model.<br>
                        <strong>Costs:</strong> total expenses, which include the initial optimization cost plus the new cost per inference.
                    </p>
                    <div ref="incomeCostsChartContainer" class="chart-container">
                        <!-- Chart will be rendered here -->
                    </div>
                    <p>
                        <strong>ROI &lt; 0:</strong> When the "Costs" line is above the "Income" line, your ROI is negative. This means you've spent more on optimization and inferences than you would have if you hadn't optimized your model.
                        <br>
                        <strong>ROI = 0 (Break-Even Point):</strong> The point where the "Costs" line and "Income" line intersect is the Break-Even point. At this point, your total savings equal your total costs.
                        <br>
                        <strong>ROI &gt; 0:</strong> When the "Income" line is above the "Costs" line, your ROI is positive. This means you've spent less than you would have if you hadn't optimized your model. This means you are saving money.
                    </p>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { formatData } from "@/utils";
import * as echarts from 'echarts';
import roiAnalyses from "@/tools/gaissaroianalyzer/services/roiAnalyses";
import pdfReportService from "@/tools/gaissaroianalyzer/services/pdfReportService";
import { ElMessage } from 'element-plus';
import 'element-plus/es/components/message/style/css';

export default {
    name: "GAISSAROIAnalyzer",
    data() {
        return {
            analysisData: null,
            metricsRadialChart: null,
            incomeCostsChart: null,
            roiChart: null,
            showVisualMetrics: true,
            pdfGenerating: false,
            metricsRadialChartOptions: {
                legend: {
                    bottom: 0,
                    itemGap: 20,
                    data: []
                },
                radar: {
                    indicator: []
                },
                label: {
                    show: true,
                    formatter: function (params) {
                        return typeof params.value === 'number' ? 
                            this.formatNumber(params.value) : params.value;
                    }.bind(this)
                },
                series: [
                    {
                        type: 'radar',
                        data: []
                    }
                ]
            },
            incomeCostsChartOptions: {
                xAxis: {
                    type: 'value',
                    name: this.$t('Number of Inferences'),
                    nameLocation: 'middle',
                    nameGap: 30,
                    min: 0,
                    axisLabel: {
                        formatter: function(value) {
                            return this.formatNumber(value);
                        }.bind(this)
                    }
                },
                yAxis: {
                    type: 'value',
                    name: this.$t('Amount (€)'),
                    nameLocation: 'middle',
                    nameGap: 35,
                    axisLabel: {
                        formatter: function(value) {
                            return this.formatNumber(value);
                        }.bind(this)
                    }
                },
                series: [
                    {
                        name: this.$t('Income'),
                        type: 'line',
                        data: [],
                        itemStyle: {
                            color: 'green'
                        },
                        lineStyle: {
                            type: 'dashed',
                            color: 'green',
                        },
                        areaStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                {
                                    offset: 0,
                                    color: 'rgba(0, 255, 0, 0.2)' // Light green at top
                                },
                                {
                                    offset: 1,
                                    color: 'rgba(0, 255, 0, 0)' // Transparent at bottom
                                }
                            ])
                        }
                    },
                    {
                        name: this.$t('Costs'),
                        type: 'line',
                        data: [],
                        itemStyle: {
                            color: 'red'
                        },
                        lineStyle: {
                            color: 'red',
                        },
                        areaStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                {
                                    offset: 0,
                                    color: 'rgba(255, 0, 0, 0.2)' // Light red at top
                                },
                                {
                                    offset: 1,
                                    color: 'rgba(255, 0, 0, 0.05)' // Transparent at bottom
                                }
                            ])
                        }
                    }
                ],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    },
                },
                legend: {
                    data: [this.$t('Income'), this.$t('Costs')],
                    bottom: 0,
                }
            },
            roiChartOptions: {
                xAxis: {
                    type: 'value',
                    name: this.$t('Number of Inferences'),
                    nameLocation: 'middle',
                    nameGap: 30,
                    axisLabel: {
                        formatter: function(value) {
                            return this.formatNumber(value);
                        }.bind(this)
                    }
                },
                yAxis: {
                    type: 'value',
                    name: this.$t('ROI'),
                    nameLocation: 'middle',
                    nameGap: 35,
                    axisLabel: {
                        formatter: function(value) {
                            return this.formatNumber(value);
                        }.bind(this)
                    }
                },
                series: [
                    {
                        name: this.$t('ROI Evolution'),
                        type: 'line',
                        smooth: true,
                        showSymbol: false,
                        data: [],
                        itemStyle: {
                            color: 'rgb(0, 71, 171)',
                        },
                        lineStyle: {
                            color: 'rgb(0, 71, 171)',
                        },
                    }
                ],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    },
                },
                legend: {
                    data: [this.$t('ROI Evolution')],
                    bottom: 0,
                }
            }
        };
    },
    computed: {
        costMetricsResults() {
            if (!this.analysisData?.metrics_analysis) return [];
            
            return this.analysisData.metrics_analysis.filter(metric => 
                metric.cost_savings && !metric.cost_savings.error
            ).map(metric => {
                const costData = metric.cost_savings;

                return {
                    metric_name: metric.metric_name,
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
                    num_inferences: costData.num_inferences
                };
            });
        },
        isResearchAnalysis() {
            return this.analysisData?.source !== null && this.analysisData?.source !== undefined;
        }
    },
    methods: {
        formatData,
        calculateCostReductionPercent(costMetric) {
            // Handle cases where baseline cost is zero or non-numeric
            const baselineCost = parseFloat(costMetric.total_baseline_cost);
            const newCost = parseFloat(costMetric.total_new_cost);

            if (isNaN(baselineCost) || isNaN(newCost)) return 0;
            if (baselineCost === 0) {
                return -Infinity;
            }

            const reduction = baselineCost - newCost;
            const percentage = (reduction / baselineCost) * 100;
            
            return parseFloat(percentage.toFixed(2));
        },
        formatNumber(value) {
            if (value === null || value === undefined || isNaN(value)) {
                return 'N/A';
            }
            
            // Scientific notation for very small values
            if (Math.abs(value) < 0.00001 && value !== 0) {
                return value.toExponential(4);
            } 
            
            if (Math.abs(value) >= 1000000) {
                return (value / 1000000).toLocaleString(undefined, { maximumFractionDigits: 1 }) + 'M';
            } else if (Math.abs(value) >= 1000) {
                return (value / 1000).toLocaleString(undefined, { maximumFractionDigits: 1 }) + 'K';
            } else if (Math.abs(value) >= 1) {
                return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
            } else if (Math.abs(value) >= 0.01) {
                return value.toLocaleString(undefined, { maximumFractionDigits: 4 });
            } else {
                return value.toLocaleString(undefined, { maximumFractionDigits: 6 });
            }
        },
        isReductionPositive(metric) {
            const reductionPercent = parseFloat(metric.expected_reduction_percent);
            const higherIsBetter = metric.higher_is_better;

            if (higherIsBetter) {
                return reductionPercent <= 0;
            } else {
                return reductionPercent >= 0;
            }
        },
        initializeIncomeCostsChart() {
            // Initialize the Metrics Radial Chart
            const metricsRadialChartContainer = this.$refs.metricsRadialChartContainer;
            this.metricsRadialChart = echarts.init(metricsRadialChartContainer);
            this.metricsRadialChart.setOption(this.metricsRadialChartOptions, false); 

            // Initialize the Income/Costs Chart
            const incomeCostsChartContainer = this.$refs.incomeCostsChartContainer;
            this.incomeCostsChart = echarts.init(incomeCostsChartContainer);
            this.incomeCostsChart.setOption(this.incomeCostsChartOptions, false);

            // Initialize the ROI Evolution Chart
            const roiChartContainer = this.$refs.roiChartContainer;
            this.roiChart = echarts.init(roiChartContainer);
            this.roiChart.setOption(this.roiChartOptions, false);
        },
        async loadAnalysisData() {
            const { id_experiment } = this.$route.params;
            
            try {
                // Fetch the analysis data
                this.analysisData = await roiAnalyses.getAnalysis(id_experiment);
            } catch (error) {
                console.error("Error loading analysis data:", error);
                this.$message.error("Failed to load ROI analysis data. Please try again.");
            }
        },
        updateIncomeCostsChartData() {
            if (!this.costMetricsResults || this.costMetricsResults.length === 0) {
                return;
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

                this.incomeCostsChartOptions.xAxis.max = maxInferences;

                // Set chart with new data
                this.incomeCostsChartOptions.series[0].data = incomeData;
                this.incomeCostsChartOptions.series[1].data = costsData;
                // Color under the Income line
                if (breakEvenPoint !== 0) {
                    this.incomeCostsChartOptions.series[0].areaStyle.color = new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgba(255, 165, 0, 0.2)' // Light orange at top
                        },
                        {
                            offset: 1,
                            color: 'rgba(255, 165, 0, 0.05)' // Transparent at bottom
                        }
                    ]);
                    this.incomeCostsChartOptions.series[0].lineStyle.color = 'orange';
                    this.incomeCostsChartOptions.series[0].itemStyle.color = 'orange';
                }
                this.incomeCostsChart.setOption(this.incomeCostsChartOptions, false);
                return;
            }

            // Chart points when breakEvenPoint is POSITIVE 
            const maxInferences = breakEvenPoint * 2; // Extend the chart beyond the Break-Even Point in a defined range
            const maxCost = (maxInferences * newCostPerInference) + optimizationCost;

            const incomeData = [[0, 0], [maxInferences, (maxInferences * oldCostPerInference)]];
            const costsData = [[0, optimizationCost], [maxInferences, maxCost]];

            this.incomeCostsChartOptions.xAxis.max = maxInferences;

            // Set chart with new data
            this.incomeCostsChartOptions.series[0].data = incomeData;
            this.incomeCostsChartOptions.series[1].data = costsData;
            // Color under the Income line
            this.incomeCostsChartOptions.series[0].areaStyle.color = new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                    offset: 0,
                    color: 'rgba(0, 255, 0, 0.2)' // Light green at top
                },
                {
                    offset: 1,
                    color: 'rgba(0, 255, 0, 0)' // Transparent at bottom
                }
            ]);
            this.incomeCostsChartOptions.series[0].lineStyle.color = 'green';
            this.incomeCostsChartOptions.series[0].itemStyle.color = 'green';
            this.incomeCostsChart.setOption(this.incomeCostsChartOptions, false);
        },
        updateROIChartData() {
            if (!this.analysisData?.metrics_analysis) {
                return;
            }

            // Find the first energy metric with ROI evolution data
            const metricWithROIData = this.analysisData.metrics_analysis.find(metric => 
                metric.roi_evolution_chart_data && metric.roi_evolution_chart_data.length > 0
            );

            if (!metricWithROIData) {
                console.warn('No ROI evolution chart data found in metrics analysis');
                return;
            }

            const roiEvolutionData = metricWithROIData.roi_evolution_chart_data.map(item => 
                [item.inferences, item.roi]
            );

            if (roiEvolutionData.length > 0) {
                const maxInferences = Math.max(...roiEvolutionData.map(point => point[0]));
                this.roiChartOptions.xAxis.max = maxInferences;
            }

            // Update chart data
            this.roiChartOptions.series[0].data = roiEvolutionData;
            this.roiChart.setOption(this.roiChartOptions, false);
        },
        updateMetricsRadialChartData() {
            if (!this.analysisData?.metrics_analysis || this.analysisData.metrics_analysis.length === 0) {
                return;
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
            
            // Update chart options
            this.metricsRadialChartOptions.radar.indicator = indicators;
            this.metricsRadialChartOptions.legend.data = ['Baseline', 'Optimized'];
            this.metricsRadialChartOptions.series[0].data = [
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
            ];
            
            // Update chart with new data
            this.metricsRadialChart.setOption(this.metricsRadialChartOptions, false);
        },
        resizeCharts() {
            if (this.incomeCostsChart) this.incomeCostsChart.resize();
            if (this.roiChart) this.roiChart.resize();
            if (this.metricsRadialChart) this.metricsRadialChart.resize();
        },
        getDescriptionsColumnCount() {
            return window.innerWidth < 992 ? 1 : 2;
        },
        async generatePDFReport() {
            this.pdfGenerating = true;
            
            try {
                // Force resize and re-render all charts
                this.resizeCharts();
                
                // Explicitly update all charts to ensure they're rendered
                if (this.metricsRadialChart) {
                    this.updateMetricsRadialChartData();
                    this.metricsRadialChart.resize();
                }
                
                if (this.incomeCostsChart) {
                    this.updateIncomeCostsChartData();
                    this.incomeCostsChart.resize();
                }
                
                if (this.roiChart) {
                    this.updateROIChartData();
                    this.roiChart.resize();
                }
                
                // Give charts time to fully render before capturing
                await new Promise(resolve => setTimeout(resolve, 500));
                
                // Generate file name based on analysis data
                const fileName = `roi-analysis-${this.analysisData.id}-${this.analysisData.model_architecture_name}-${this.analysisData.tactic_parameter_option_details.tactic_name}.pdf`.replace(/\s+/g, '-').toLowerCase();
                
                // Generate the PDF
                const result = await pdfReportService.generatePDFReport(
                    this.analysisData,
                    'roi-analysis-container', 
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
    },
    mounted() {
        window.addEventListener('resize', this.resizeCharts);
        this.loadAnalysisData();
        this.initializeIncomeCostsChart();
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeCharts);
    },
    watch: {
        costMetricsResults: {
            handler: 'updateIncomeCostsChartData',
            deep: true
        },
        analysisData: {
            handler(newData) {
                this.updateROIChartData();
                this.updateMetricsRadialChartData();
            },
            deep: true
        }
    },
};
</script>

<style scoped>
.gaissa-roi-analyzer {
    padding: 20px;
}

.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin-bottom: 20px;
}

.metric-values-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin-top: 30px;
    margin-bottom: 15px;
}

.chart-description,
.results-description {
    margin-bottom: 10px;
}

.chart-container {
    width: 100%;
    height: 400px;
}

.mobile-card {
    margin-bottom: 20px;
}

.el-button {
    background-color: var(--gaissa_green);
    color: white;
    border-color: var(--gaissa_green);
}

.roi-cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.roi-card {
    flex: 1;
    min-width: 20px;
}

.roi-card h3 {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 15px;
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

.metric-card {
    display: flex;
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 8px;
    background-color: #f8f8f8;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    flex-direction: row;
    min-width: 0;
}

.metric-data {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.metric-title {
    font-size: 1.4rem !important;
    font-weight: bold;
    margin-bottom: 5px;
    color: #333;
}

.metric-description {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 20px;
}

.metric-comparison {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 15px;
    border-top: 1px dashed #ddd;
}

.change-indicator {
    display: flex;
    flex-direction: row;
    gap: 5px;               
    align-items: center;
    flex: 0;
    margin-right: 20px;
}

.change-percentage {
    font-size: 2.5rem;
    font-weight: bold;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.change-percentage.positive {
    color: green;
}

.change-percentage.negative {
    color: orange;
}

.arrow-container {
    margin-top: 5px;
}

.change-arrow {
    font-size: 2rem;
    font-weight: bold;
}

.change-arrow.positive {
    color: green;
}

.change-arrow.negative {
    color: orange;
}

.values-comparison {
    display: flex;
    justify-content: flex-start;
    gap: 40px;
    flex: 2;
    margin-left: 10px;
}

.value-container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    text-align: right;
}

.value-label {
    font-size: 0.9rem;
    color: #777;
    margin-bottom: 10px;
}

.value {
    font-size: 1.6rem;
    font-weight: bold;
    letter-spacing: -0.5px;
    line-height: 0.5;
}

.value.positive {
    color: green;
}

.value.negative {
    color: orange;
}

.unit {
    font-size: 0.9rem;
    opacity: 0.7;
    margin-left: 3px;
}

.recommendation-container {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
    margin-bottom: 20px;
    padding: 15px;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.recommendation-icon.positive {
    font-size: 2rem;
    color: var(--gaissa_green);
}

.recommendation-icon.negative {
    font-size: 2rem;
    color: orange;
}

.recommendation {
    font-size: 1.1rem;
    line-height: 1.5;
    padding: 10px;
    border-radius: 6px;
}

.recommendation.positive {
    background-color: rgba(0, 128, 0, 0.1);
    border-left: 4px solid green;
}

.recommendation.negative {
    background-color: rgba(255, 165, 0, 0.1);
    border-left: 4px solid orange;
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
    .roi-card {
        min-width: 100%;
        width: 100%;
    }
    
    .values-comparison {
        width: 100%;
        justify-content: space-between;
        gap: 10px;
        margin-left: 0;
    }
    
    .value-container {
        align-items: center;
    }

    .metric-card {
        flex-direction: column;
        align-items: center;
    }
}
</style>