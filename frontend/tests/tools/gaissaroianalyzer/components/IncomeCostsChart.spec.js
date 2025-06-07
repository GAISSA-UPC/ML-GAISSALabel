import { mount } from '@vue/test-utils';
import IncomeCostsChart from '@/tools/gaissaroianalyzer/components/IncomeCostsChart.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import flushPromises from 'flush-promises';
import * as echarts from 'echarts/core';

// Mock echarts modules
vi.mock('echarts/core', () => ({
    default: {
        init: vi.fn(),
        use: vi.fn(),
        graphic: {
            LinearGradient: vi.fn((x1, y1, x2, y2, colorStops) => ({
                type: 'linear',
                x: x1,
                y: y1,
                x2: x2,
                y2: y2,
                colorStops
            }))
        }
    },
    use: vi.fn(),
    init: vi.fn(),
    graphic: {
        LinearGradient: vi.fn((x1, y1, x2, y2, colorStops) => ({
            type: 'linear',
            x: x1,
            y: y1,
            x2: x2,
            y2: y2,
            colorStops
        }))
    }
}));

vi.mock('echarts/charts', () => ({
    LineChart: vi.fn()
}));

vi.mock('echarts/components', () => ({
    TitleComponent: vi.fn(),
    TooltipComponent: vi.fn(),
    GridComponent: vi.fn(),
    LegendComponent: vi.fn(),
    MarkLineComponent: vi.fn()
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
import * as echarts from 'echarts/core';
echarts.init = vi.fn(() => mockChartInstance);

describe('IncomeCostsChart.vue', () => {
    let wrapper;
    
    // Sample data for the component
    const defaultProps = {
        chartData: {
            maxInferences: 100000,
            incomeData: [
                [0, 0],
                [10000, 1000],
                [50000, 5000],
                [100000, 10000]
            ],
            costsData: [
                [0, 2000],
                [10000, 2500],
                [50000, 4500],
                [100000, 8000]
            ],
            breakEvenType: 'positive'
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

        wrapper = mount(IncomeCostsChart, {
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
        expect(wrapper.find('h2.section-title').text()).toContain('Income/Costs Chart');

        const description = wrapper.find('.chart-description');
        expect(description.exists()).toBe(true);
        expect(description.text()).toContain('This chart illustrates the evolution of income and costs');
    });

    it('displays explanation paragraphs', () => {
        const paragraphs = wrapper.findAll('p');
        
        // Check for Income/Costs explanation
        const incomeExplanation = paragraphs.find(p => p.text().includes('Income:'));
        expect(incomeExplanation).toBeDefined();
        expect(incomeExplanation.text()).toContain('how much money you would spend on inferences');

        // Check for ROI explanations
        const roiNegative = paragraphs.find(p => p.text().includes('ROI < 0:'));
        expect(roiNegative).toBeDefined();
        
        const roiZero = paragraphs.find(p => p.text().includes('ROI = 0'));
        expect(roiZero).toBeDefined();
        
        const roiPositive = paragraphs.find(p => p.text().includes('ROI > 0:'));
        expect(roiPositive).toBeDefined();
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
            ...defaultProps.chartData,
            maxInferences: 200000,
            incomeData: [[0, 0], [200000, 20000]],
            costsData: [[0, 3000], [200000, 15000]]
        };

        await wrapper.setProps({ chartData: newChartData });
        await flushPromises();

        expect(mockChartInstance.setOption).toHaveBeenCalledTimes(2); // Once on mount, once on update
    });

    it('applies green theme for positive break-even type', async () => {
        const positiveBreakEvenData = {
            ...defaultProps.chartData,
            breakEvenType: 'positive'
        };

        await wrapper.setProps({ chartData: positiveBreakEvenData });
        await flushPromises();

        // Verify that setOption was called with green color scheme
        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.series[0].lineStyle.color).toBe('green');
        expect(chartOptions.series[0].itemStyle.color).toBe('green');
    });

    it('applies orange theme for infinite break-even type', async () => {
        const infiniteBreakEvenData = {
            ...defaultProps.chartData,
            breakEvenType: 'infinite'
        };

        await wrapper.setProps({ chartData: infiniteBreakEvenData });
        await flushPromises();

        // Verify that setOption was called with orange color scheme
        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.series[0].lineStyle.color).toBe('orange');
        expect(chartOptions.series[0].itemStyle.color).toBe('orange');
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
        expect(chartOptions.series).toHaveLength(2);
        expect(chartOptions.series[0].name).toContain('Income');
        expect(chartOptions.series[1].name).toContain('Costs');
        
        // Verify axis configuration
        expect(chartOptions.xAxis.type).toBe('value');
        expect(chartOptions.yAxis.type).toBe('value');
        expect(chartOptions.xAxis.name).toContain('Number of Inferences');
        expect(chartOptions.yAxis.name).toContain('Amount (€)');
    });

    it('updates data series correctly when chartData changes', async () => {
        const newData = {
            maxInferences: 150000,
            incomeData: [[0, 0], [75000, 7500], [150000, 15000]],
            costsData: [[0, 5000], [75000, 8750], [150000, 17500]],
            breakEvenType: 'positive'
        };

        await wrapper.setProps({ chartData: newData });
        await flushPromises();

        const lastCall = mockChartInstance.setOption.mock.calls[mockChartInstance.setOption.mock.calls.length - 1];
        const chartOptions = lastCall[0];
        
        expect(chartOptions.xAxis.max).toBe(150000);
        expect(chartOptions.series[0].data).toEqual(newData.incomeData);
        expect(chartOptions.series[1].data).toEqual(newData.costsData);
    });

    it('applies formatNumber function to axis labels', () => {
        expect(wrapper.vm.chartOptions.xAxis.axisLabel.formatter).toBe(wrapper.vm.formatNumber);
        expect(wrapper.vm.chartOptions.yAxis.axisLabel.formatter).toBe(wrapper.vm.formatNumber);
    });

    it('configures legend correctly', () => {
        expect(wrapper.vm.chartOptions.legend.data).toEqual([
            expect.stringContaining('Income'),
            expect.stringContaining('Costs')
        ]);
        expect(wrapper.vm.chartOptions.legend.bottom).toBe(0);
    });

    it('handles multiple chart updates without memory leaks', async () => {
        const updates = [
            { ...defaultProps.chartData, maxInferences: 50000 },
            { ...defaultProps.chartData, maxInferences: 75000 },
            { ...defaultProps.chartData, maxInferences: 100000 }
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
});
