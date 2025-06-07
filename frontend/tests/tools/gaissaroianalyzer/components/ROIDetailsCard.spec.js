import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import ROIDetailsCard from '@/tools/gaissaroianalyzer/components/ROIDetailsCard.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';

// Mock FontAwesome
vi.mock('@fortawesome/vue-fontawesome', () => ({
    FontAwesomeIcon: {
        name: 'FontAwesomeIcon',
        template: '<i class="fa-icon" :class="icon"></i>',
        props: ['icon']
    }
}));

describe('ROIDetailsCard.vue', () => {
    let wrapper;
    
    const mockFormatNumber = vi.fn((value) => {
        if (value === null || value === undefined || isNaN(value)) return 'N/A';
        return value.toFixed(2);
    });

    const mockCostMetric = {
        metric_name: 'Incurred Cost',
        total_new_cost: 1000.50,
        total_baseline_cost: 1500.75,
        new_cost_per_inference: 0.001,
        baseline_cost_per_inference: 0.0015,
        implementation_cost: 500.25,
        energy_cost_rate: 0.12,
        total_savings: 500.25,
        break_even_inferences: 500000,
        num_inferences: 1000000,
        roi_percentage: 25.5,
        infinite_roi_percentage: 33.33
    };

    beforeEach(() => {
        vi.clearAllMocks();
        
        wrapper = mount(ROIDetailsCard, {
            props: {
                costMetric: mockCostMetric,
                formatNumber: mockFormatNumber,
                tacticName: 'Quantization',
                showTitle: true,
                columnCount: 2
            },
            global: {
                plugins: [ElementPlus, i18n],
                components: {
                    'font-awesome-icon': {
                        name: 'FontAwesomeIcon',
                        template: '<i class="fa-icon" :class="icon"></i>',
                        props: ['icon']
                    }
                }
            }
        });
    });

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    });

    describe('Component Initialization', () => {
        it('has correct default props', () => {
            const componentProps = wrapper.vm.$options.props;
            expect(componentProps.tacticName.default).toBe('');
            expect(componentProps.showTitle.default).toBe(false);
            expect(componentProps.columnCount.default).toBe(2);
        });
    });

    describe('Component Rendering', () => {
        it('renders title when showTitle is true', () => {
            expect(wrapper.find('h3').exists()).toBe(true);
            expect(wrapper.find('h3').text()).toBe('Incurred Cost');
        });

        it('does not render title when showTitle is false', async () => {
            await wrapper.setProps({ showTitle: false });
            expect(wrapper.find('h3').exists()).toBe(false);
        });

        it('passes correct column count to el-descriptions', () => {
            const descriptions = wrapper.findComponent({ name: 'el-descriptions' });
            expect(descriptions.props('column')).toBe(2);
        });
    });

    describe('Data Display', () => {
        it('calls formatNumber function for numeric values', () => {
            expect(mockFormatNumber).toHaveBeenCalledWith(mockCostMetric.total_new_cost);
            expect(mockFormatNumber).toHaveBeenCalledWith(mockCostMetric.total_baseline_cost);
            expect(mockFormatNumber).toHaveBeenCalledWith(mockCostMetric.roi_percentage);
        });

        it('displays break-even point correctly', () => {
            const text = wrapper.text();
            expect(text).toContain('500000');
        });

        it('displays ROI percentage with correct number of inferences', () => {
            const text = wrapper.text();
            expect(text).toContain('1,000,000');
        });
    });

    describe('Recommendation Logic', () => {
        it('shows positive recommendation when break-even is finite', () => {
            expect(wrapper.find('.recommendation.positive').exists()).toBe(true);
            expect(wrapper.find('.recommendation-icon.positive').exists()).toBe(true);
        });

        it('shows negative recommendation when break-even is infinite', async () => {
            const infiniteCostMetric = {
                ...mockCostMetric,
                break_even_inferences: 'Infinity'
            };
            
            await wrapper.setProps({ costMetric: infiniteCostMetric });
            
            expect(wrapper.find('.recommendation.negative').exists()).toBe(true);
            expect(wrapper.find('.recommendation-icon.negative').exists()).toBe(true);
        });
    });
});
