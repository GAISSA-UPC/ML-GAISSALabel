import { mount } from '@vue/test-utils';
import MetricCard from '@/tools/gaissaroianalyzer/components/MetricCard.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import { library } from '@fortawesome/fontawesome-svg-core';
import { 
    faDownLong, 
    faUpLong, 
    faEquals 
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import flushPromises from 'flush-promises';

// Add required FontAwesome icons
library.add(faDownLong, faUpLong, faEquals);

describe('MetricCard.vue', () => {
    let wrapper;
    
    // Sample data for the component
    const defaultProps = {
        metric: {
            metric_name: 'Energy Consumption',
            description: 'Total energy used during model inference',
            baseline_value: 100.5,
            new_expected_value: 75.2,
            expected_reduction_percent: 25.2,
            unit: 'kWh',
            higher_is_better: false
        },
        formatNumber: (num) => num.toLocaleString('en-US', { maximumFractionDigits: 2 }),
        forceMobile: false
    };

    const higherIsBetterMetric = {
        metric_name: 'Model Accuracy',
        description: 'Accuracy percentage of the model predictions',
        baseline_value: 85.5,
        new_expected_value: 92.3,
        expected_reduction_percent: -7.95,
        unit: '%',
        higher_is_better: true
    };

    beforeEach(() => {
        wrapper = mount(MetricCard, {
            props: defaultProps,
            global: {
                plugins: [ElementPlus, i18n],
                components: { 'font-awesome-icon': FontAwesomeIcon }
            }
        });
    });

    describe('Component Rendering', () => {
        it('renders the component with correct structure', () => {
            expect(wrapper.find('.metric-card').exists()).toBe(true);
            expect(wrapper.find('.change-indicator').exists()).toBe(true);
            expect(wrapper.find('.metric-data').exists()).toBe(true);
            expect(wrapper.find('.metric-info').exists()).toBe(true);
            expect(wrapper.find('.metric-comparison').exists()).toBe(true);
        });

        it('displays metric title and description correctly', () => {
            const title = wrapper.find('.metric-title');
            const description = wrapper.find('.metric-description');
            
            expect(title.exists()).toBe(true);
            expect(title.text()).toBe('Energy Consumption');
            expect(description.exists()).toBe(true);
            expect(description.text()).toBe('Total energy used during model inference');
        });

        it('displays optimized and baseline values correctly', () => {
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            const baselineValue = wrapper.find('.value-container.baseline .value');
            
            expect(optimizedValue.text()).toContain('75.2');
            expect(optimizedValue.text()).toContain('kWh');
            expect(baselineValue.text()).toContain('100.5');
            expect(baselineValue.text()).toContain('kWh');
        });

        it('displays correct percentage reduction', () => {
            const percentage = wrapper.find('.change-percentage');
            expect(percentage.text()).toBe('25.2%');
        });

        it('applies forceMobile class when prop is true', async () => {
            await wrapper.setProps({ forceMobile: true });
            expect(wrapper.find('.metric-card.force-mobile').exists()).toBe(true);
        });

        it('does not apply forceMobile class when prop is false', () => {
            expect(wrapper.find('.metric-card.force-mobile').exists()).toBe(false);
        });
    });

    describe('Computed Properties', () => {
        describe('calculateReductionPercent', () => {
            it('calculates reduction percentage correctly for normal values', () => {
                const expectedReduction = ((100.5 - 75.2) / 100.5) * 100;
                expect(wrapper.vm.calculateReductionPercent).toBeCloseTo(expectedReduction, 2);
            });

            it('returns 0 when baseline value is NaN', async () => {
                await wrapper.setProps({
                    metric: {
                        ...defaultProps.metric,
                        baseline_value: 'invalid'
                    }
                });
                expect(wrapper.vm.calculateReductionPercent).toBe(0);
            });

            it('returns 0 when new expected value is NaN', async () => {
                await wrapper.setProps({
                    metric: {
                        ...defaultProps.metric,
                        new_expected_value: 'invalid'
                    }
                });
                expect(wrapper.vm.calculateReductionPercent).toBe(0);
            });

            it('returns -Infinity when baseline value is 0', async () => {
                await wrapper.setProps({
                    metric: {
                        ...defaultProps.metric,
                        baseline_value: 0
                    }
                });
                expect(wrapper.vm.calculateReductionPercent).toBe(-Infinity);
            });

            it('handles negative reduction (increase) correctly', async () => {
                await wrapper.setProps({
                    metric: {
                        ...defaultProps.metric,
                        new_expected_value: 120.0
                    }
                });
                const expectedReduction = ((100.5 - 120.0) / 100.5) * 100;
                expect(wrapper.vm.calculateReductionPercent).toBeCloseTo(expectedReduction, 2);
            });
        });

        describe('isReductionPositive', () => {
            it('returns true for positive reduction when higher is NOT better', () => {
                // Default metric has higher_is_better: false and positive reduction
                expect(wrapper.vm.isReductionPositive).toBe(true);
            });

            it('returns false for negative reduction when higher is NOT better', async () => {
                await wrapper.setProps({
                    metric: {
                        ...defaultProps.metric,
                        expected_reduction_percent: -10.5
                    }
                });
                expect(wrapper.vm.isReductionPositive).toBe(false);
            });

            it('returns true for negative reduction when higher IS better', async () => {
                await wrapper.setProps({
                    metric: higherIsBetterMetric
                });
                expect(wrapper.vm.isReductionPositive).toBe(true);
            });

            it('returns false for positive reduction when higher IS better', async () => {
                await wrapper.setProps({
                    metric: {
                        ...higherIsBetterMetric,
                        expected_reduction_percent: 5.0
                    }
                });
                expect(wrapper.vm.isReductionPositive).toBe(false);
            });

            it('returns true for zero reduction regardless of higher_is_better', async () => {
                await wrapper.setProps({
                    metric: {
                        ...defaultProps.metric,
                        baseline_value: 100,
                        new_expected_value: 100,
                        expected_reduction_percent: 0
                    }
                });
                expect(wrapper.vm.isReductionPositive).toBe(true);

                await wrapper.setProps({
                    metric: {
                        ...higherIsBetterMetric,
                        baseline_value: 85.5,
                        new_expected_value: 85.5,
                        expected_reduction_percent: 0
                    }
                });
                expect(wrapper.vm.isReductionPositive).toBe(true);
            });
        });
    });

    describe('FontAwesome Icons', () => {
        it('shows down arrow for positive reduction', async () => {
            await flushPromises();
            const downArrow = wrapper.find('[data-icon="down-long"]');
            expect(downArrow.exists()).toBe(true);
        });

        it('shows up arrow for negative reduction', async () => {
            await wrapper.setProps({
                metric: {
                    ...defaultProps.metric,
                    expected_reduction_percent: -15.5
                }
            });
            await flushPromises();
            
            const upArrow = wrapper.find('[data-icon="up-long"]');
            expect(upArrow.exists()).toBe(true);
        });

        it('shows equals icon for zero reduction', async () => {
            await wrapper.setProps({
                metric: {
                    ...defaultProps.metric,
                    baseline_value: 100,
                    new_expected_value: 100,
                    expected_reduction_percent: 0
                }
            });
            await flushPromises();
            
            const equalsIcon = wrapper.find('[data-icon="equals"]');
            expect(equalsIcon.exists()).toBe(true);
        });

        it('applies positive class to arrow when reduction is positive', () => {
            const arrow = wrapper.find('.change-arrow');
            expect(arrow.classes()).toContain('positive');
        });

        it('applies negative class to arrow when reduction is negative', async () => {
            await wrapper.setProps({
                metric: {
                    ...defaultProps.metric,
                    expected_reduction_percent: -10.0
                }
            });
            
            const arrow = wrapper.find('.change-arrow');
            expect(arrow.classes()).toContain('negative');
        });
    });

    describe('Value Formatting and Display', () => {
        it('formats numbers using the provided formatNumber function', () => {
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            const baselineValue = wrapper.find('.value-container.baseline .value');
            
            expect(optimizedValue.text()).toContain('75.2');
            expect(baselineValue.text()).toContain('100.5');
        });

        it('displays units correctly', () => {
            const units = wrapper.findAll('.unit');
            units.forEach(unit => {
                expect(unit.text()).toBe('kWh');
            });
        });

        it('applies positive class to optimized value when reduction is positive', () => {
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            expect(optimizedValue.classes()).toContain('positive');
        });

        it('applies negative class to optimized value when reduction is negative', async () => {
            await wrapper.setProps({
                metric: {
                    ...defaultProps.metric,
                    expected_reduction_percent: -10.0
                }
            });
            
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            expect(optimizedValue.classes()).toContain('negative');
        });

        it('applies positive class to percentage when reduction is positive', () => {
            const percentage = wrapper.find('.change-percentage');
            expect(percentage.classes()).toContain('positive');
        });

        it('applies negative class to percentage when reduction is negative', async () => {
            await wrapper.setProps({
                metric: {
                    ...defaultProps.metric,
                    expected_reduction_percent: -10.0
                }
            });
            
            const percentage = wrapper.find('.change-percentage');
            expect(percentage.classes()).toContain('negative');
        });
    });

    describe('Edge Cases', () => {
        it('handles missing unit gracefully', async () => {
            await wrapper.setProps({
                metric: {
                    ...defaultProps.metric,
                    unit: undefined
                }
            });
            
            const units = wrapper.findAll('.unit');
            units.forEach(unit => {
                expect(unit.text()).toBe('');
            });
        });
    });

    describe('Higher is Better vs Lower is Better Logic', () => {
        it('handles "lower is better" metrics correctly', () => {
            // Default metric has higher_is_better: false (energy consumption - lower is better)
            // Positive reduction (25.2%) should be good (positive)
            expect(wrapper.vm.isReductionPositive).toBe(true);
            
            const arrow = wrapper.find('.change-arrow');
            const percentage = wrapper.find('.change-percentage');
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            
            expect(arrow.classes()).toContain('positive');
            expect(percentage.classes()).toContain('positive');
            expect(optimizedValue.classes()).toContain('positive');
        });

        it('handles "higher is better" metrics correctly', async () => {
            await wrapper.setProps({
                metric: higherIsBetterMetric
            });
            
            // For accuracy (higher is better), negative reduction (-7.95%) is actually good
            // because it means the new value is higher than baseline
            expect(wrapper.vm.isReductionPositive).toBe(true);
            
            const arrow = wrapper.find('.change-arrow');
            const percentage = wrapper.find('.change-percentage');
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            
            expect(arrow.classes()).toContain('positive');
            expect(percentage.classes()).toContain('positive');
            expect(optimizedValue.classes()).toContain('positive');
        });

        it('shows negative styling when "lower is better" metric increases', async () => {
            await wrapper.setProps({
                metric: {
                    ...defaultProps.metric,
                    new_expected_value: 120.0,
                    expected_reduction_percent: -19.4 // Increase is bad for energy consumption
                }
            });
            
            expect(wrapper.vm.isReductionPositive).toBe(false);
            
            const arrow = wrapper.find('.change-arrow');
            const percentage = wrapper.find('.change-percentage');
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            
            expect(arrow.classes()).toContain('negative');
            expect(percentage.classes()).toContain('negative');
            expect(optimizedValue.classes()).toContain('negative');
        });

        it('shows negative styling when "higher is better" metric decreases', async () => {
            await wrapper.setProps({
                metric: {
                    ...higherIsBetterMetric,
                    new_expected_value: 80.0,
                    expected_reduction_percent: 6.4 // Decrease is bad for accuracy
                }
            });
            
            expect(wrapper.vm.isReductionPositive).toBe(false);
            
            const arrow = wrapper.find('.change-arrow');
            const percentage = wrapper.find('.change-percentage');
            const optimizedValue = wrapper.find('.value-container.optimized .value');
            
            expect(arrow.classes()).toContain('negative');
            expect(percentage.classes()).toContain('negative');
            expect(optimizedValue.classes()).toContain('negative');
        });
    });

    describe('Responsive Design', () => {
        it('applies force-mobile class and related styles when forceMobile is true', async () => {
            await wrapper.setProps({ forceMobile: true });
            
            const card = wrapper.find('.metric-card');
            expect(card.classes()).toContain('force-mobile');
        });

        it('maintains proper structure in mobile mode', async () => {
            await wrapper.setProps({ forceMobile: true });
            
            // Component should still render all essential elements
            expect(wrapper.find('.change-indicator').exists()).toBe(true);
            expect(wrapper.find('.metric-info').exists()).toBe(true);
            expect(wrapper.find('.values-comparison').exists()).toBe(true);
            expect(wrapper.find('.value-container.optimized').exists()).toBe(true);
            expect(wrapper.find('.value-container.baseline').exists()).toBe(true);
        });
    });
});
