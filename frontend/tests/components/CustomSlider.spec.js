import { mount } from '@vue/test-utils';
import CustomSlider from '@/components/CustomSlider.vue';
import ElementPlus from 'element-plus';

describe('CustomSlider.vue', () => {
    let wrapper;
    const defaultProps = {
        values: [20, 80],
        marks: { 0: '', 50: '', 100: '' },
        max: 100,
        color: '#ff0000'
    };

    beforeEach(() => {
        wrapper = mount(CustomSlider, {
            props: defaultProps,
            global: {
                plugins: [ElementPlus]
            }
        });
    });

    it('renders el-slider component', () => {
        const slider = wrapper.findComponent({ name: 'el-slider' });
        expect(slider.exists()).toBe(true);
    });

    it('passes props correctly to el-slider', () => {
        const slider = wrapper.findComponent({ name: 'el-slider' });
        expect(slider.props('modelValue')).toEqual(defaultProps.values);
        expect(slider.props('marks')).toEqual(defaultProps.marks);
        expect(slider.props('max')).toBe(defaultProps.max);
    });

    it('slider mode is disabled and range', () => {
        const slider = wrapper.findComponent({ name: 'el-slider' });
        expect(slider.props('disabled')).toBe(true);
        expect(slider.props('range')).toBe(true);
    });
});
