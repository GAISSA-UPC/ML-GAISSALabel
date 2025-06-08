import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import TacticSourcesCard from '@/tools/gaissaroianalyzer/components/TacticSourcesCard.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';

describe('TacticSourcesCard.vue', () => {
    let wrapper;

    const mockSingleSource = [
        {
            title: 'Efficient Neural Network Compression Techniques',
            url: 'https://research.example.com/compression-techniques'
        }
    ];

    const mockMultipleSources = [
        {
            title: 'Neural Network Quantization Methods',
            url: 'https://arxiv.org/papers/quantization-methods'
        },
        {
            title: 'Deep Learning Model Pruning Strategies',
            url: 'https://journal.ai.com/pruning-strategies-2023'
        },
        {
            title: 'Knowledge Distillation for Model Compression',
            url: 'https://academic.research.org/knowledge-distillation'
        }
    ];

    const mockSourcesWithSpecialChars = [
        {
            title: 'AI/ML Optimization: "Advanced Techniques" & Best Practices (2023)',
            url: 'https://example.com/research?q=neural+networks&year=2023&category=AI%20ML'
        }
    ];

    beforeEach(() => {
        wrapper = mount(TacticSourcesCard, {
            props: {
                sources: mockSingleSource
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
        it('renders el-card when sources array has items', () => {
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(true);
        });

        it('does not render el-card when sources array is empty', async () => {
            await wrapper.setProps({ sources: [] });
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(false);
        });

        it('does not render el-card when sources is null or undefined', async () => {
            await wrapper.setProps({ sources: null });
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(false);

            await wrapper.setProps({ sources: undefined });
            expect(wrapper.findComponent({ name: 'el-card' }).exists()).toBe(false);
        });

        it('renders section title', () => {
            const title = wrapper.find('.section-title');
            expect(title.exists()).toBe(true);
            expect(title.text()).toBe('Tactic Sources');
        });

        it('renders description paragraph', () => {
            const description = wrapper.find('.results-description');
            expect(description.exists()).toBe(true);
            expect(description.text()).toContain('This analysis provides an estimation');
        });
    });

    describe('Single Source Display', () => {
        it('renders one el-descriptions for single source', () => {
            const descriptions = wrapper.findAllComponents({ name: 'el-descriptions' });
            expect(descriptions).toHaveLength(1);
        });

        it('displays source title correctly', () => {
            expect(wrapper.text()).toContain(mockSingleSource[0].title);
        });

        it('displays source URL as a link', () => {
            const link = wrapper.find('a[target="_blank"]');
            expect(link.exists()).toBe(true);
            expect(link.attributes('href')).toBe(mockSingleSource[0].url);
            expect(link.attributes('rel')).toBe('noopener noreferrer');
            expect(link.text()).toBe(mockSingleSource[0].url);
        });
    });

    describe('Multiple Sources Display', () => {
        beforeEach(async () => {
            await wrapper.setProps({ sources: mockMultipleSources });
        });

        it('renders multiple el-descriptions for multiple sources', () => {
            const descriptions = wrapper.findAllComponents({ name: 'el-descriptions' });
            expect(descriptions).toHaveLength(mockMultipleSources.length);
        });

        it('displays all source titles correctly', () => {
            mockMultipleSources.forEach(source => {
                expect(wrapper.text()).toContain(source.title);
            });
        });

        it('displays all source URLs as links', () => {
            const links = wrapper.findAll('a[target="_blank"]');
            expect(links).toHaveLength(mockMultipleSources.length);
            
            links.forEach((link, index) => {
                expect(link.attributes('href')).toBe(mockMultipleSources[index].url);
                expect(link.attributes('rel')).toBe('noopener noreferrer');
                expect(link.text()).toBe(mockMultipleSources[index].url);
            });
        });
    });

    describe('Accessibility', () => {
        it('has proper link attributes for security', () => {
            const links = wrapper.findAll('a[target="_blank"]');
            links.forEach(link => {
                expect(link.attributes('rel')).toBe('noopener noreferrer');
                expect(link.attributes('target')).toBe('_blank');
            });
        });
    });
});
