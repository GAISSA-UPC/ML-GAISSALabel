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
import { LineChart, ScatterChart } from 'echarts/charts';
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
    ScatterChart,
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
            customTooltipEl: null,
            hoverRafId: null,
            pendingHover: null,
            lastHoverX: null,
            chartOptions: {
                xAxis: {
                    type: 'value',
                    min: 0,
                    name: this.$t('Number of Inferences'),
                    nameLocation: 'middle',
                    nameGap: 30,
                    axisLabel: {
                        formatter: (v) => {
                            const val = Number.isFinite(v) ? Math.round(v) : v;
                            return (this.formatNumber && typeof this.formatNumber === 'function') ? this.formatNumber(val) : String(val);
                        }
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
                        emphasis: {
                            focus: 'series'
                        },
                    },
                    {
                        name: this.$t('Hover Point'),
                        type: 'scatter',
                        data: [],
                        symbol: 'circle',
                        symbolSize: 8,
                        hoverAnimation: false,
                        silent: false,
                        zlevel: 10,
                        itemStyle: {
                            color: 'rgb(220,20,60)',
                            borderColor: '#fff',
                            borderWidth: 1,
                            shadowBlur: 4,
                            shadowColor: 'rgba(0,0,0,0.25)'
                        },
                        z: 100
                    }
                ],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    },
                    formatter: null
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
        interpolateValue(x, data) {
            if (!data || data.length === 0) return 0;
            // Normalize array of [x,y]
            const pts = data.map(p => Array.isArray(p) ? [Number(p[0]), Number(p[1])] : [Number(p.x), Number(p.y)]).sort((a, b) => a[0] - b[0]);
            if (pts.length === 1) return pts[0][1];

            // If x is before first or after last, extrapolate using first two or last two
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

            // Find surrounding points for interpolation
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
            // Attach mouse listeners for showing interpolated tooltip
            chartContainer.addEventListener('mousemove', this.handleChartMouseMove);
            chartContainer.addEventListener('mouseleave', this.handleChartMouseLeave);
        },
        updateChart() {
            if (!this.chartData || !this.chart) return;

            // Update chart options
            this.chartOptions.xAxis.max = this.chartData.maxInferences;
            this.chartOptions.series[0].data = this.chartData.roiEvolutionData;
            // clear hover marker data when updating
            if (this.chartOptions.series[1]) this.chartOptions.series[1].data = [];

            // Set tooltip formatter to compute interpolated/extrapolated ROI for hovered inference count
            const self = this;
            this.chartOptions.tooltip.formatter = function (params) {
                // params is an array when trigger is 'axis'
                const p = Array.isArray(params) ? params[0] : params;
                const axisX = Number(p.axisValue != null ? p.axisValue : (Array.isArray(p.value) ? p.value[0] : p.value));
                const y = self.interpolateValue(axisX, self.chartData.roiEvolutionData);
                return `${self.$t('Number of Inferences')}: ${self.formatNumber(axisX)}<br/>${self.$t('ROI')}: ${self.formatNumber(y)}`;
            };

            // Render the chart
            this.chart.setOption(this.chartOptions, true);
        },
        resize() {
            if (this.chart) {
                this.chart.resize();
                // reposition tooltip if visible
                if (this.customTooltipEl && this.customTooltipEl.style.display === 'block') {
                    this.customTooltipEl.style.display = 'none';
                }
            }
        }
        ,
        createCustomTooltip() {
            const container = this.$refs.chartContainer;
            if (!container) return;
            this.destroyCustomTooltip();
            const el = document.createElement('div');
            el.className = 'custom-echarts-tooltip';
            el.style.position = 'absolute';
            el.style.pointerEvents = 'none';
            el.style.zIndex = 1000;
            el.style.display = 'none';
            el.style.minWidth = '120px';
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
                    const yVal = this.interpolateValue(xVal, this.chartData.roiEvolutionData);

                    // clamp and round inference x to integer (inferences are integers)
                    const xMax = (this.chartOptions && this.chartOptions.xAxis && this.chartOptions.xAxis.max) ? Number(this.chartOptions.xAxis.max) : Infinity;
                    const xMin = (this.chartOptions && this.chartOptions.xAxis && this.chartOptions.xAxis.min) ? Number(this.chartOptions.xAxis.min) : -Infinity;
                    const xClamped = Math.min(Math.max(xVal, xMin), xMax);
                    const xRounded = Math.round(xClamped);

                    // compute value at integer x
                    const yAtRounded = this.interpolateValue(xRounded, this.chartData.roiEvolutionData);

                    // store pending hover and schedule RAF to throttle updates
                    this.pendingHover = { xVal: xRounded, yVal: yAtRounded };
                    if (this.hoverRafId == null) {
                        this.hoverRafId = requestAnimationFrame(() => {
                            this.processPendingHover(rect);
                        });
                    }
                }
            } catch (err) {
                // convertFromPixel may throw if out of grid
            }
        },
        handleChartMouseLeave() {
            if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
            this.clearHover();
        },

        processPendingHover(rect) {
            if (!this.pendingHover) {
                this.hoverRafId = null;
                return;
            }
            const { xVal, yVal } = this.pendingHover;
            this.lastHoverX = xVal;
            // update scatter hover marker (series index 1) once per RAF
                try {
                    // hide marker for non-positive inferences
                    if (!(Number.isFinite(xVal) && xVal > 0)) {
                        if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
                        try { this.chart.setOption({ series: [{}, { data: [] }] }, { notMerge: false }); } catch(e) {}
                        this.pendingHover = null;
                        this.hoverRafId = null;
                        return;
                    }

                    // set data with explicit symbolSize and value to ensure canvas draws a visible marker (smaller)
                    this.chart.setOption({ series: [{}, { data: [{ value: [xVal, yVal], symbolSize: 8, itemStyle: { color: 'rgb(220,20,60)' } }] }] }, { notMerge: false });
                } catch (err) {
                    // ignore
                }

            // position tooltip attached to the calculated point
            try {
                const pixel = this.chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [xVal, yVal]);
                if (!Array.isArray(pixel) || pixel.some(v => !Number.isFinite(v))) {
                    if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
                } else {
                    const px2 = pixel[0];
                    const py2 = pixel[1];
                    if (this.customTooltipEl) {
                        // Show full integer for inferences (no abbreviation)
                        const displayX = Number.isFinite(xVal) ? xVal.toLocaleString(undefined) : String(xVal);
                        const displayY = (this.formatNumber && typeof this.formatNumber === 'function') ? this.formatNumber(yVal) : String(yVal);
                        this.customTooltipEl.innerHTML = `<div class="ct-line"><strong>${this.$t('Inferences')}:</strong> ${displayX}</div><div class="ct-line"><strong>${this.$t('ROI')}:</strong> ${displayY}</div>`;
                        const left = Math.min(Math.max(px2 + 12, 8), rect.width - 160);
                        const top = Math.min(Math.max(py2 + 12, 8), rect.height - 60);
                        this.customTooltipEl.style.left = `${left}px`;
                        this.customTooltipEl.style.top = `${top}px`;
                        this.customTooltipEl.style.display = 'block';
                    }
                }
            } catch (err) {
                if (this.customTooltipEl) this.customTooltipEl.style.display = 'none';
            }

            // clear pending and RAF id
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
            try {
                if (this.chart) this.chart.setOption({ series: [{}, { data: [] }] }, { notMerge: false });
            } catch (err) {
                // ignore
            }
        }
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
        // cancel any pending RAF
        if (this.hoverRafId != null) {
            cancelAnimationFrame(this.hoverRafId);
            this.hoverRafId = null;
        }
    },

    // Add tooltip helper methods and event handlers into the main methods block
    mounted() {
        window.addEventListener('resize', this.resize);
        this.initChart();
    },
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

.custom-echarts-tooltip .ct-line {
    margin: 2px 0;
}
</style>
