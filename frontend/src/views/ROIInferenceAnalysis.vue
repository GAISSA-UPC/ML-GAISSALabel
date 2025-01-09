<template>
    <div class="roi-inference-analysis">
        <h1>{{ $t("ROI Inference Optimization Analysis") }}</h1>

        <el-row :gutter="20" type="flex" :justify="center" class="row-bg">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("Model Information") }}</h2>
                    <el-descriptions :column="1" border>
                        <el-descriptions-item :label="$t('Model name')">
                            {{ modelInfo.name }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Model optimization')">
                            {{ modelInfo.optimizationTechnique }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Model creation date')">
                            {{ formatData(modelInfo.creationDate) }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Analysis identifier')">
                            {{ analysisInfo.id }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Analysis registration date')">
                            {{ formatData(analysisInfo.registrationDate) }}
                        </el-descriptions-item>
                        <el-descriptions-item :label="$t('Country deploy')">
                            {{ analysisInfo.country }}
                        </el-descriptions-item>
                    </el-descriptions>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="mobile-card">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h2 class="section-title">{{ $t("ROI Chart") }}</h2>
                    <p class="chart-description">
                        {{ $t("This chart illustrates the evolution of costs and benefits associated with dynamic quantization over a range of inferences.") }}
                    </p>
                    <div ref="chartContainer" class="chart-container">
                        <!-- Chart will be rendered here -->
                    </div>
                </el-card>
            </el-col>

            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                <el-card shadow="always" :body-style="{ padding: '20px' }" style="margin-top: 20px">
                    <h2 class="section-title">{{ $t("ROI Results") }}</h2>
                    <p class="results-description">
                        {{ $t("This table provides a detailed breakdown of the ROI analysis over the defined optimization strategy. It illustrates specific data about the potential benefits associated with the dynamic quantization strategy over a range of inferences.") }}
                    </p>
                    <el-table :data="roiResults" style="width: 100%">
                        <el-table-column prop="name" :label="$t('Metric')" />
                        <el-table-column prop="value" :label="$t('Value')" />
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import { formatData } from "@/utils";
import * as echarts from 'echarts';

export default {
    name: "ROIInferenceAnalysis",
    data() {
        return {
            modelInfo: {
                name: "GPT-2",
                optimizationTechnique: "Dynamic quantization",
                creationDate: "2023-11-21 17:59",
            },
            analysisInfo: {
                id: 4,
                registrationDate: "2023-12-24 19:06",
                country: "Catalunya",
            },
            roiResults: [
                { name: "Optimization Cost", value: "79.72 €" },
                { name: "New Cost Per Inference", value: "3.0e-05 €" },
                { name: "Old Cost Per Inference", value: "1.24e-04 €" },
                { name: "ROI", value: "-0.999882" },
                { name: "Break-Even Point", value: "1,256,452 inferences" },
            ],
            chart: null,
            chartOptions: {
                xAxis: {
                    type: 'value',
                    name: this.$t('Number of Inferences'),
                    nameLocation: 'middle',
                    nameGap: 30,
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
                        data: [[0, 0], [2000000, 185]],
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
                        data: [[0, 80], [2000000, 145]], // Replace with actual data
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
                                    color: 'rgba(255, 0, 0, 0)' // Transparent at bottom
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
        loadAnalysisData() {
            const { id_model, optimization_technique, technique_param, id_experiment } = this.$route.params;

            // Fetch data from the API using the parameters
            // const data = await roiAnalysis.getAnalysis(id_model, optimization_technique, technique_param, id_experiment);

            // For now, mock data is used:
            this.modelInfo = {
                name: "GPT-2",
                optimizationTechnique: optimization_technique,
                creationDate: "2023-11-21 17:59",
            };

            this.analysisInfo = {
                id: id_experiment,
                registrationDate: "2023-12-24 19:06",
                country: "Catalunya",
            };

            this.roiResults = [
                { name: "Optimization Cost", value: "79.72 €" },
                { name: "New Cost Per Inference", value: "3.0e-05 €" },
                { name: "Old Cost Per Inference", value: "1.24e-04 €" },
                { name: "ROI", value: "-0.999882" },
                { name: "Break-Even Point", value: "1,256,452 inferences" },
            ];
        },
    },
    mounted() {
        this.loadAnalysisData();
        this.initializeChart();
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