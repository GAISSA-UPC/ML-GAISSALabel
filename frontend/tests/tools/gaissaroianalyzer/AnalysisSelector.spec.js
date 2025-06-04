import { mount } from '@vue/test-utils';
import AnalysisSelector from '@/tools/gaissaroianalyzer/components/AnalysisSelector.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import flushPromises from 'flush-promises';
import modelArchitectures from '@/tools/gaissaroianalyzer/services/modelArchitectures';
import mlTactics from '@/tools/gaissaroianalyzer/services/mlTactics';
import tacticParameters from '@/tools/gaissaroianalyzer/services/tacticParameters';
import roiAnalyses from '@/tools/gaissaroianalyzer/services/roiAnalyses';
import { formatData } from '@/utils';

// Mock the services and the formatData utility
vi.mock('@/tools/gaissaroianalyzer/services/modelArchitectures');
vi.mock('@/tools/gaissaroianalyzer/services/mlTactics');
vi.mock('@/tools/gaissaroianalyzer/services/tacticParameters');
vi.mock('@/tools/gaissaroianalyzer/services/roiAnalyses');
vi.mock('@/utils', () => ({
    formatData: vi.fn().mockImplementation(date => `Formatted: ${date}`)
}));

describe('AnalysisSelector.vue', () => {
    let wrapper;
    let mockRouter;
    
    const defaultProps = {
        analysisType: 'calculation',
        repositoryTitle: 'Test Repository',
        repositoryDescription: 'Test Repository Description',
        analysisSelectionDescription: 'Select an analysis',
        comparisonMode: false
    };

    // Sample data for mocks
    const mockModelArchitectures = [
        { id: 'arch1', name: 'Architecture 1' },
        { id: 'arch2', name: 'Architecture 2' }
    ];

    const mockMlTactics = [
        { id: 'tactic1', name: 'Tactic 1' },
        { id: 'tactic2', name: 'Tactic 2' }
    ];

    const mockTacticParameters = [
        { id: 'param1', name: 'Parameter 1', value: '10' },
        { id: 'param2', name: 'Parameter 2', value: '20' }
    ];

    const mockExperiments = [
        { id: 'exp1', dateRegistration: '2025-01-01' },
        { id: 'exp2', source: { title: 'Research Paper Title' } }
    ];

    beforeEach(() => {
        // Set up mocks
        modelArchitectures.list.mockResolvedValue({ data: mockModelArchitectures });
        mlTactics.getCompatibleTacticsWithArchitecture.mockResolvedValue({ data: mockMlTactics });
        tacticParameters.list.mockResolvedValue({ data: mockTacticParameters });
        roiAnalyses.list.mockResolvedValue({ data: mockExperiments });

        mockRouter = { push: vi.fn() };

        // Mount component
        wrapper = mount(AnalysisSelector, {
            global: {
                plugins: [ElementPlus, i18n],
                mocks: { $router: mockRouter }
            },
            props: defaultProps
        });
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it('renders titles and descriptions correctly based on props', async () => {
        await flushPromises(); // Wait for component to load data
        
        expect(wrapper.find('h1').text()).toContain('GAISSA ROI Analyzer');
        expect(wrapper.find('h2').text()).toBe('Test Repository');
        expect(wrapper.find('p.description').text()).toBe('Test Repository Description');
    });

    it('loads model architectures on mount', async () => {
        await flushPromises();
        
        expect(modelArchitectures.list).toHaveBeenCalledWith({ analysis_type: 'calculation' });
        
        // Check that options are rendered
        const options = wrapper.findAll('.el-select:first-of-type .el-option');
        expect(wrapper.vm.modelArchitectures).toEqual(mockModelArchitectures);
    });

    it('shows and hides sections based on selections', async () => {
        await flushPromises();
        
        // Initially, only model architecture section should be visible
        expect(wrapper.findAll('h3.section-title').length).toBe(1);
        expect(wrapper.findAll('h3.section-title')[0].text()).toContain('Model Architecture');
        
        // Select a model architecture
        await wrapper.setData({ selectedModelArchitecture: 'arch1' });
        await wrapper.vm.onModelArchitectureChange();
        await flushPromises();
        
        // Now ML Tactic section should be visible
        expect(wrapper.findAll('h3.section-title').length).toBe(2);
        expect(wrapper.findAll('h3.section-title')[1].text()).toContain('ML Tactic');
        
        // Select an ML Tactic
        await wrapper.setData({ selectedMlTactic: 'tactic1' });
        await wrapper.vm.onMlTacticChange();
        await flushPromises();
        
        // Now Tactic Parameter section should be visible
        expect(wrapper.findAll('h3.section-title').length).toBe(3);
        expect(wrapper.findAll('h3.section-title')[2].text()).toContain('Tactic Parameter');
        
        // Select a Tactic Parameter
        await wrapper.setData({ selectedTacticParameter: 'param1' });
        await wrapper.vm.onTacticParameterChange();
        await flushPromises();
        
        // Now Analysis section should be visible
        expect(wrapper.findAll('h3.section-title').length).toBe(4);
        expect(wrapper.findAll('h3.section-title')[3].text()).toContain('Analysis');
    });

    it('loads ML tactics when a model architecture is selected', async () => {
        await flushPromises();
        
        await wrapper.setData({ selectedModelArchitecture: 'arch1' });
        await wrapper.vm.onModelArchitectureChange();
        
        expect(mlTactics.getCompatibleTacticsWithArchitecture).toHaveBeenCalledWith('arch1', { analysis_type: 'calculation' });
        expect(wrapper.vm.mlTactics).toEqual(mockMlTactics);
    });

    it('loads tactic parameters when an ML tactic is selected', async () => {
        await flushPromises();
        
        await wrapper.setData({ 
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1'
        });
        await wrapper.vm.onMlTacticChange();
        
        expect(tacticParameters.list).toHaveBeenCalledWith('tactic1', { 
            model_architecture: 'arch1',
            analysis_type: 'calculation'
        });
        expect(wrapper.vm.tacticParameters).toEqual(mockTacticParameters);
    });

    it('loads experiments when a tactic parameter is selected', async () => {
        await flushPromises();
        
        await wrapper.setData({ 
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1'
        });
        await wrapper.vm.onTacticParameterChange();
        
        expect(roiAnalyses.list).toHaveBeenCalledWith({ 
            model_architecture: 'arch1',
            tactic: 'tactic1',
            tactic_parameter_option: 'param1',
            analysis_type: 'calculation'
        });
        expect(wrapper.vm.experiments).toEqual(mockExperiments);
    });

    it('disables the action button until form is valid', async () => {
        await flushPromises();
        
        // Initially button should be disabled
        let button = wrapper.find('.action-button');
        expect(button.attributes('disabled')).toBeDefined();
        
        // Complete form
        await wrapper.setData({
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1',
            selectedExperiment: 'exp1'
        });
        
        await flushPromises();
        
        // Button should be enabled now
        button = wrapper.find('.action-button');
        expect(button.attributes('disabled')).toBeUndefined();
    });

    it('formats experiment labels correctly based on analysis type', async () => {
        await flushPromises();
        
        // For calculation type
        wrapper.setProps({ analysisType: 'calculation' });
        const calcLabel = wrapper.vm.formatLabel(mockExperiments[0]);
        expect(formatData).toHaveBeenCalledWith('2025-01-01');
        expect(calcLabel).toContain('Formatted:');
        
        // Need to mount a new instance with research type to properly test this case
        const researchWrapper = mount(AnalysisSelector, {
            global: {
                plugins: [ElementPlus, i18n],
                mocks: { $router: mockRouter }
            },
            props: {
                ...defaultProps,
                analysisType: 'research'
            }
        });
        const researchLabel = researchWrapper.vm.formatLabel(mockExperiments[1]);
        expect(researchLabel).toBe('Research Paper Title');
    });

    it('emits event and navigates on analysis load in normal mode', async () => {
        await flushPromises();
        
        await wrapper.setData({
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1',
            selectedExperiment: 'exp1'
        });
        
        await wrapper.find('.action-button').trigger('click');
        
        // Should emit event
        expect(wrapper.emitted('analysisSelected')).toBeTruthy();
        expect(wrapper.emitted('analysisSelected')[0]).toEqual(['exp1']);
        
        // Should navigate
        expect(mockRouter.push).toHaveBeenCalledWith({
            name: 'GAISSA ROI Analyzer Analysis',
            params: { id_experiment: 'exp1' }
        });
    });

    it('emits event but does not navigate in comparison mode', async () => {
        wrapper = mount(AnalysisSelector, {
            global: {
                plugins: [ElementPlus, i18n],
                mocks: { $router: mockRouter }
            },
            props: {
                ...defaultProps,
                comparisonMode: true
            }
        });
        
        await flushPromises();
        
        await wrapper.setData({
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1',
            selectedExperiment: 'exp1'
        });
        
        await wrapper.find('.action-button').trigger('click');
        
        // Should emit event
        expect(wrapper.emitted('analysisSelected')).toBeTruthy();
        expect(wrapper.emitted('analysisSelected')[0]).toEqual(['exp1']);
        
        // Should NOT navigate
        expect(mockRouter.push).not.toHaveBeenCalled();
    });

    it('shows different button text based on mode', async () => {
        // Normal mode
        await flushPromises();
        expect(wrapper.find('.action-button').text()).toBe('Load ROI Analysis');
        
        // Comparison mode
        const comparisonWrapper = mount(AnalysisSelector, {
            global: {
                plugins: [ElementPlus, i18n],
                mocks: { $router: mockRouter }
            },
            props: {
                ...defaultProps,
                comparisonMode: true
            }
        });
        
        await flushPromises();
        expect(comparisonWrapper.find('.action-button').text()).toBe('Select Analysis');
        
        // After selection in comparison mode
        await comparisonWrapper.setData({
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1',
            selectedExperiment: 'exp1',
            analysisSelected: true
        });
        
        await flushPromises();
        // Trigger a button click to make sure the text changes
        await comparisonWrapper.find('.action-button').trigger('click');
        await flushPromises();
        
        // Need to manually mock the translation since $t is used in getButtonText
        expect(comparisonWrapper.vm.getButtonText()).toBe('Analysis Selected ✓');
    });

    it('resets selection state when experiment changes', async () => {
        await flushPromises();
        
        // Set up selected state
        await wrapper.setData({
            selectedExperiment: 'exp1',
            analysisSelected: true
        });
        
        // Change experiment
        await wrapper.setData({ selectedExperiment: 'exp2' });
        
        // Selection should be reset
        expect(wrapper.vm.analysisSelected).toBe(false);
    });

    it('shows info alerts only when not in comparison mode', async () => {
        // Normal mode - should show alerts
        await flushPromises();
        expect(wrapper.findAll('.el-alert').length).toBe(1);
        
        // Comparison mode - should not show alerts
        wrapper = mount(AnalysisSelector, {
            global: {
                plugins: [ElementPlus, i18n],
                mocks: { $router: mockRouter }
            },
            props: {
                ...defaultProps,
                comparisonMode: true
            }
        });
        
        await flushPromises();
        expect(wrapper.findAll('.el-alert').length).toBe(0);
    });

    it('resets dependent fields when a parent selection changes', async () => {
        await flushPromises();
        
        // Set up all fields
        await wrapper.setData({
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1',
            selectedExperiment: 'exp1',
            mlTactics: mockMlTactics,
            tacticParameters: mockTacticParameters,
            experiments: mockExperiments
        });
        
        // Change architecture - should reset ML tactics and below
        await wrapper.vm.onModelArchitectureChange();
        
        expect(wrapper.vm.selectedMlTactic).toBeNull();
        expect(wrapper.vm.selectedTacticParameter).toBeNull();
        expect(wrapper.vm.selectedExperiment).toBeNull();
        
        // Set up again and change ML tactic
        await wrapper.setData({
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1',
            selectedExperiment: 'exp1',
            mlTactics: mockMlTactics,
            tacticParameters: mockTacticParameters,
            experiments: mockExperiments
        });
        
        await wrapper.vm.onMlTacticChange();
        
        // Should reset tactic parameter and below
        expect(wrapper.vm.selectedTacticParameter).toBeNull();
        expect(wrapper.vm.selectedExperiment).toBeNull();
        expect(wrapper.vm.selectedMlTactic).not.toBeNull();

        // Set up again and change tactic parameter
        await wrapper.setData({
            selectedModelArchitecture: 'arch1',
            selectedMlTactic: 'tactic1',
            selectedTacticParameter: 'param1',
            selectedExperiment: 'exp1',
            mlTactics: mockMlTactics,
            tacticParameters: mockTacticParameters,
            experiments: mockExperiments
        });

        await wrapper.vm.onTacticParameterChange();

        // Should reset experiment
        expect(wrapper.vm.selectedExperiment).toBeNull();
        expect(wrapper.vm.selectedTacticParameter).not.toBeNull();
    });
});