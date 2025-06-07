import { mount } from '@vue/test-utils';
import { vi } from 'vitest';
import ModelInformationCard from '@/tools/gaissaroianalyzer/components/ModelInformationCard.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import flushPromises from 'flush-promises';

describe('ModelInformationCard.vue', () => {
    let wrapper;
    
    // Sample data for the component
    const defaultProps = {
        modelData: {
            id: 123,
            model_architecture_name: 'BERT Base',
            tactic_parameter_option_details: {
                tactic_name: 'Quantization',
                name: 'Bit Width',
                value: '8-bit'
            },
            dateRegistration: '2023-11-21T17:01:34.781082Z',
            country: {
                name: 'Spain',
                country_code: 'ES'
            },
            source: null // Calculation type
        },
        formatDate: vi.fn().mockImplementation(date => `Formatted: ${date}`)
    };

    const researchModelData = {
        id: 456,
        model_architecture_name: 'GPT-3.5',
        tactic_parameter_option_details: {
            tactic_name: 'Pruning',
            name: 'Sparsity Level',
            value: '90%'
        },
        dateRegistration: '2023-12-15T10:30:00.000Z',
        country: {
            name: 'United States',
            country_code: 'US'
        },
        source: {
            title: 'Advanced Neural Network Optimization',
            authors: ['Smith, J.', 'Doe, A.'],
            year: 2023
        }
    };

    beforeEach(() => {
        wrapper = mount(ModelInformationCard, {
            props: defaultProps,
            global: {
                plugins: [ElementPlus, i18n]
            }
        });
    });

    describe('Component Rendering', () => {
        it('renders the component with correct structure', () => {
            expect(wrapper.find('.section-title').exists()).toBe(true);
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(true);
            expect(wrapper.findComponent({ name: 'el-descriptions' }).exists()).toBe(true);

            const title = wrapper.find('.section-title');
            expect(title.exists()).toBe(true);
            expect(title.text()).toBe('Model Information');
        });

        it('displays model architecture correctly', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Model architecture');
            expect(descriptionsText).toContain('BERT Base');
        });

        it('displays ML tactic information correctly', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('ML Tactic');
            expect(descriptionsText).toContain('Quantization');
        });

        it('displays tactic parameter information correctly', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Tactic parameter');
            expect(descriptionsText).toContain('Bit Width: 8-bit');
        });

        it('displays analysis identifier correctly', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Analysis identifier');
            expect(descriptionsText).toContain('123');
        });

        it('displays registration date', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Analysis registration date');
            expect(descriptionsText).toContain('Formatted: 2023-11-21T17:01:34.781082Z');
            expect(defaultProps.formatDate).toHaveBeenCalledWith('2023-11-21T17:01:34.781082Z');
        });

        it('displays country information', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Country deploy');
            expect(descriptionsText).toContain('Spain (ES)');
        });

        it('displays analysis type correctly for calculation', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Analysis type');
            expect(descriptionsText).toContain('Calculation');
        });

        it('shows loading message when modelData is null', async () => {
            await wrapper.setProps({ modelData: null });
            
            expect(wrapper.find('p').exists()).toBe(true);
            expect(wrapper.find('p').text()).toBe('Loading model information...');
            expect(wrapper.findComponent({ name: 'el-descriptions' }).exists()).toBe(false);
        });
    });

    describe('Computed Properties', () => {
        describe('isResearch', () => {
            it('returns false when source is null or undefined (calculation type)', () => {
                expect(wrapper.vm.isResearch).toBe(false);
            });

            it('returns true when source is provided (research type)', async () => {
                await wrapper.setProps({
                    modelData: researchModelData
                });
                expect(wrapper.vm.isResearch).toBe(true);
            });
        });
    });

    describe('Analysis Type Display', () => {
        it('displays "Calculation" for calculation type analysis', () => {
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Calculation');
        });

        it('displays "Research" for research type analysis', async () => {
            await wrapper.setProps({
                modelData: researchModelData
            });
            
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Research');
        });
    });

    describe('Research Type Analysis', () => {
        beforeEach(async () => {
            await wrapper.setProps({
                modelData: researchModelData
            });
        });

        it('displays correct model architecture for research', () => {
            // Check that research model architecture is displayed
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('GPT-3.5');
        });

        it('displays correct tactic information for research', () => {
            // Check that research tactic information is displayed
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Pruning');
            expect(descriptionsText).toContain('Sparsity Level: 90%');
        });

        it('displays research analysis type', () => {
            // Check that research analysis type is displayed
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('Research');
        });

        it('displays country for research analysis', () => {
            // Check that country is displayed for research analysis
            const descriptionsText = wrapper.text();
            expect(descriptionsText).toContain('United States (US)');
        });
    });

    describe('Format Date Function', () => {
        it('calls formatDate function with correct parameter', () => {
            expect(defaultProps.formatDate).toHaveBeenCalledWith('2023-11-21T17:01:34.781082Z');
        });

        it('calls formatDate function when date changes', async () => {
            const newDate = '2024-01-15T12:00:00.000Z';
            await wrapper.setProps({
                modelData: {
                    ...defaultProps.modelData,
                    dateRegistration: newDate
                }
            });
            
            expect(defaultProps.formatDate).toHaveBeenCalledWith(newDate);
        });
    });
});
