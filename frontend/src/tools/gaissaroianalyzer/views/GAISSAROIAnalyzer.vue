<template>
    <div class="gaissa-roi-analyzer">
        <h1>{{ $t("GAISSA ROI Analyzer") }}</h1>

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
                        <el-descriptions-item :label="$t('Analysis registration date')">
                            {{ formatData(analysisData.dateRegistration) }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Country deploy')">
                            {{ analysisData.country }}
                        </el-descriptions-item>
                    </el-descriptions>
                    <p v-else>{{ $t("Loading model information...") }}</p>
                </el-card>

                <div style="margin-bottom: 20px"></div>

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

            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card">
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

            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("ROI Results") }}</h2>
                    <p class="results-description">
                        {{ $t("This table provides a detailed breakdown of the ROI analysis over the defined tactic strategy. It illustrates specific data about the potential benefits associated with the applied ML tactic.") }}
                    </p>
                    <h3 v-if="analysisData?.metrics_analysis?.length" class="metric-values-title">{{ $t("Baseline Metrics") }}</h3>
                    <el-table v-if="analysisData?.metrics_analysis?.length" :data="analysisData.metrics_analysis" style="width: 100%; margin-top: 15px;">
                        <el-table-column prop="metric_name" :label="$t('Metric')" />
                        <el-table-column prop="baseline_value" :label="$t('Baseline Value')" />
                        <el-table-column prop="expected_reduction_percent" :label="$t('Reduction (%)')" />
                        <el-table-column prop="new_expected_value" :label="$t('New Expected Value')" />
                    </el-table>
                    
                    <p v-if="!roiResults.length && !analysisData">{{ $t("Loading ROI results...") }}</p>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { formatData } from "@/utils";
import * as echarts from 'echarts';
import roiAnalyses from "@/tools/gaissaroianalyzer/services/roiAnalyses";

export default {
    name: "GAISSAROIAnalyzer",
    data() {
        return {
            analysisData: null,
            roiResults: [],
            incomeCostsChart: null,
            roiChart: null,
            incomeCostsChartOptions: {
                xAxis: {
                    type: 'value',
                    name: this.$t('Number of Inferences'),
                    nameLocation: 'middle',
                    nameGap: 30,
                    min: 0,
                },
                yAxis: {
                    type: 'value',
                    name: this.$t('Amount (€)'),
                    nameLocation: 'middle',
                    nameGap: 35,
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
                },
                yAxis: {
                    type: 'value',
                    name: this.$t('ROI'),
                    nameLocation: 'middle',
                    nameGap: 35,
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
    methods: {
        formatData,
        initializeIncomeCostsChart() {
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
                
                if (this.analysisData && this.analysisData.roi_results) {
                    this.roiResults = this.analysisData.roi_results;
                } else {
                    console.error("No ROI results found in the analysis data");
                    this.roiResults = [];
                }
            } catch (error) {
                console.error("Error loading analysis data:", error);
                this.$message.error("Failed to load ROI analysis data. Please try again.");
            }
        },
        updateIncomeCostsChartData() {
            if (!this.roiResults || this.roiResults.length === 0) {
                return;
            }

            const optimizationCost = parseFloat(this.roiResults.find(r => r.name === 'Optimization Cost')?.value) || 0;
            const newCostPerInference = parseFloat(this.roiResults.find(r => r.name === 'New Cost Per Inference')?.value) || 0;
            const oldCostPerInference = parseFloat(this.roiResults.find(r => r.name === 'Original Cost Per Inference')?.value) || 0;
            const breakEvenPointValue = this.roiResults.find(r => r.name === 'Break-Even Point')?.value;
            const breakEvenPoint = !isFinite(parseFloat(breakEvenPointValue)) ? Infinity : parseFloat(breakEvenPointValue) || 0;

            // Chart points when breakEvenPoint is NEGATIVE or INFINITE 
            if (!isFinite(breakEvenPoint) || breakEvenPoint < 0) {
                const maxInferences = 2000000;

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
                        color: 'rgba(255, 165, 0, 0.2)' // Light orange at top
                    },
                    {
                        offset: 1,
                        color: 'rgba(255, 165, 0, 0.05)' // Transparent at bottom
                    }
                ]);
                this.incomeCostsChartOptions.series[0].lineStyle.color = 'orange';
                this.incomeCostsChartOptions.series[0].itemStyle.color = 'orange';
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
            if (!this.analysisData || !this.analysisData.roi_evolution_chart_data) {
                return;
            }

            this.roiChartOptions.xAxis.max = Math.max(...this.analysisData.roi_evolution_chart_data.map(item => item.inferences));

            const roiEvolutionData = this.analysisData.roi_evolution_chart_data.map(item => [item.inferences, item.roi]);
            this.roiChartOptions.series[0].data = roiEvolutionData;

            this.roiChart.setOption(this.roiChartOptions, false);
        },
        resizeCharts() {
            if (this.incomeCostsChart) this.incomeCostsChart.resize();
            if (this.roiChart) this.roiChart.resize();
        },
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
        roiResults: {
            handler: 'updateIncomeCostsChartData',
            deep: true
        },
        analysisData: {
            handler: 'updateROIChartData',
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

@media (max-width: 768px) {
    .mobile-card {
        margin-bottom: 20px;
    }
}
</style>