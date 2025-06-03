<template>
    <div>
        <h2 class="section-title">{{ $t("ROI Evolution Chart") }}</h2>
        <p class="chart-description">
            {{ $t("This chart illustrates the evolution of the Return on Investment (ROI) of the specified technique over a range of inferences.") }}
        </p>
        <div ref="chartContainer" class="chart-container">
            <!-- Chart will be rendered here -->
        </div>
        <p>
            The ROI Evolution Chart shows the evolution of the Return on Investment (ROI) over a range of inferences. A
            positive ROI indicates that you've saved more money than you've spent on optimization and inferences. A
            negative ROI means you've spent more than you've saved. For example, a positive ROI of 0.5 means that for
            every €1 you've spent, you've earned/saved €0.5.
        </p>
    </div>
</template>

<script>
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
    GridComponent,
    TooltipComponent,
    LegendComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
echarts.use([
    GridComponent,
    TooltipComponent,
    LegendComponent,
    LineChart,
    CanvasRenderer
]);

export default {
    name: "ROIEvolutionChart",
    props: {
        chartData: {
            type: Object,
            required: true
        },
        formatNumber: {
            type: Function,
            required: true
        }
    },
    data() {
        return {
            chart: null,
            chartOptions: {
                xAxis: {
                    type: 'value',
                    name: this.$t('Number of Inferences'),
                    nameLocation: 'middle',
                    nameGap: 30,
                    axisLabel: {
                        formatter: this.formatNumber
                    }
                },
                yAxis: {
                    type: 'value',
                    name: this.$t('ROI'),
                    nameLocation: 'middle',
                    nameGap: 35,
                    axisLabel: {
                        formatter: this.formatNumber
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
    watch: {
        chartData: {
            handler: 'updateChart',
            deep: true,
            immediate: true
        }
    },
    methods: {
        initChart() {
            if (this.chart) {
                this.chart.dispose();
            }

            const chartContainer = this.$refs.chartContainer;
            if (!chartContainer) return;

            this.chart = echarts.init(chartContainer);
            this.updateChart();
        },
        updateChart() {
            if (!this.chartData || !this.chart) return;

            // Update chart options
            this.chartOptions.xAxis.max = this.chartData.maxInferences;
            this.chartOptions.series[0].data = this.chartData.roiEvolutionData;

            // Render the chart
            this.chart.setOption(this.chartOptions, true);
        },
        resize() {
            if (this.chart) {
                this.chart.resize();
            }
        }
    },
    mounted() {
        window.addEventListener('resize', this.resize);
        this.initChart();
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.resize);
        if (this.chart) {
            this.chart.dispose();
            this.chart = null;
        }
    }
};
</script>

<style scoped>
.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin-bottom: 20px;
}

.chart-description {
    margin-bottom: 10px;
}

.chart-container {
    width: 100%;
    height: 400px;
}
</style>
