// EnergyLabel.spec.js
import { mount } from '@vue/test-utils';
import EnergyLabel from '@/components/EnergyLabel.vue';
import flushPromises from 'flush-promises';

describe('EnergyLabel.vue', () => {
    let wrapper;
    const mockPdfUrl = 'blob:mock-url';
    const mockBase64 = 'JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKI...'; 
    
    // Mock browser APIs
    beforeAll(() => {
        global.URL.createObjectURL = vi.fn(() => mockPdfUrl);
        global.URL.revokeObjectURL = vi.fn();
        global.Blob = vi.fn((content, options) => ({ content, options }));
        global.atob = vi.fn(str => str); // Simple mock, real implementation not needed for tests
    });

    beforeEach(() => {
        // Reset mocks
        vi.clearAllMocks();
        
        // Mount component
        wrapper = mount(EnergyLabel, {
            props: {
                pdfBase64: mockBase64
            }
        });
    });

    it('renders iframe with correct PDF URL', async () => {
        await flushPromises();
        
        const iframe = wrapper.find('iframe');
        expect(iframe.exists()).toBe(true);
        expect(iframe.attributes('src')).toBe(mockPdfUrl);
        expect(iframe.attributes('type')).toBe('application/pdf');
    });

    it('creates blob URL from base64 on mount', async () => {
        await flushPromises();
        
        expect(global.atob).toHaveBeenCalledWith(mockBase64);
        expect(global.Blob).toHaveBeenCalledWith(
            [expect.any(String)], 
            { type: "application/pdf" }
        );
        expect(global.URL.createObjectURL).toHaveBeenCalled();
        expect(wrapper.vm.pdfURL).toBe(mockPdfUrl);
    });

    it('updates PDF URL when base64 prop changes', async () => {
        const newBase64 = 'newMockBase64Data';
        await wrapper.setProps({ pdfBase64: newBase64 });
        await flushPromises();
        
        expect(global.atob).toHaveBeenCalledWith(newBase64);
        expect(global.URL.createObjectURL).toHaveBeenCalled();
        expect(wrapper.find('iframe').attributes('src')).toBe(mockPdfUrl);
    });

    it('revokes object URL on unmount', async () => {
        wrapper.vm.pdfURL = mockPdfUrl;
        await wrapper.unmount();
        
        expect(global.URL.revokeObjectURL).toHaveBeenCalledWith(mockPdfUrl);
    });

    it('has correct iframe dimensions', () => {
        const iframe = wrapper.find('iframe');
        expect(iframe.attributes('width')).toBe('100%');
        expect(iframe.attributes('height')).toBe('600px');
    });
});