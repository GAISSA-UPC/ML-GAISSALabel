<template>
    <div>
        <h2 class="section-title">{{ $t("Metrics Chart") }}</h2>
        <p class="chart-description">
            {{ $t("This chart illustrates the expected effect of the tactic over a set of the metrics.") }}
        </p>
        <div ref="chartContainer" class="chart-container">
            <!-- Chart will be rendered here -->
        </div>
        <p>
            The chart displays the baseline and new expected values for each metric, allowing the visualization of the
            impact of the tactic.
        </p>
    </div>
</template>

<script>
import * as echarts from 'echarts/core';
import { RadarChart } from 'echarts/charts';
import {
    LegendComponent,
    TooltipComponent,
    RadarComponent,
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
echarts.use([
    LegendComponent,
    TooltipComponent,
    RadarComponent,
    RadarChart,
    CanvasRenderer
]);

export default {
    name: "MetricsRadialChart",
    props: {
        metricsData: {
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
                legend: {
                    bottom: 0,
                    itemGap: 20,
                    data: [],
                },
                label: {
                    show: true,
                    formatter: function (params) {
                        return typeof params.value === 'number' ?
                            this.formatNumber(params.value) : params.value;
                    }.bind(this)
                },
                radar: {
                    indicator: []
                },
                series: [
                    {
                        type: 'radar',
                        data: []
                    }
                ],
            }
        };
    },
    watch: {
        metricsData: {
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
            this.chart.setOption(this.chartOptions, true);

            this.updateChart();
        },
        updateChart() {
            if (!this.metricsData || !this.chart) return;

            // Update chart options
            this.chartOptions.radar.indicator = this.metricsData.indicators || [];
            this.chartOptions.legend.data = this.metricsData.legendData || [];
            this.chartOptions.series[0].data = this.metricsData.seriesData || [];

            // Update chart with new data
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
