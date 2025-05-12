<template>
    <div>
        <h2 class="section-title">{{ $t("Income/Costs Chart") }}</h2>
        <p class="chart-description">
            {{ $t("This chart illustrates the evolution of income and costs over a range of inferences for the specified technique.") }}
        </p>
        <p>
            <strong>Income:</strong> how much money you would spend on inferences if you didn't optimize your model.<br>
            <strong>Costs:</strong> total expenses, which include the initial optimization cost plus the new cost per
            inference.
        </p>
        <div ref="chartContainer" class="chart-container">
            <!-- Chart will be rendered here -->
        </div>
        <p>
            <strong>ROI &lt; 0:</strong> When the "Costs" line is above the "Income" line, your ROI is negative. This
            means you've spent more on optimization and inferences than you would have if you hadn't optimized your
            model.
            <br>
            <strong>ROI = 0 (Break-Even Point):</strong> The point where the "Costs" line and "Income" line intersect is
            the Break-Even point. At this point, your total savings equal your total costs.
            <br>
            <strong>ROI &gt; 0:</strong> When the "Income" line is above the "Costs" line, your ROI is positive. This
            means you've spent less than you would have if you hadn't optimized your model. This means you are saving
            money.
        </p>
    </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: "IncomeCostsChart",
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
                    min: 0,
                    axisLabel: {
                        formatter: this.formatNumber
                    }
                },
                yAxis: {
                    type: 'value',
                    name: this.$t('Amount (€)'),
                    nameLocation: 'middle',
                    nameGap: 35,
                    axisLabel: {
                        formatter: this.formatNumber
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
            this.chartOptions.series[0].data = this.chartData.incomeData;
            this.chartOptions.series[1].data = this.chartData.costsData;

            // Update colors based on break-even type
            if (this.chartData.breakEvenType === 'infinite') {
                // Orange theme for infinite/negative break-even
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
            } else {
                // Green theme for positive break-even
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
            }

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
    beforeDestroy() {
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
