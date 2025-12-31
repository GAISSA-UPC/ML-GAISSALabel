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
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
    MarkLineComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
    MarkLineComponent,
    LineChart,
    CanvasRenderer
]);


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
            customTooltipEl: null,
            hoverRafId: null,
            pendingHover: null,
            lastHoverX: null,
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
        interpolateValue(x, data) {
            if (!data || data.length === 0) return 0;
            const pts = data.map(p => Array.isArray(p) ? [Number(p[0]), Number(p[1])] : [Number(p.x), Number(p.y)]).sort((a, b) => a[0] - b[0]);
            if (pts.length === 1) return pts[0][1];
            if (x <= pts[0][0]) {
                const [x0, y0] = pts[0];
                const [x1, y1] = pts[1];
                const t = (x - x0) / (x1 - x0);
                return y0 + t * (y1 - y0);
            }
            if (x >= pts[pts.length - 1][0]) {
                const [x0, y0] = pts[pts.length - 2];
                const [x1, y1] = pts[pts.length - 1];
                const t = (x - x0) / (x1 - x0);
                return y0 + t * (y1 - y0);
            }
            for (let i = 0; i < pts.length - 1; i++) {
                const [x0, y0] = pts[i];
                const [x1, y1] = pts[i + 1];
                if (x0 <= x && x <= x1) {
                    if (x1 === x0) return y0;
                    const t = (x - x0) / (x1 - x0);
                    return y0 + t * (y1 - y0);
                }
            }
            return 0;
        },
        initChart() {
            if (this.chart) {
                this.chart.dispose();
            }

            const chartContainer = this.$refs.chartContainer;
            if (!chartContainer) return;

            this.chart = echarts.init(chartContainer);
            this.createCustomTooltip();
            this.updateChart();
            chartContainer.addEventListener('mousemove', this.handleChartMouseMove);
            chartContainer.addEventListener('mouseleave', this.handleChartMouseLeave);
        },
        updateChart() {
            if (!this.chartData || !this.chart) return;

            // Update chart options
            this.chartOptions.xAxis.max = this.chartData.maxInferences;
            this.chartOptions.series[0].data = this.chartData.incomeData;
            this.chartOptions.series[1].data = this.chartData.costsData;

            // Ensure hover marker series (index 2 and 3) exist for Income and Costs
            if (!this.chartOptions.series[2]) {
                this.chartOptions.series[2] = {
                    name: this.$t('Income Hover'),
                    type: 'scatter',
                    data: [],
                    symbol: 'circle',
                    symbolSize: 8,
                    hoverAnimation: false,
                    silent: false,
                    itemStyle: { color: 'green', borderColor: '#fff', borderWidth: 1, shadowBlur: 4, shadowColor: 'rgba(0,0,0,0.25)' },
                    z: 100
                };
            }
            if (!this.chartOptions.series[3]) {
                this.chartOptions.series[3] = {
                    name: this.$t('Costs Hover'),
                    type: 'scatter',
                    data: [],
                    symbol: 'circle',
                    symbolSize: 8,
                    hoverAnimation: false,
                    silent: false,
                    itemStyle: { color: 'red', borderColor: '#fff', borderWidth: 1, shadowBlur: 4, shadowColor: 'rgba(0,0,0,0.25)' },
                    z: 100
                };
            }

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

        ,createCustomTooltip() {
            const container = this.$refs.chartContainer;
            if (!container) return;
            this.destroyCustomTooltip();
            const el = document.createElement('div');
            el.className = 'custom-echarts-tooltip';
            el.style.position = 'absolute';
            el.style.pointerEvents = 'none';
            el.style.zIndex = 1000;
            el.style.display = 'none';
            el.style.minWidth = '140px';
            el.style.padding = '6px 8px';
            el.style.background = 'rgba(50,50,50,0.9)';
            el.style.color = '#fff';
            el.style.borderRadius = '4px';
            el.style.fontSize = '12px';
            container.style.position = container.style.position || 'relative';
            container.appendChild(el);
            this.customTooltipEl = el;
        },
        destroyCustomTooltip() {
            if (this.customTooltipEl && this.customTooltipEl.parentNode) {
                this.customTooltipEl.parentNode.removeChild(this.customTooltipEl);
            }
            this.customTooltipEl = null;
        },

        handleChartMouseMove(e) {
            const container = this.$refs.chartContainer;
            if (!container || !this.chart || !this.chartData) return;
            const rect = container.getBoundingClientRect();
            const px = e.clientX - rect.left;
            const py = e.clientY - rect.top;
            try {
                const dataCoord = this.chart.convertFromPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [px, py]);
                const xVal = Number(dataCoord[0]);
                if (Number.isFinite(xVal)) {
                    const xMax = (this.chartOptions && this.chartOptions.xAxis && this.chartOptions.xAxis.max) ? Number(this.chartOptions.xAxis.max) : Infinity;
                    const xMin = (this.chartOptions && this.chartOptions.xAxis && this.chartOptions.xAxis.min) ? Number(this.chartOptions.xAxis.min) : -Infinity;
                    const xClamped = Math.min(Math.max(xVal, xMin), xMax);
                    const xRounded = Math.round(xClamped);

                    const yIncome = this.interpolateValue(xRounded, this.chartData.incomeData);
                    const yCosts = this.interpolateValue(xRounded, this.chartData.costsData);

                    this.pendingHover = { xVal: xRounded, yIncome, yCosts, rect };
                    if (this.hoverRafId == null) {
                        this.hoverRafId = requestAnimationFrame(() => { this.processPendingHover(); });
                    }
                }
            } catch (err) {
                // ignore
            }
        },

        handleChartMouseLeave() {
            if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
            this.clearHover();
        },

        processPendingHover() {
            if (!this.pendingHover) { this.hoverRafId = null; return; }
            const { xVal, yIncome, yCosts, rect } = this.pendingHover;
            this.lastHoverX = xVal;

            try {
                if (!(Number.isFinite(xVal) && xVal > 0)) {
                    if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
                    try { this.chart.setOption({ series: [{}, {}, { data: [] }, { data: [] }] }, { notMerge: false }); } catch (e) {}
                    this.pendingHover = null; this.hoverRafId = null; return;
                }

                this.chart.setOption({ series: [{}, {}, { data: [{ value: [xVal, yIncome], symbolSize: 8, itemStyle: { color: 'green' } }] }, { data: [{ value: [xVal, yCosts], symbolSize: 8, itemStyle: { color: 'red' } }] }] }, { notMerge: false });
            } catch (err) {
                // ignore
            }

            try {
                const pixIncome = this.chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [xVal, yIncome]);
                const pixCosts = this.chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [xVal, yCosts]);
                const validIncome = Array.isArray(pixIncome) && pixIncome.every(v => Number.isFinite(v));
                const validCosts = Array.isArray(pixCosts) && pixCosts.every(v => Number.isFinite(v));
                if (!validIncome && !validCosts) {
                    if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
                } else {
                    const px = validIncome ? pixIncome[0] : pixCosts[0];
                    const py = Math.min(validIncome ? pixIncome[1] : Infinity, validCosts ? pixCosts[1] : Infinity);
                    if (this.customTooltipEl) {
                        const displayX = Number.isFinite(xVal) ? xVal.toLocaleString(undefined) : String(xVal);
                        const displayIncome = (this.formatNumber && typeof this.formatNumber === 'function') ? this.formatNumber(yIncome) : String(yIncome);
                        const displayCosts = (this.formatNumber && typeof this.formatNumber === 'function') ? this.formatNumber(yCosts) : String(yCosts);
                        this.customTooltipEl.innerHTML = `<div class="ct-line"><strong>${this.$t('Inferences')}:</strong> ${displayX}</div><div class="ct-line"><strong>${this.$t('Income')}:</strong> ${displayIncome}</div><div class="ct-line"><strong>${this.$t('Costs')}:</strong> ${displayCosts}</div>`;
                        // Show tooltip offscreen briefly to measure size
                        this.customTooltipEl.style.display = 'block';
                        this.customTooltipEl.style.visibility = 'hidden';
                        // measure
                        const tooltipW = this.customTooltipEl.offsetWidth || 160;
                        const tooltipH = this.customTooltipEl.offsetHeight || 60;


                        // Prefer placing tooltip to the LEFT and slightly HIGHER of the marker when possible
                        let left;
                        if (px - 12 - tooltipW >= 8) {
                            left = px - 12 - tooltipW; // left side
                        } else if (px + 12 + tooltipW <= rect.width - 8) {
                            left = px + 12; // fallback right side
                        } else {
                            // fallback clamp near left
                            left = Math.min(Math.max(px - 12 - tooltipW, 8), rect.width - tooltipW - 8);
                        }

                        // Prefer placing tooltip a bit higher than the marker to avoid occluding the point and line
                        let top;
                        if (py - 16 - tooltipH >= 8) {
                            top = py - 16 - tooltipH; // a bit higher
                        } else if (py - 12 - tooltipH >= 8) {
                            top = py - 12 - tooltipH;
                        } else if (py + 12 + tooltipH <= rect.height - 8) {
                            top = py + 12; // fallback below
                        } else {
                            top = Math.min(Math.max(py - 16 - tooltipH, 8), rect.height - tooltipH - 8);
                        }

                        this.customTooltipEl.style.left = `${left}px`;
                        this.customTooltipEl.style.top = `${top}px`;
                        this.customTooltipEl.style.visibility = 'visible';
                        this.customTooltipEl.style.display = 'block';
                    }
                }
            } catch (err) {
                if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
            }

            this.pendingHover = null;
            this.hoverRafId = null;
        },

        clearHover() {
            if (this.hoverRafId != null) {
                cancelAnimationFrame(this.hoverRafId);
                this.hoverRafId = null;
            }
            this.pendingHover = null;
            this.lastHoverX = null;
            try { if (this.chart) this.chart.setOption({ series: [{}, {}, { data: [] }, { data: [] }] }, { notMerge: false }); } catch (err) {}
        },
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
        const chartContainer = this.$refs.chartContainer;
        if (chartContainer) {
            chartContainer.removeEventListener('mousemove', this.handleChartMouseMove);
            chartContainer.removeEventListener('mouseleave', this.handleChartMouseLeave);
        }
        this.destroyCustomTooltip();
        if (this.hoverRafId != null) {
            cancelAnimationFrame(this.hoverRafId);
            this.hoverRafId = null;
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
