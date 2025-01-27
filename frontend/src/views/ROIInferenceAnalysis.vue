<template>
    <div class="roi-inference-analysis">
        <h1>{{ $t("ROI Inference Optimization Analysis") }}</h1>

        <el-row :gutter="20" type="flex" :justify="center" class="row-bg">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Model Information") }}</h2>
                    <el-descriptions v-if="analysisData" :column="1" border>
                        <el-descriptions-item :label="$t('Model name')">
                            {{ analysisData.model_name }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Model optimization')">
                            {{ analysisData.optimization_technique_name }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Analysis identifier')">
                            {{ analysisData.id }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Analysis registration date')">
                            {{ formatData(analysisData.registration_date) }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Country deploy')">
                            {{ analysisData.country }}
                        </el-descriptions-item>
                    </el-descriptions>
                    <p v-else>{{ $t("Loading model information...") }}</p>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Costs/Benefits Chart") }}</h2>
                    <p class="chart-description">
                        {{ $t("This chart illustrates the evolution of costs and benefits associated with dynamic quantization over a range of inferences.") }}
                    </p>
                    <p>
                        <strong>Benefits:</strong> how much money you save cumulatively as you perform more inferences<br>
                        <strong>Costs:</strong> total expenses, which include the initial optimization cost plus the new cost per inference
                    </p>
                    <div ref="chartContainer" class="chart-container">
                        <!-- Chart will be rendered here -->
                    </div>
                    <p>
                        <strong>ROI &lt; 0:</strong> When the "Costs" line is above the "Benefits" line, your ROI is negative. This means you've spent more on optimization and inferences than you've saved.
                        <br>
                        <strong>ROI = 0 (Positive-ROI Point):</strong> The point where the "Costs" line and "Benefits" line intersect is the positive-ROI point. At this point, your total savings equal your total costs.
                        <br>
                        <strong>ROI &gt; 0:</strong> When the "Benefits" line is above the "Costs" line, your ROI is positive. You've saved more than you've spent.
                    </p>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                <el-card shadow="always" :body-style="{ padding: '20px' }" style="margin-top: 20px">
                    <h2 class="section-title">{{ $t("ROI Results") }}</h2>
                    <p class="results-description">
                        {{ $t("This table provides a detailed breakdown of the ROI analysis over the defined optimization strategy. It illustrates specific data about the potential benefits associated with the dynamic quantization strategy over a range of inferences.") }}
                    </p>
                    <el-table v-if="roiResults.length" :data="roiResults" style="width: 100%">
                        <el-table-column prop="name" :label="$t('Metric')" />
                        <el-table-column prop="value" :label="$t('Value')" />
                    </el-table>
                    <p v-else>{{ $t("Loading ROI results...") }}</p>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { formatData } from "@/utils";
import * as echarts from 'echarts';
import roiAnalyses from "@/controllers/roiAnalyses";

export default {
    name: "ROIInferenceAnalysis",
    data() {
        return {
            analysisData: null,
            roiResults: [],
            chart: null,
            chartOptions: {
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
                        name: this.$t('Benefits'),
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
                    trigger: 'axis'
                },
                legend: {
                    data: [this.$t('Benefits'), this.$t('Costs')],
                    bottom: 0,
                }
            }
        };
    },
    methods: {
        formatData,
        initializeChart() {
            const chartContainer = this.$refs.chartContainer;
            this.chart = echarts.init(chartContainer);
            this.chart.setOption(this.chartOptions);
        },
        async loadAnalysisData() {
            const { id_model, id_experiment } = this.$route.params;

            // Fetch the analysis data
            this.analysisData = await roiAnalyses.getAnalysis(
                id_model,
                id_experiment
            );

            this.roiResults = this.analysisData.roi_results;
        },
        updateChartData() {
            if (!this.roiResults || this.roiResults.length === 0) {
                return;
            }

            const optimizationCost = parseFloat(this.roiResults.find(r => r.name === 'Optimization Cost')?.value) || 0;
            const newCostPerInference = parseFloat(this.roiResults.find(r => r.name === 'New Cost Per Inference')?.value) || 0;
            const oldCostPerInference = parseFloat(this.roiResults.find(r => r.name === 'Original Cost Per Inference')?.value) || 0;
            const positiveRoiPointValue = this.roiResults.find(r => r.name === 'Positive-ROI Point')?.value;
            const positiveRoiPoint = !isFinite(parseFloat(positiveRoiPointValue)) ? Infinity : parseFloat(positiveRoiPointValue) || 0;

            // Chart points when positiveRoiPoint is NEGATIVE or INFINITE 
            if (!isFinite(positiveRoiPoint) || positiveRoiPoint < 0) {
                const maxInferences = 2000000;

                const maxCost = (maxInferences * newCostPerInference) + optimizationCost;

                const benefitsData = [[0, 0], [maxInferences, (maxInferences * (oldCostPerInference - newCostPerInference))]];
                const costsData = [[0, optimizationCost], [maxInferences, maxCost]];

                this.chartOptions.xAxis.max = maxInferences;

                // Set chart with new data
                this.chartOptions.series[0].data = benefitsData;
                this.chartOptions.series[1].data = costsData;
                // Color under the Benefits line
                this.chartOptions.series[0].areaStyle.color = new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    {
                        offset: 0,
                        color: 'rgba(255, 165, 0, 0.2)' // Light orange at top
                    },
                    {
                        offset: 1,
                        color: 'rgba(255, 165, 0, 0.05)' // Transparent at bottom
                    }
                ]);
                this.chartOptions.series[0].lineStyle.color = 'orange';
                this.chartOptions.series[0].itemStyle.color = 'orange';
                this.chart.setOption(this.chartOptions, true);
                return;
            }

            // Chart points when positiveRoiPoint is POSITIVE 
            const maxInferences = positiveRoiPoint * 2; // Extend the chart beyond the Positive-ROI Point in a defined range
            const maxCost = (maxInferences * newCostPerInference) + optimizationCost;

            const benefitsData = [[0, 0], [maxInferences, (maxInferences * (oldCostPerInference - newCostPerInference))]];
            const costsData = [[0, optimizationCost], [maxInferences, maxCost]];

            this.chartOptions.xAxis.max = maxInferences;

            // Set chart with new data
            this.chartOptions.series[0].data = benefitsData;
            this.chartOptions.series[1].data = costsData;
            // Color under the Benefits line
            this.chartOptions.series[0].areaStyle.color = new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                    offset: 0,
                    color: 'rgba(0, 255, 0, 0.2)' // Light green at top
                },
                {
                    offset: 1,
                    color: 'rgba(0, 255, 0, 0)' // Transparent at bottom
                }
            ]);
            this.chartOptions.series[0].lineStyle.color = 'green';
            this.chartOptions.series[0].itemStyle.color = 'green';
            this.chart.setOption(this.chartOptions, true);
        },
    },
    mounted() {
        this.loadAnalysisData();
        this.initializeChart();
    },
    watch: {
        roiResults: {
            handler: 'updateChartData',
            deep: true
        }
    },
};
</script>

<style scoped>
.roi-inference-analysis {
    padding: 20px;
}

.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin-bottom: 20px;
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