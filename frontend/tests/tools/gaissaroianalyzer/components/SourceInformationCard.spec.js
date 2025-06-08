import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import SourceInformationCard from '@/tools/gaissaroianalyzer/components/SourceInformationCard.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';

describe('SourceInformationCard.vue', () => {
    let wrapper;

    const mockSource = {
        title: 'Advanced Neural Network Optimization Research',
        url: 'https://example.com/research/neural-networks'
    };

    const mockSourceWithLongTitle = {
        title: 'A Comprehensive Study on Deep Learning Model Efficiency and Sustainability in Large-Scale Machine Learning Applications',
        url: 'https://academic-journal.com/papers/deep-learning-efficiency/2023/12345'
    };

    beforeEach(() => {
        wrapper = mount(SourceInformationCard, {
            props: {
                source: mockSource
            },
            global: {
                plugins: [ElementPlus, i18n]
            }
        });
    });

    afterEach(() => {
        if (wrapper) {
            wrapper.unmount();
        }
    });

    describe('Component Rendering', () => {
        it('renders el-card when source is provided', () => {
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(true);
        });

        it('does not render el-card when source is null or undefined', async () => {
            await wrapper.setProps({ source: null });
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(false);

            await wrapper.setProps({ source: undefined });
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(false);
        });

        it('renders section title', () => {
            const title = wrapper.find('.section-title');
            expect(title.exists()).toBe(true);
            expect(title.text()).toBe('Source Information');
        });
    });

    describe('Data Display', () => {
        it('displays source title correctly', () => {
            const titleItem = wrapper.find('[data-testid="title-item"]') || 
                            wrapper.findAllComponents({ name: 'el-descriptions-item' })[0];
            expect(wrapper.text()).toContain(mockSource.title);
        });

        it('displays source URL as a link', () => {
            const link = wrapper.find('a[target="_blank"]');
            expect(link.exists()).toBe(true);
            expect(link.attributes('href')).toBe(mockSource.url);
            expect(link.attributes('rel')).toBe('noopener noreferrer');
            expect(link.text()).toBe(mockSource.url);
        });

        it('has proper link attributes', () => {
            const link = wrapper.find('a[target="_blank"]');
            expect(link.attributes('rel')).toBe('noopener noreferrer');
            expect(link.attributes('target')).toBe('_blank');
        });
    });
});
