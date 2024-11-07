import { mount } from '@vue/test-utils';
import FormNewExperiment from '@/components/FormNewExperiment.vue';
import ElementPlus from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { i18n } from '@/i18n';

describe('FormNewExperiment.vue', () => {
    let wrapper;

    beforeEach(() => {
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
