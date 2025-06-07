import { mount } from '@vue/test-utils';
import ROIEvolutionChart from '@/tools/gaissaroianalyzer/components/ROIEvolutionChart.vue';
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
    LineChart: vi.fn()
}));

vi.mock('echarts/components', () => ({
    GridComponent: vi.fn(),
    TooltipComponent: vi.fn(),
    LegendComponent: vi.fn()
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

describe('ROIEvolutionChart.vue', () => {
    let wrapper;
    
    // Sample data for the component
    const defaultProps = {
        chartData: {
            maxInferences: 100000,
            roiEvolutionData: [
                [0, -1.0],
                [10000, -0.5],
                [25000, 0.0],
                [50000, 0.3],
                [75000, 0.45],
                [100000, 0.5]
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

        wrapper = mount(ROIEvolutionChart, {
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
        expect(wrapper.find('h2.section-title').text()).toContain('ROI Evolution Chart');

        const description = wrapper.find('.chart-description');
        expect(description.exists()).toBe(true);
        expect(description.text()).toContain('This chart illustrates the evolution of the Return on Investment');
    });

    it('displays ROI explanation paragraph', () => {
        const paragraphs = wrapper.findAll('p');
        
        // Check for ROI explanation
        const roiExplanation = paragraphs.find(p => 
            p.text().includes('The ROI Evolution Chart shows the evolution of the Return on Investment')
        );
        expect(roiExplanation).toBeDefined();
        expect(roiExplanation.text()).toContain('positive ROI indicates that you\'ve saved more money');
        expect(roiExplanation.text()).toContain('negative ROI means you\'ve spent more than you\'ve saved');
        expect(roiExplanation.text()).toContain('positive ROI of 0.5 means that for every €1 you\'ve spent');
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

    it('updates chart when chartData prop changes', async () => {
        const newChartData = {
            maxInferences: 200000,
            roiEvolutionData: [
                [0, -2.0],
                [50000, -0.8],
                [100000, 0.0],
                [150000, 0.4],
                [200000, 0.7]
            ]
        };

        await wrapper.setProps({ chartData: newChartData });
        await flushPromises();

        expect(mockChartInstance.setOption).toHaveBeenCalledTimes(2); // Once on mount, once on update
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
        expect(chartOptions).toHaveProperty('xAxis');
        expect(chartOptions).toHaveProperty('yAxis');
        expect(chartOptions).toHaveProperty('series');
        expect(chartOptions).toHaveProperty('tooltip');
        expect(chartOptions).toHaveProperty('legend');
        
        // Verify series structure
        expect(chartOptions.series).toHaveLength(1);
        expect(chartOptions.series[0].name).toContain('ROI Evolution');
        expect(chartOptions.series[0].type).toBe('line');
        expect(chartOptions.series[0].smooth).toBe(true);
        expect(chartOptions.series[0].showSymbol).toBe(false);
        
        // Verify axis configuration
        expect(chartOptions.xAxis.type).toBe('value');
        expect(chartOptions.yAxis.type).toBe('value');
        expect(chartOptions.xAxis.name).toContain('Number of Inferences');
        expect(chartOptions.yAxis.name).toContain('ROI');
    });

    it('applies correct color scheme for ROI evolution line', async () => {
        await flushPromises();

        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.series[0].itemStyle.color).toBe('rgb(0, 71, 171)');
        expect(chartOptions.series[0].lineStyle.color).toBe('rgb(0, 71, 171)');
    });

    it('updates data series correctly when chartData changes', async () => {
        const newData = {
            maxInferences: 150000,
            roiEvolutionData: [
                [0, -1.5],
                [30000, -0.2],
                [60000, 0.1],
                [90000, 0.35],
                [120000, 0.5],
                [150000, 0.6]
            ]
        };

        await wrapper.setProps({ chartData: newData });
        await flushPromises();

        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.xAxis.max).toBe(150000);
        expect(chartOptions.series[0].data).toEqual(newData.roiEvolutionData);
    });

    it('applies formatNumber function to axis labels', () => {
        expect(wrapper.vm.chartOptions.xAxis.axisLabel.formatter).toBe(wrapper.vm.formatNumber);
        expect(wrapper.vm.chartOptions.yAxis.axisLabel.formatter).toBe(wrapper.vm.formatNumber);
    });

    it('configures legend correctly', () => {
        expect(wrapper.vm.chartOptions.legend.data).toEqual([
            expect.stringContaining('ROI Evolution')
        ]);
        expect(wrapper.vm.chartOptions.legend.bottom).toBe(0);
    });

    it('configures tooltip correctly', () => {
        expect(wrapper.vm.chartOptions.tooltip.trigger).toBe('axis');
        expect(wrapper.vm.chartOptions.tooltip.axisPointer.type).toBe('cross');
    });

    it('handles multiple chart updates without memory leaks', async () => {
        const updates = [
            { 
                maxInferences: 50000,
                roiEvolutionData: [[0, -1.0], [25000, -0.2], [50000, 0.1]]
            },
            { 
                maxInferences: 75000,
                roiEvolutionData: [[0, -1.2], [37500, -0.1], [75000, 0.2]]
            },
            { 
                maxInferences: 100000,
                roiEvolutionData: [[0, -0.8], [50000, 0.0], [100000, 0.3]]
            }
        ];

        for (const update of updates) {
            await wrapper.setProps({ chartData: update });
            await flushPromises();
        }

        // Should have called setOption for each update plus initial
        expect(mockChartInstance.setOption.mock.calls.length).toBe(updates.length + 1);
        
        // Should not have created multiple chart instances
        expect(echarts.init.mock.calls.length).toBe(1);
    });

    it('handles empty or invalid chart data gracefully', async () => {
        const emptyData = {
            maxInferences: 0,
            roiEvolutionData: []
        };

        await wrapper.setProps({ chartData: emptyData });
        await flushPromises();

        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.xAxis.max).toBe(0);
        expect(chartOptions.series[0].data).toEqual([]);
        expect(mockChartInstance.setOption).toHaveBeenCalled();
    });

    it('sets correct axis naming and positioning', () => {
        expect(wrapper.vm.chartOptions.xAxis.nameLocation).toBe('middle');
        expect(wrapper.vm.chartOptions.xAxis.nameGap).toBe(30);
        expect(wrapper.vm.chartOptions.yAxis.nameLocation).toBe('middle');
        expect(wrapper.vm.chartOptions.yAxis.nameGap).toBe(35);
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

    it('handles missing chart container gracefully', async () => {
        // Mock refs to return null
        wrapper.vm.$refs.chartContainer = null;
        
        // This should not throw an error
        wrapper.vm.initChart();
        
        // Chart should remain the original instance when container is not available
        expect(wrapper.vm.chart).toStrictEqual(mockChartInstance);
    });

    it('calls updateChart on initChart', async () => {
        const updateChartSpy = vi.spyOn(wrapper.vm, 'updateChart');
        
        wrapper.vm.initChart();
        await flushPromises();
        
        expect(updateChartSpy).toHaveBeenCalled();
    });
});
