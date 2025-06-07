import { mount } from '@vue/test-utils';
import { vi } from 'vitest';
import ROIAnalysisComponent from '@/tools/gaissaroianalyzer/components/ROIAnalysisComponent.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import flushPromises from 'flush-promises';

// Mock FontAwesome
vi.mock('@fortawesome/vue-fontawesome', () => ({
    FontAwesomeIcon: {
        name: 'FontAwesomeIcon',
        template: '<i class="fa-icon"></i>'
    }
}));

// Mock services
vi.mock('@/tools/gaissaroianalyzer/services/roiAnalyses', () => ({
    default: {
        getAnalysis: vi.fn()
    }
}));

vi.mock('@/tools/gaissaroianalyzer/services/mlTactics', () => ({
    default: {
        getById: vi.fn()
    }
}));

// Mock child components
vi.mock('@/tools/gaissaroianalyzer/components/ModelInformationCard.vue', () => ({
    default: {
        name: 'ModelInformationCard',
        template: '<div data-testid="model-information-card">ModelInformationCard</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/SourceInformationCard.vue', () => ({
    default: {
        name: 'SourceInformationCard',
        template: '<div data-testid="source-information-card">SourceInformationCard</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/TacticSourcesCard.vue', () => ({
    default: {
        name: 'TacticSourcesCard',
        template: '<div data-testid="tactic-sources-card">TacticSourcesCard</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/MetricsRadialChart.vue', () => ({
    default: {
        name: 'MetricsRadialChart',
        template: '<div data-testid="metrics-radial-chart">MetricsRadialChart</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/MetricCard.vue', () => ({
    default: {
        name: 'MetricCard',
        template: '<div data-testid="metric-card">MetricCard</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/ROIDetailsCard.vue', () => ({
    default: {
        name: 'ROIDetailsCard',
        template: '<div data-testid="roi-details-card">ROIDetailsCard</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/ROIEvolutionChart.vue', () => ({
    default: {
        name: 'ROIEvolutionChart',
        template: '<div data-testid="roi-evolution-chart">ROIEvolutionChart</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/IncomeCostsChart.vue', () => ({
    default: {
        name: 'IncomeCostsChart',
        template: '<div data-testid="income-costs-chart">IncomeCostsChart</div>'
    }
}));

vi.mock('@/tools/gaissaroianalyzer/components/EmissionsReductionCard.vue', () => ({
    default: {
        name: 'EmissionsReductionCard',
        template: '<div data-testid="emissions-reduction-card">EmissionsReductionCard</div>'
    }
}));

describe('ROIAnalysisComponent.vue', () => {
    let wrapper;

    // Sample analysis data
    const calculationAnalysisData = {
        id: 123,
        model_architecture_name: 'BERT Base',
        analysis_type: 'calculation',
        tactic_parameter_option_details: {
            tactic: 1,
            tactic_name: 'Quantization',
            name: 'Bit Width',
            value: '8-bit'
        },
        dateRegistration: '2023-11-21T17:01:34.781082Z',
        country: {
            name: 'Spain',
            country_code: 'ES'
        },
        source: null,
        metrics_analysis: [
            {
                metric_name: 'Power Consumption',
                baseline_value: 100,
                new_expected_value: 75,
                unit: 'W',
                expected_reduction_percent: 25,
                cost_savings: {
                    total_baseline_cost: 1000,
                    total_new_cost: 750,
                    baseline_cost_per_inference: 0.001,
                    new_cost_per_inference: 0.00075,
                    implementation_cost: 50,
                    energy_cost_rate: 0.1,
                    total_savings: 250,
                    break_even_inferences: 200,
                    roi: 0.5,
                    infinite_roi: 0.6,
                    num_inferences: 1000000,
                    inferences_carbon_emissions: {
                        baseline_co2_grams: 500,
                        new_co2_grams: 375,
                        co2_reduction_grams: 125,
                        co2_reduction_percent: 25
                    }
                },
                roi_evolution_chart_data: [
                    { inferences: 100, roi: 10 },
                    { inferences: 200, roi: 25 },
                    { inferences: 500, roi: 50 }
                ]
            }
        ]
    };

    const researchAnalysisData = {
        id: 456,
        model_architecture_name: 'GPT-3.5',
        analysis_type: 'research',
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
        },
        metrics_analysis: []
    };

    const tacticSourcesData = [
        {
            id: 1,
            title: 'Quantization Techniques Paper',
            authors: ['Author A', 'Author B'],
            year: 2023
        }
    ];

    beforeEach(async () => {
        // Reset mocks
        vi.clearAllMocks();
        
        // Setup mock imports - get the mocked modules
        const roiAnalyses = await import('@/tools/gaissaroianalyzer/services/roiAnalyses');
        const mlTactics = await import('@/tools/gaissaroianalyzer/services/mlTactics');
        
        // Default successful mocks
        roiAnalyses.default.getAnalysis.mockResolvedValue(calculationAnalysisData);
        mlTactics.default.getById.mockResolvedValue({ sources: tacticSourcesData });

        wrapper = mount(ROIAnalysisComponent, {
            props: {
                analysisId: 123
            },
            global: {
                plugins: [ElementPlus, i18n],
                components: {
                    'font-awesome-icon': {
                        name: 'font-awesome-icon',
                        template: '<i class="fa-icon" :data-icon="icon"></i>',
                        props: ['icon']
                    }
                },
                stubs: {
                    'font-awesome-icon': {
                        name: 'font-awesome-icon',
                        template: '<i class="fa-icon" :data-icon="icon"></i>',
                        props: ['icon']
                    }
                }
            }
        });
        
        // Wait for component to load data
        await flushPromises();
    });

    afterEach(() => {
        wrapper?.unmount();
    });

    describe('Component Initialization', () => {
        it('renders the component with correct structure', () => {
            expect(wrapper.find('.roi-analysis-component').exists()).toBe(true);
            expect(wrapper.find('.export-button-container').exists()).toBe(true);
            expect(wrapper.findComponent({ name: 'el-row' }).exists()).toBe(true);
        });

        it('has correct default props', () => {
            expect(wrapper.vm.analysisId).toBe(123);
            expect(wrapper.vm.showExportButton).toBe(true);
            expect(wrapper.vm.containerId).toBe('roi-analysis-container');
            expect(wrapper.vm.forceMobile).toBe(false);
        });

        it('has correct initial data before loading', () => {
            // Create a wrapper without waiting for data loading to test initial state
            const freshWrapper = mount(ROIAnalysisComponent, {
                props: { analysisId: 123 },
                global: {
                    plugins: [ElementPlus, i18n],
                    components: {
                        'font-awesome-icon': {
                            name: 'font-awesome-icon',
                            template: '<i class="fa-icon" :data-icon="icon"></i>',
                            props: ['icon']
                        }
                    }
                }
            });
            
            // Test the component's initial data state (before API calls complete)
            expect(freshWrapper.vm.analysisData).toBeNull();
            expect(freshWrapper.vm.tacticSources).toEqual([]);
            expect(freshWrapper.vm.showVisualMetrics).toBe(true);
            expect(freshWrapper.vm.pdfGenerating).toBe(false);
            expect(freshWrapper.vm.inferenceCount).toBe(100000000);
            
            freshWrapper.unmount();
        });

        it('applies force-mobile class when forceMobile prop is true', async () => {
            await wrapper.setProps({ forceMobile: true });
            expect(wrapper.find('.roi-analysis-component.force-mobile').exists()).toBe(true);
        });
    });

    describe('Export Button Functionality', () => {
        it('shows export button when showExportButton is true', () => {
            expect(wrapper.find('.export-button-container').exists()).toBe(true);
            expect(wrapper.find('.export-button').exists()).toBe(true);
        });

        it('hides export button when showExportButton is false', async () => {
            await wrapper.setProps({ showExportButton: false });
            expect(wrapper.find('.export-button-container').exists()).toBe(false);
        });

        it('shows PDF icon and correct text in export button', () => {
            const exportButton = wrapper.find('.export-button');
            expect(exportButton.exists()).toBe(true);
            expect(exportButton.text()).toContain('Generate PDF Report');
            // Check for the mocked fa-icon class
            expect(wrapper.find('.fa-icon').exists()).toBe(true);
        });
    });

    describe('Data Loading', () => {
        it('calls loadAnalysisData when analysisId changes', async () => {
            const spy = vi.spyOn(wrapper.vm, 'loadAnalysisData');
            await wrapper.setProps({ analysisId: 456 });
            expect(spy).toHaveBeenCalled();
        });

        it('loads analysis data on component mount', async () => {
            await flushPromises();
            const roiAnalyses = await import('@/tools/gaissaroianalyzer/services/roiAnalyses');
            expect(roiAnalyses.default.getAnalysis).toHaveBeenCalledWith(123, { num_inferences: 100000000 });
        });

        it('loads tactic sources for calculation type analysis', async () => {
            await flushPromises();
            const mlTactics = await import('@/tools/gaissaroianalyzer/services/mlTactics');
            expect(mlTactics.default.getById).toHaveBeenCalledWith(1);
        });

        it('does not load tactic sources for research type analysis', async () => {
            const roiAnalyses = await import('@/tools/gaissaroianalyzer/services/roiAnalyses');
            const mlTactics = await import('@/tools/gaissaroianalyzer/services/mlTactics');
            
            // Clear previous calls
            vi.clearAllMocks();
            
            // Setup mocks for research analysis
            roiAnalyses.default.getAnalysis.mockResolvedValue(researchAnalysisData);
            
            // Create new wrapper with research data
            const researchWrapper = mount(ROIAnalysisComponent, {
                props: { analysisId: 456 },
                global: {
                    plugins: [ElementPlus, i18n],
                    components: {
                        'font-awesome-icon': {
                            name: 'FontAwesomeIcon',
                            template: '<i class="fa-icon"></i>',
                            props: ['icon']
                        }
                    }
                }
            });
            
            await flushPromises();
            
            // Since research analysis has no tactic field, it shouldn't try to load tactic sources
            expect(mlTactics.default.getById).not.toHaveBeenCalled();
            
            researchWrapper.unmount();
        });
    });

    describe('Computed Properties', () => {
        beforeEach(async () => {
            await flushPromises();
        });

        describe('isResearchAnalysis', () => {
            it('returns false for calculation type analysis', () => {
                expect(wrapper.vm.isResearchAnalysis).toBe(false);
            });

            it('returns true for research type analysis', async () => {
                wrapper.vm.analysisData = researchAnalysisData;
                await wrapper.vm.$nextTick();
                expect(wrapper.vm.isResearchAnalysis).toBe(true);
            });
        });

        describe('sliderInferenceCount', () => {
            it('returns inference count when below max', () => {
                wrapper.vm.inferenceCount = 50000000;
                expect(wrapper.vm.sliderInferenceCount).toBe(50000000);
            });

            it('returns max value when inference count exceeds max', () => {
                wrapper.vm.inferenceCount = 2000000000;
                expect(wrapper.vm.sliderInferenceCount).toBe(1000000000);
            });

            it('sets inference count when setter is called', () => {
                wrapper.vm.sliderInferenceCount = 75000000;
                expect(wrapper.vm.inferenceCount).toBe(75000000);
            });
        });

        describe('costMetricsResults', () => {
            it('filters metrics with cost savings', () => {
                expect(wrapper.vm.costMetricsResults).toHaveLength(1);
                expect(wrapper.vm.costMetricsResults[0].metric_name).toBe('Incurred Cost');
            });
        });

        describe('emissionsData', () => {
            it('returns null when no cost metrics results', () => {
                wrapper.vm.analysisData = { metrics_analysis: [] };
                expect(wrapper.vm.emissionsData).toBeNull();
            });

            it('returns emissions data when available', () => {
                const emissionsData = wrapper.vm.emissionsData;
                expect(emissionsData).toEqual({
                    baseline_co2_grams: 500,
                    new_co2_grams: 375,
                    co2_reduction_grams: 125,
                    co2_reduction_percent: 25
                });
            });
        });
    });

    describe('Methods', () => {
        describe('calculateCostReductionPercent', () => {
            it('calculates correct percentage for valid inputs', () => {
                const result = wrapper.vm.calculateCostReductionPercent(1000, 750);
                expect(result).toBe('25.00');
            });

            it('returns 0 for non-numeric inputs', () => {
                expect(wrapper.vm.calculateCostReductionPercent('invalid', 750)).toBe(0);
                expect(wrapper.vm.calculateCostReductionPercent(1000, 'invalid')).toBe(0);
            });

            it('returns -Infinity when baseline cost is zero', () => {
                const result = wrapper.vm.calculateCostReductionPercent(0, 100);
                expect(result).toBe(-Infinity);
            });

            it('handles negative reduction (cost increase)', () => {
                const result = wrapper.vm.calculateCostReductionPercent(750, 1000);
                expect(result).toBe('-33.33');
            });
        });

        describe('formatNumber', () => {
            it('returns "N/A" for null, undefined, or NaN', () => {
                expect(wrapper.vm.formatNumber(null)).toBe('N/A');
                expect(wrapper.vm.formatNumber(undefined)).toBe('N/A');
                expect(wrapper.vm.formatNumber(NaN)).toBe('N/A');
            });

            it('formats billions correctly', () => {
                expect(wrapper.vm.formatNumber(1500000000)).toBe('1.5B');
            });

            it('formats millions correctly', () => {
                expect(wrapper.vm.formatNumber(2500000)).toBe('2.5M');
            });

            it('formats thousands correctly', () => {
                expect(wrapper.vm.formatNumber(1500)).toBe('1.5K');
            });

            it('uses scientific notation for very small values', () => {
                const result = wrapper.vm.formatNumber(0.000001);
                expect(result).toMatch(/e/);
            });
        });

        describe('getDescriptionsColumnCount', () => {
            it('returns 2 for desktop width', () => {
                Object.defineProperty(window, 'innerWidth', {
                    writable: true,
                    configurable: true,
                    value: 1200
                });
                expect(wrapper.vm.getDescriptionsColumnCount()).toBe(2);
            });

            it('returns 1 for mobile width', () => {
                Object.defineProperty(window, 'innerWidth', {
                    writable: true,
                    configurable: true,
                    value: 600
                });
                expect(wrapper.vm.getDescriptionsColumnCount()).toBe(1);
            });
        });

        describe('updateInferences', () => {
            it('ensures minimum inference count of 10000', async () => {
                wrapper.vm.inferenceCount = 5000;
                await wrapper.vm.updateInferences();
                expect(wrapper.vm.inferenceCount).toBe(10000);
            });

            it('calls getAnalysis with new inference count', async () => {
                wrapper.vm.inferenceCount = 50000000;
                await wrapper.vm.updateInferences();
                const roiAnalyses = await import('@/tools/gaissaroianalyzer/services/roiAnalyses');
                expect(roiAnalyses.default.getAnalysis).toHaveBeenCalledWith(123, { num_inferences: 50000000 });
            });
        });

        describe('updateInferencesFromSlider', () => {
            it('updates inference count and calls updateInferences', async () => {
                const updateInferencesSpy = vi.spyOn(wrapper.vm, 'updateInferences').mockResolvedValue();
                await wrapper.vm.updateInferencesFromSlider(75000000);
                
                expect(wrapper.vm.inferenceCount).toBe(75000000);
                expect(updateInferencesSpy).toHaveBeenCalled();
            });
        });
    });

    describe('Component Rendering Based on Data', () => {
        beforeEach(async () => {
            await flushPromises();
        });

        it('renders ModelInformationCard when analysis data is available', () => {
            expect(wrapper.find('[data-testid="model-information-card"]').exists()).toBe(true);
        });

        it('shows loading placeholder when analysis data is null', async () => {
            await wrapper.setData({ analysisData: null });
            expect(wrapper.text()).toContain('Loading analysis data...');
        });

        it('renders TacticSourcesCard for calculation type analysis', () => {
            expect(wrapper.find('[data-testid="tactic-sources-card"]').exists()).toBe(true);
        });

        it('renders SourceInformationCard for research type analysis with source', async () => {
            await wrapper.setData({ analysisData: researchAnalysisData });
            expect(wrapper.find('[data-testid="source-information-card"]').exists()).toBe(true);
            expect(wrapper.find('[data-testid="tactic-sources-card"]').exists()).toBe(false);
        });

        it('renders view toggle for metrics display', () => {
            const viewToggle = wrapper.find('.view-toggle');
            expect(viewToggle.exists()).toBe(true);
            expect(wrapper.findComponent({ name: 'el-switch' }).exists()).toBe(true);
        });

        it('renders visual metrics when showVisualMetrics is true', () => {
            expect(wrapper.find('.visual-metrics-container').exists()).toBe(true);
            expect(wrapper.find('[data-testid="metric-card"]').exists()).toBe(true);
        });

        it('renders table view when showVisualMetrics is false', async () => {
            await wrapper.setData({ showVisualMetrics: false });
            expect(wrapper.findComponent({ name: 'el-table' }).exists()).toBe(true);
            expect(wrapper.find('.visual-metrics-container').exists()).toBe(false);
        });

        it('renders inference control container', () => {
            const controlContainer = wrapper.find('.inferences-control-container');
            expect(controlContainer.exists()).toBe(true);
            expect(wrapper.findComponent({ name: 'el-slider' }).exists()).toBe(true);
            expect(wrapper.findComponent({ name: 'el-input-number' }).exists()).toBe(true);
        });

        it('renders ROI evolution chart when data is available', () => {
            expect(wrapper.find('[data-testid="roi-evolution-chart"]').exists()).toBe(true);
        });

        it('renders income costs chart when data is available', () => {
            expect(wrapper.find('[data-testid="income-costs-chart"]').exists()).toBe(true);
        });

        it('renders ROI details card when cost metrics are available', () => {
            expect(wrapper.find('[data-testid="roi-details-card"]').exists()).toBe(true);
        });

        it('renders emissions section when emissions data is available', () => {
            expect(wrapper.text()).toContain('Environmental Impact');
            expect(wrapper.find('[data-testid="emissions-reduction-card"]').exists()).toBe(true);
        });
    });

    describe('Responsive Design', () => {
        it('applies mobile layout when forceMobile is true', async () => {
            await wrapper.setProps({ forceMobile: true });
            expect(wrapper.classes()).toContain('force-mobile');
        });

        it('uses correct column configuration for mobile', async () => {
            await wrapper.setProps({ forceMobile: true });
            const columns = wrapper.findAllComponents({ name: 'el-col' });
            
            // Check that some columns have 24-span for mobile
            const mobileColumns = columns.filter(col => 
                col.props('md') === 24 && col.props('lg') === 24
            );
            expect(mobileColumns.length).toBeGreaterThan(0);
        });
    });

    describe('PDF Generation', () => {
        it('shows loading state during PDF generation', async () => {
            await wrapper.setData({ pdfGenerating: true });
            const exportButton = wrapper.find('.export-button');
            
            // Check that the component's pdfGenerating state is true
            expect(wrapper.vm.pdfGenerating).toBe(true);
            
            // For ElementPlus buttons, check the component's props
            const buttonComponent = wrapper.findComponent({ name: 'el-button' });
            expect(buttonComponent.props().loading).toBe(true);
        });
    });
});
