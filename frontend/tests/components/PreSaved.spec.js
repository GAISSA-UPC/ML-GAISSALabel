// PreSaved.spec.js
import { mount } from '@vue/test-utils';
import { formatData } from '@/utils';
import PreSaved from '@/tools/gaissalabel/components/PreSaved.vue';
import ElementPlus from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { i18n } from '@/i18n';
import models from '@/tools/gaissalabel/services/models';
import trainings from '@/tools/gaissalabel/services/trainings';
import inferencies from '@/tools/gaissalabel/services/inferencies';
import flushPromises from 'flush-promises';

// Mock controllers
vi.mock('@/tools/gaissalabel/services/models');
vi.mock('@/tools/gaissalabel/services/trainings');
vi.mock('@/tools/gaissalabel/services/inferencies');

// Mock data
export const mockModelsResponse = {
    data: [
        {
            id: 1,
            nom: "Model A",
            autor: null,
            informacio: "This is the information of Model A",
            dataCreacio: "2023-11-21T16:59:36.312175Z",
        },
        {
            id: 2,
            nom: "Model B",
            autor: "authorB",
            informacio: null,
            dataCreacio: "2023-10-29T00:00:00Z",
        },
    ],
    status: 200,
    statusText: "OK",
    headers: {
        "content-type": "application/json"
    }
};

const mockTrainingsResponse = {
    data: [
        { id: 1, dataRegistre: "2023-11-21T17:01:34.781082Z", model: 1 },
        { id: 2, dataRegistre: "2023-11-23T10:50:39.410848Z", model: 1 },
    ]
};

const mockInferenciesResponse = {
    data: [
        { id: 1, dataRegistre: "2023-11-21T17:01:34.781082Z", model: 1 },
        { id: 2, dataRegistre: "2023-11-23T10:50:39.410848Z", model: 1 },
    ]
};

describe('PreSaved.vue', () => {
    let wrapper;
    let mockRouter;

    beforeEach(() => {
        // Setup mocks
        models.list.mockResolvedValue(mockModelsResponse);
        trainings.listByModel.mockResolvedValue(mockTrainingsResponse);
        inferencies.listByModel.mockResolvedValue(mockInferenciesResponse);
        
        mockRouter = {
            push: vi.fn()
        };

        // Mount component
        wrapper = mount(PreSaved, {
            global: {
                plugins: [ElementPlus, i18n],
                components: {
                    'font-awesome-icon': FontAwesomeIcon
                },
                mocks: {
                    $router: mockRouter
                }
            },
            props: {
                fase: 'Training'
            }
        });
    });

    it('renders correctly', async () => {
        expect(wrapper.find('h1').text()).toContain('Energy label for Training');
        expect(wrapper.find('h2').text()).toContain('Create label for dataset model');
    });

    it('loads and displays models in dropdown', async () => {
        await flushPromises();
        
        const modelSelect = wrapper.findComponent({ name: 'el-select' });
        const options = modelSelect.findAllComponents({ name: 'el-option' });
        
        expect(options).toHaveLength(2);
        expect(options[0].props('label')).toBe('Model A');
        expect(options[1].props('label')).toBe('Model B');
    });

    it('shows experiment selector after model selection', async () => {
        await flushPromises();
    
        // Check initial visible select components
        const initialSelects = wrapper.findAllComponents({ name: 'el-select' });
        const visibleSelects = initialSelects.filter(select => select.isVisible());
        expect(visibleSelects).toHaveLength(1);
    
        // Simulate selecting a model
        await wrapper.setData({ selectedModel: 1 });
        await wrapper.vm.canviModel();
        await flushPromises();
    
        // Check visible select components after model selection
        const allSelects = wrapper.findAllComponents({ name: 'el-select' });
        const newVisibleSelects = allSelects.filter(select => select.isVisible());
        expect(newVisibleSelects).toHaveLength(2);
    });  

    it('loads training experiments when model is selected', async () => {
        await wrapper.setData({ selectedModel: 1 });
        await wrapper.vm.canviModel();
        await flushPromises();
        
        const allSelects = wrapper.findAllComponents({ name: 'el-select' });
        const newVisibleSelects = allSelects.filter(select => select.isVisible());

        // Check that the second select has options
        const experimentSelect = newVisibleSelects[1];
        const experimentOptions = experimentSelect.findAllComponents({ name: 'el-option' });
        expect(experimentOptions).toHaveLength(2);

        // Check that the options are correct
        expect(experimentOptions[0].props('label')).toBe(formatData("2023-11-21T17:01:34.781082Z"));
        expect(experimentOptions[1].props('label')).toBe(formatData("2023-11-23T10:50:39.410848Z"));
    });

    it('loads inference experiments when in inference mode', async () => {
        // Set component to Inference mode
        await wrapper.setProps({ fase: 'Inference' });
        await flushPromises();
        
        await wrapper.setData({ selectedModel: 1 });
        await wrapper.vm.canviModel();
        await flushPromises();
        
        expect(inferencies.listByModel).toHaveBeenCalledWith(1);
        
        const allSelects = wrapper.findAllComponents({ name: 'el-select' });
        const newVisibleSelects = allSelects.filter(select => select.isVisible());
        const experimentSelect = newVisibleSelects[1];
        const experimentOptions = experimentSelect.findAllComponents({ name: 'el-option' });
        
        // Verify number and content of options (according to mock data)
        expect(experimentOptions).toHaveLength(2);
        expect(experimentOptions[0].props('label')).toBe(formatData("2023-11-21T17:01:34.781082Z"));
        expect(experimentOptions[1].props('label')).toBe(formatData("2023-11-23T10:50:39.410848Z"));
    });

    it('shows button when experiment is selected', async () => {
        await flushPromises();
    
        // Initially, the button should be hidden
        const button = wrapper.findComponent({ name: 'el-button' });
        expect(button.exists()).toBe(true);
        expect(button.isVisible()).toBe(false);
    
        // Select model and experiment
        await wrapper.setData({ 
            selectedModel: 1,
            selectedExperiment: 1 
        });
        await wrapper.vm.$nextTick();
    
        // Button should now be visible
        expect(button.isVisible()).toBe(true);
        expect(button.text()).toBe('Generate label');
    });

    it('navigates to correct route for training', async () => {
        await wrapper.setData({ 
            selectedModel: 1,
            selectedExperiment: 2 
        });
        
        await wrapper.vm.mostrarEtiqueta();
        
        expect(mockRouter.push).toHaveBeenCalledWith({
            name: 'Label info for training',
            params: { 
                id_model: 1,
                id_training: 2 
            }
        });
    });

    it('navigates to correct route for inference', async () => {
        wrapper.setProps({ fase: 'Inference' });
        await wrapper.setData({ 
            selectedModel: 1,
            selectedExperiment: 2
        });
        
        await wrapper.vm.mostrarEtiqueta();
        
        expect(mockRouter.push).toHaveBeenCalledWith({
            name: 'Label info for inference',
            params: { 
                id_model: 1,
                id_inference: 2
            }
        });
    });
});