import { mount } from '@vue/test-utils';
import MetricsRadialChart from '@/tools/gaissaroianalyzer/components/MetricsRadialChart.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import flushPromises from 'flush-promises';
import * as echarts from 'echarts/core';

// Mock echarts modules
vi.mock('echarts/core', () => ({
    default: {
        init: vi.fn(),
        use: vi.fn(),
    },
    use: vi.fn(),
    init: vi.fn(),
}));

vi.mock('echarts/charts', () => ({
    RadarChart: vi.fn()
}));

vi.mock('echarts/components', () => ({
    LegendComponent: vi.fn(),
    TooltipComponent: vi.fn(),
    RadarComponent: vi.fn()
}));

vi.mock('echarts/renderers', () => ({
    CanvasRenderer: vi.fn()
}));

// Mock chart instance
const mockChartInstance = {
    setOption: vi.fn(),
    dispose: vi.fn(),
    resize: vi.fn()
};

// Mock echarts.init to return our mock instance
echarts.init = vi.fn(() => mockChartInstance);

describe('MetricsRadialChart.vue', () => {
    let wrapper;
    
    // Sample data for the component
    const defaultProps = {
        metricsData: {
            indicators: [
                { name: 'Accuracy', max: 1.0 },
                { name: 'Precision', max: 1.0 },
                { name: 'Recall', max: 1.0 },
                { name: 'F1-Score', max: 1.0 },
                { name: 'Inference Time', max: 100 }
            ],
            legendData: ['Baseline', 'Optimized'],
            seriesData: [
                {
                    value: [0.85, 0.82, 0.88, 0.85, 45],
                    name: 'Baseline',
                    itemStyle: { color: '#FF6B6B' }
                },
                {
                    value: [0.87, 0.85, 0.89, 0.87, 32],
                    name: 'Optimized',
                    itemStyle: { color: '#4ECDC4' }
                }
            ]
        },
        formatNumber: (num) => num.toLocaleString('en-US', { maximumFractionDigits: 2 })
    };

    beforeEach(() => {
        // Clear all mocks before each test
        vi.clearAllMocks();
        
        // Mock DOM APIs
        Object.defineProperty(window, 'addEventListener', {
            value: vi.fn(),
            writable: true
        });
        Object.defineProperty(window, 'removeEventListener', {
            value: vi.fn(),
            writable: true
        });

        wrapper = mount(MetricsRadialChart, {
            props: defaultProps,
            global: {
                plugins: [ElementPlus, i18n]
            }
        });
    });

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    });

    it('renders the component with correct title and description text', () => {
        expect(wrapper.find('h2.section-title').exists()).toBe(true);
        expect(wrapper.find('h2.section-title').text()).toContain('Metrics Chart');

        const description = wrapper.find('.chart-description');
        expect(description.exists()).toBe(true);
        expect(description.text()).toContain('This chart illustrates the expected effect of the tactic');
    });

    it('displays metrics explanation paragraph', () => {
        const paragraphs = wrapper.findAll('p');
        
        // Check for metrics explanation
        const metricsExplanation = paragraphs.find(p => 
            p.text().includes('The chart displays the baseline and new expected values')
        );
        expect(metricsExplanation).toBeDefined();
        expect(metricsExplanation.text()).toContain('baseline and new expected values for each metric');
        expect(metricsExplanation.text()).toContain('visualization of the impact of the tactic');
    });

    it('renders chart container element', () => {
        const chartContainer = wrapper.find('.chart-container');
        expect(chartContainer.exists()).toBe(true);
    });

    it('initializes chart on mount', async () => {
        await flushPromises();
        
        expect(echarts.init).toHaveBeenCalled();
        expect(mockChartInstance.setOption).toHaveBeenCalled();
    });

    it('disposes chart on unmount', async () => {
        await wrapper.unmount();
        
        expect(mockChartInstance.dispose).toHaveBeenCalled();
    });

    it('updates chart when metricsData prop changes', async () => {
        const newMetricsData = {
            indicators: [
                { name: 'Accuracy', max: 1.0 },
                { name: 'Speed', max: 100 },
                { name: 'Memory Usage', max: 1000 }
            ],
            legendData: ['Model A', 'Model B'],
            seriesData: [
                {
                    value: [0.90, 75, 800],
                    name: 'Model A',
                    itemStyle: { color: '#FF9999' }
                },
                {
                    value: [0.88, 85, 650],
                    name: 'Model B',
                    itemStyle: { color: '#99CCFF' }
                }
            ]
        };

        await wrapper.setProps({ metricsData: newMetricsData });
        await flushPromises();

        expect(mockChartInstance.setOption).toHaveBeenCalledTimes(3); // Once on init, once on mount, once on update
    });

    it('handles window resize events', () => {
        const resizeHandler = window.addEventListener.mock.calls.find(
            call => call[0] === 'resize'
        );
        
        expect(resizeHandler).toBeDefined();
        
        // Simulate window resize
        resizeHandler[1]();
        expect(mockChartInstance.resize).toHaveBeenCalled();
    });

    it('removes resize event listener on unmount', async () => {
        await wrapper.unmount();
        
        expect(window.removeEventListener).toHaveBeenCalledWith('resize', expect.any(Function));
    });

    it('sets correct chart options structure', async () => {
        await flushPromises();
        
        const setOptionCalls = mockChartInstance.setOption.mock.calls;
        expect(setOptionCalls.length).toBeGreaterThan(0);
        
        const chartOptions = setOptionCalls[setOptionCalls.length - 1][0];
        
        // Verify chart structure
        expect(chartOptions).toHaveProperty('legend');
        expect(chartOptions).toHaveProperty('radar');
        expect(chartOptions).toHaveProperty('series');
        expect(chartOptions).toHaveProperty('label');
        
        // Verify series structure
        expect(chartOptions.series).toHaveLength(1);
        expect(chartOptions.series[0].type).toBe('radar');
        
        // Verify radar component
        expect(chartOptions.radar).toHaveProperty('indicator');
        
        // Verify legend configuration
        expect(chartOptions.legend.bottom).toBe(0);
        expect(chartOptions.legend.itemGap).toBe(20);
    });

    it('updates radar indicators correctly when metricsData changes', async () => {
        const newData = {
            indicators: [
                { name: 'Performance', max: 100 },
                { name: 'Efficiency', max: 1.0 },
                { name: 'Quality', max: 10 }
            ],
            legendData: ['Version 1', 'Version 2'],
            seriesData: [
                {
                    value: [85, 0.75, 8.5],
                    name: 'Version 1'
                },
                {
                    value: [92, 0.82, 9.1],
                    name: 'Version 2'
                }
            ]
        };

        await wrapper.setProps({ metricsData: newData });
        await flushPromises();

        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.radar.indicator).toEqual(newData.indicators);
        expect(chartOptions.legend.data).toEqual(newData.legendData);
        expect(chartOptions.series[0].data).toEqual(newData.seriesData);
    });

    it('configures legend correctly', async () => {
        await flushPromises();
        
        expect(wrapper.vm.chartOptions.legend.bottom).toBe(0);
        expect(wrapper.vm.chartOptions.legend.itemGap).toBe(20);
        expect(wrapper.vm.chartOptions.legend.data).toEqual(defaultProps.metricsData.legendData);
    });

    it('configures label formatter correctly', () => {
        const labelFormatter = wrapper.vm.chartOptions.label.formatter;
        expect(typeof labelFormatter).toBe('function');
        expect(wrapper.vm.chartOptions.label.show).toBe(true);
        
        // Test the formatter function
        const mockParams = { value: 123.456 };
        const formattedValue = labelFormatter(mockParams);
        expect(formattedValue).toBe('123.46'); // Should use formatNumber
    });

    it('handles multiple chart updates without memory leaks', async () => {
        const updates = [
            {
                indicators: [{ name: 'Metric A', max: 50 }],
                legendData: ['Test 1'],
                seriesData: [{ value: [25], name: 'Test 1' }]
            },
            {
                indicators: [{ name: 'Metric B', max: 75 }],
                legendData: ['Test 2'],
                seriesData: [{ value: [40], name: 'Test 2' }]
            },
            {
                indicators: [{ name: 'Metric C', max: 100 }],
                legendData: ['Test 3'],
                seriesData: [{ value: [60], name: 'Test 3' }]
            }
        ];

        for (const update of updates) {
            await wrapper.setProps({ metricsData: update });
            await flushPromises();
        }

        // Should have called setOption for each update plus initial calls
        expect(mockChartInstance.setOption.mock.calls.length).toBe(updates.length + 2);
        
        // Should not have created multiple chart instances
        expect(echarts.init.mock.calls.length).toBe(1);
    });

    it('handles empty or invalid metrics data gracefully', async () => {
        const emptyData = {
            indicators: [],
            legendData: [],
            seriesData: []
        };

        await wrapper.setProps({ metricsData: emptyData });
        await flushPromises();

        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.radar.indicator).toEqual([]);
        expect(chartOptions.legend.data).toEqual([]);
        expect(chartOptions.series[0].data).toEqual([]);
        expect(mockChartInstance.setOption).toHaveBeenCalled();
    });

    it('disposes existing chart before creating new one in initChart', async () => {
        // First initialization already happened in mounted
        expect(echarts.init).toHaveBeenCalledTimes(1);
        
        // Call initChart again to test disposal
        wrapper.vm.initChart();
        await flushPromises();
        
        expect(mockChartInstance.dispose).toHaveBeenCalled();
        expect(echarts.init).toHaveBeenCalledTimes(2);
    });
});
