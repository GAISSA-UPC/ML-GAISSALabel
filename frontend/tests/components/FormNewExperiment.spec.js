import { mount } from '@vue/test-utils';
import FormNewExperiment from '@/components/FormNewExperiment.vue';
import ElementPlus from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { i18n } from '@/i18n';
import models from '@/controllers/models';
import metriques from '@/controllers/metriques';
import informacions from '@/controllers/informacions';

// Import mocks
vi.mock('@/controllers/models');
vi.mock('@/controllers/metriques');
vi.mock('@/controllers/informacions');

// Mocks to return a specific response structure
import { mockModelsData, mockMetriquesData, mockInformacionsData } from '@tests/components/FormNewExperiment.mock'; 

describe('FormNewExperiment.vue', () => {
    let wrapper;

    beforeEach(() => {
        models.list.mockResolvedValue(mockModelsData);
        metriques.listOrderedFilteredByPhase.mockResolvedValue(mockMetriquesData);
        informacions.listFilteredByPhase.mockResolvedValue(mockInformacionsData);

        wrapper = mount(FormNewExperiment, {
            global: {
                plugins: [ElementPlus, i18n],
                components: {
                    'font-awesome-icon': FontAwesomeIcon,
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
});
