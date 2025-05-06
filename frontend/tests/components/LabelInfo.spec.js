import { mount } from '@vue/test-utils';
import LabelInfo from '@/tools/gaissalabel/components/LabelInfo.vue';
import ElementPlus from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core'; 
import {
    faIdCardClip,
    faCircleInfo,
    faCalendarDays,
    faDumbbell,
    faUser, 
    faBullseye
} from '@fortawesome/free-solid-svg-icons';

import { i18n } from '@/i18n';
import trainings from '@/tools/gaissalabel/services/trainings';
import inferencies from '@/tools/gaissalabel/services/inferencies';
import metriques from '@/tools/gaissalabel/services/metriques';
import models from '@/tools/gaissalabel/services/models';
import EnergyLabel from '@/tools/gaissalabel/components/EnergyLabel.vue'
import CustomSlider from '@/tools/gaissalabel/components/CustomSlider.vue'
import flushPromises from 'flush-promises';

// Mock the controllers
vi.mock('@/tools/gaissalabel/services/trainings');
vi.mock('@/tools/gaissalabel/services/inferencies');
vi.mock('@/tools/gaissalabel/services/metriques');
vi.mock('@/tools/gaissalabel/services/models');

library.add(faIdCardClip, faCircleInfo, faCalendarDays, faDumbbell, faUser, faBullseye);

// Mock route params
const mockRouteParams = {
    id_model: '1',
    id_training: '1'
};

vi.mock('@/tools/gaissalabel/components/EnergyLabel.vue', () => ({
    default: {
      name: 'EnergyLabel',
      props: {
        pdfBase64: String
      },
      template: '<div class="mock-energy-label"></div>'
    }
  }));
  
  vi.mock('@/tools/gaissalabel/components/CustomSlider.vue', () => ({
    default: {
      name: 'CustomSlider',
      props: {
        marks: Object,
        max: Number,
        values: Object,
        color: String,
      },
      template: '<div class="mock-custom-slider"></div>'
    }
  }));

// Mocks to return a specific response structure
import { mockTrainingResponse, mockModelResponse, mockMetriquesResponse } from '@tests/components/LabelInfo.mock';

describe('LabelInfo.vue', () => {
    let wrapper;

    beforeEach(() => {
        // Reset mocks before each test
        trainings.retrieve.mockResolvedValue(mockTrainingResponse);
        inferencies.retrieve.mockResolvedValue(mockTrainingResponse);
        models.retrieve.mockResolvedValue(mockModelResponse);
        metriques.listOrderedFilteredByPhase.mockResolvedValue(mockMetriquesResponse);

        // Mock $route
        const mockRoute = {
            params: mockRouteParams
        };

        wrapper = mount(LabelInfo, {
            global: {
                plugins: [ElementPlus, i18n],
                components: { 
                    'font-awesome-icon': FontAwesomeIcon,
                    EnergyLabel,
                    CustomSlider,
                },
                mocks: {
                    $route: mockRoute
                }
            },
            props: {
                fase: 'Training'
            }
        });
    });

    it('renders component correctly', async () => {
        await flushPromises();
        await wrapper.vm.$nextTick();

        // Check main sections are rendered
        expect(wrapper.find('h1').text()).toContain('Energy label for Training');
        expect(wrapper.findComponent({ name: 'EnergyLabel' }).exists()).toBe(true);
    });

    it('fetches and displays model information correctly', async () => {
        await flushPromises();
        await wrapper.vm.$nextTick();
    
        // Query table rows directly (5 based on mock data)
        const rows = wrapper.findAll('tr');
        expect(rows).toHaveLength(5);

        expect(rows.at(0).text()).toContain('Model name');
        expect(rows.at(0).text()).toContain('GPT-2');

        expect(rows.at(1).text()).toContain('Model information');
        expect(rows.at(1).text()).toContain('GPT-2 is a transformers model');

        expect(rows.at(2).text()).toContain('Model creation date');
        expect(rows.at(2).text()).toContain('November 21, 2023 at 5:59 PM');

        expect(rows.at(3).text()).toContain('Training identifier');
        expect(rows.at(3).text()).toContain('1'); 

        expect(rows.at(4).text()).toContain('Training registration date');
        expect(rows.at(4).text()).toContain('November 21, 2023 at 6:01 PM');
    });

    it('displays energy label in EnergyLabel component', async () => {
        await flushPromises();
        const energyLabel = wrapper.findComponent(EnergyLabel);
        expect(energyLabel.props('pdfBase64')).toBe('mockBase64');
    });

    it('renders metric results with correct information', async () => {
        await flushPromises();
        await wrapper.vm.$nextTick();
        
        // Find metric section using more specific selectors
        const metricSection = wrapper.find('[style*="margin-bottom: 40px"]');
        const metricName = metricSection.find('h3');
        const metricValue = metricSection.find('p[style*="font-size: 20px"]');
        const metricQualification = metricSection.find('p[style*="font-size: 35px"]');
        
        // Check metric name, qualification and value
        expect(metricName.text()).toBe('Size efficiency');
        expect(metricQualification.text()).toBe('A');
        expect(metricValue.text()).toContain('266551.57');
        expect(metricValue.text()).toContain('B');
    });

    it('displays recommendations for metrics', async () => {
        await flushPromises();
        await wrapper.vm.$nextTick();
        
        // Get recommendations sections
        const metricSections = wrapper.findAll('[style*="margin-bottom: 40px"]');
        
        // Full verify first metric recommendations
        const firstMetricRecs = metricSections.at(0).findAll('ul li');
        expect(firstMetricRecs).toHaveLength(4);
        expect(firstMetricRecs[0].text()).toBe('Model Pruning: Use model pruning techniques to remove unnecessary parameters, reducing model size without compromising performance.');
        expect(firstMetricRecs[1].text()).toBe('Knowledge Distillation: Apply knowledge distillation to train smaller models that are as effective as larger ones.');
        expect(firstMetricRecs[2].text()).toBe('Efficient Neural Network Architectures: Employ efficient neural network architectures like MobileNets or EfficientNets that are designed for lower energy consumption.');
        expect(firstMetricRecs[3].text()).toBe('Other Model Optimizations');
        
        // Fast verify second metric recommendations
        const secondMetricRecs = metricSections.at(1).findAll('ul li');
        expect(secondMetricRecs).toHaveLength(3);
    });
});