import { mount } from '@vue/test-utils';
import EmissionsReductionCard from '@/tools/gaissaroianalyzer/components/EmissionsReductionCard.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import { library } from '@fortawesome/fontawesome-svg-core';
import { 
    faCloud, 
    faLeaf, 
    faArrowRight, 
    faSeedling, 
    faGasPump, 
    faTree, 
    faCar, 
    faMobileAlt, 
    faGlobe 
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import flushPromises from 'flush-promises';

// Add required FontAwesome icons
library.add(faCloud, faLeaf, faArrowRight, faSeedling, faGasPump, faTree, faCar, faMobileAlt, faGlobe);

describe('EmissionsReductionCard.vue', () => {
    let wrapper;
    
    // Sample data for the component
    const defaultProps = {
        emissionsData: {
            country_carbon_intensity_kgCO2Kwh: 0.385,
            emissions_country_used: 'Spain',
            baseline_emissions_gCO2: 1500,
            new_emissions_gCO2: 800,
            emissions_saved_gCO2: 700
        },
        numInferences: 10000,
        formatNumber: (num) => num.toLocaleString('en-US', { maximumFractionDigits: 2 }),
        showTitle: true,
        columnCount: 2
    };

    beforeEach(() => {
        wrapper = mount(EmissionsReductionCard, {
            props: defaultProps,
            global: {
                plugins: [ElementPlus, i18n],
                components: { 'font-awesome-icon': FontAwesomeIcon }
            }
        });
    });

    it('renders the component with title when showTitle is true', () => {
        expect(wrapper.find('h3').exists()).toBe(true);
        expect(wrapper.find('h3').text()).toContain('Environmental Impact');
    });

    it('does not show title when showTitle is false', async () => {
        await wrapper.setProps({ showTitle: false });
        expect(wrapper.find('h3').exists()).toBe(false);
    });

    it('displays correct carbon intensity value', async () => {
        // Wait for the component to render
        await flushPromises();
        
        // Get the HTML content to check for the formatted value
        const html = wrapper.html();
        expect(html).toContain('385');
        expect(html).toContain('gCO₂/kWh');
    });

    it('displays correct region', async () => {
        await flushPromises();
        const html = wrapper.html();
        expect(html).toContain('Spain');
    });

    it('shows "Global Average" when no region is provided', async () => {
        const updatedData = {
            ...defaultProps.emissionsData,
            emissions_country_used: null
        };
        await wrapper.setProps({ emissionsData: updatedData });
        await flushPromises();
        
        const html = wrapper.html();
        expect(html).toContain('Global Average');
    });

    it('formats emissions correctly in grams', () => {
        const result = wrapper.vm.formatEmissions(500);
        expect(result).toBe('500 g');
    });

    it('formats emissions correctly in kilograms', () => {
        const result = wrapper.vm.formatEmissions(1500);
        expect(result).toBe('1.5 kg');
    });

    it('defaults to 0 g when emission value is NaN', () => {
        const result = wrapper.vm.formatEmissions('not-a-number');
        expect(result).toBe('0 g');
    });

    it('displays baseline and optimized emissions correctly', () => {
        const baselineValue = wrapper.find('.impact-item.baseline .impact-value');
        const optimizedValue = wrapper.find('.impact-item.optimized .impact-value');
        
        expect(baselineValue.text()).toBe('1.5 kg CO₂');
        expect(optimizedValue.text()).toBe('800 g CO₂');
    });

    it('displays correct CO₂ savings', () => {
        const savingsText = wrapper.find('.savings-text strong');
        expect(savingsText.text()).toContain('700 g');
        expect(savingsText.text()).toContain('CO₂ saved');
    });

    it('displays correct number of inferences', () => {
        const savingsContext = wrapper.find('.savings-context');
        expect(savingsContext.text()).toContain('10,000');
        expect(savingsContext.text()).toContain('inferences');
    });

    it('provides environmental context for small savings (< 50g)', async () => {
        await wrapper.setProps({
            emissionsData: { 
                ...defaultProps.emissionsData,
                emissions_saved_gCO2: 40
            }
        });
        
        const context = wrapper.find('.context-card');
        expect(context.text()).toContain('Every gram');
        expect(context.text()).toContain('sustainability');
    });

    it('provides environmental context for phone charging equivalent (50g-1kg)', async () => {
        await wrapper.setProps({
            emissionsData: { 
                ...defaultProps.emissionsData,
                emissions_saved_gCO2: 100
            }
        });
        
        const context = wrapper.find('.environmental-context .context-card');
        expect(context.text()).toContain('phone');
        expect(context.text()).toContain('usage days');
    });

    it('provides environmental context for car driving equivalent (1kg-10kg)', async () => {
        await wrapper.setProps({
            emissionsData: { 
                ...defaultProps.emissionsData,
                emissions_saved_gCO2: 2000
            }
        });
        
        const context = wrapper.find('.environmental-context .context-card');
        expect(context.text()).toContain('car driving');
        expect(context.text()).toContain('km');
    });

    it('provides environmental context for tree equivalent (10kg-100kg)', async () => {
        await wrapper.setProps({
            emissionsData: { 
                ...defaultProps.emissionsData,
                emissions_saved_gCO2: 15000
            }
        });
        
        const context = wrapper.find('.environmental-context .context-card');
        expect(context.text()).toContain('tree');
        expect(context.text()).toContain('year');
    });

    it('provides environmental context for gasoline equivalent (>100kg)', async () => {
        await wrapper.setProps({
            emissionsData: { 
                ...defaultProps.emissionsData,
                emissions_saved_gCO2: 250000
            }
        });
        
        const context = wrapper.find('.environmental-context .context-card');
        expect(context.text()).toContain('gasoline');
        expect(context.text()).toContain('liters');
    });
});
