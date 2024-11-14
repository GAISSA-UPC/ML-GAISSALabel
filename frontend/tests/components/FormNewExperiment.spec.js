import { mount } from '@vue/test-utils';
import FormNewExperiment from '@/components/FormNewExperiment.vue';
import ElementPlus from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { i18n } from '@/i18n';
import models from '@/controllers/models';
import metriques from '@/controllers/metriques';
import informacions from '@/controllers/informacions';
import trainings from '@/controllers/trainings';
import flushPromises from 'flush-promises';

// Import mocks
vi.mock('@/controllers/models');
vi.mock('@/controllers/metriques');
vi.mock('@/controllers/informacions');
vi.mock('@/controllers/trainings');

// Mocks to return a specific response structure
import { mockModelsData, mockMetriquesData, mockInformacionsData } from '@tests/components/FormNewExperiment.mock'; 

describe('FormNewExperiment.vue', () => {
    let wrapper;
    let mockRouter;

    beforeEach(() => {
        models.list.mockResolvedValue(mockModelsData);
        metriques.listOrderedFilteredByPhase.mockResolvedValue(mockMetriquesData);
        informacions.listFilteredByPhase.mockResolvedValue(mockInformacionsData);
        trainings.create.mockResolvedValue({ status: 201, data: { id: 1 } });
        
        mockRouter = {
            push: vi.fn(),
        };

        wrapper = mount(FormNewExperiment, {
            global: {
                plugins: [ElementPlus, i18n],
                components: {
                    'font-awesome-icon': FontAwesomeIcon,
                },
                mocks: {
                    $router: mockRouter,
                },
            },
            props: {
                fase: 'Training',
            },
        });
    });

    it('renders correctly', () => {
        expect(wrapper.exists()).toBe(true);
    });

    it('displays the correct title based on the fase prop', () => {
        expect(wrapper.find('h1').text()).toContain('Energy label for Training');
        expect(wrapper.find('h2').text()).toContain('Register a new Training');
    });

    it('loads and displays all models in the select dropdown', async () => {
        await flushPromises();
        await wrapper.vm.$nextTick();
        
        // Find the specific el-select component
        const select = wrapper.findComponent({ name: 'el-select' });
        const options = select.findAllComponents({ name: 'el-option' });

        expect(options).toHaveLength(2);    // Expect two options based on the mock data

        // Verify both models are displayed
        expect(options[0].text()).toBe('Model A');
        expect(options[1].text()).toBe('Model B');
    });

    it('opens the dialog when "Add New Model" / "+" button is clicked', async () => {
        await wrapper.find('.action-button-light').trigger('click');
        expect(wrapper.vm.dialogNewModel).toBe(true);
    });

    it('displays success alert when estat is "modelCreat-ok"', async () => {
        wrapper.setData({ estat: 'modelCreat-ok' });
        await wrapper.vm.$nextTick();
        expect(wrapper.find('.el-alert--success').text()).toContain('Model registered correctly');
    });

    it('displays error alert when estat is "modelCreat-ko"', async () => {
        wrapper.setData({ estat: 'modelCreat-ko' });
        await wrapper.vm.$nextTick();
        expect(wrapper.find('.el-alert--error').text()).toContain('There was an error while creating the model');
    });

    it('updates selectedModel when a model is selected', async () => {
        await wrapper.vm.$nextTick();

        // Find the specific el-select component
        const select = wrapper.findComponent({ name: 'el-select' });
        const options = select.findAllComponents({ name: 'el-option' });
        select.vm.$emit('update:modelValue', '1');
        await wrapper.vm.$nextTick();
        expect(wrapper.vm.selectedModel).toBe('1');
    });

    it('sets estat to "select-model" if no model is selected on submit', async () => {
        const button = wrapper.findComponent({ ref: 'generateLabelButton' });
        await button.trigger('click');

        expect(wrapper.vm.estat).toBe('select-model');
        expect(wrapper.find('.el-alert--error').text()).toContain('Please, select (or create) some model');
    });

    it('redirects correctly on successful form submission for Training', async () => {
        wrapper.setData({ selectedModel: 'model A' });

        await wrapper.vm.mostrarEtiqueta();
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
            name: 'Label info for training',
            params: { id_model: 'model A', id_training: 1 },
        });
    });

    it('redirects correctly on successful form submission for Inference', async () => {
        wrapper.setProps({ fase: 'Inference' });
        wrapper.setData({ selectedModel: 'model A' });

        await wrapper.vm.mostrarEtiqueta();
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
            name: 'Label info for inference',
            params: { id_model: 'model A', id_inference: 1 },
        });
    });
});
