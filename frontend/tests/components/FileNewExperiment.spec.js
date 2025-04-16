import { mount } from '@vue/test-utils';
import FileNewExperiment from '@/tools/gaissalabel/components/FileNewExperiment.vue';
import ElementPlus from 'element-plus';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { i18n } from '@/i18n';
import XLSX from "xlsx";
import eines from '@/tools/gaissalabel/services/eines';
import flushPromises from 'flush-promises';

vi.mock('@/tools/gaissalabel/services/eines');
vi.mock('xlsx');

describe('FileNewExperiment.vue', () => {
    let wrapper;
    let mockRouter;

    beforeEach(() => {
        // Mock data setup
        eines.list.mockResolvedValue({ data: [{ id: 'toolA', nom: 'Tool A' }, { id: 'toolB', nom: 'Tool B' }] });
        mockRouter = { push: vi.fn() };

        wrapper = mount(FileNewExperiment, {
            global: {
                plugins: [ElementPlus, i18n],
                components: { 'font-awesome-icon': FontAwesomeIcon },
                mocks: { $router: mockRouter },
            },
            props: { fase: 'Training' },
        });
    });

    it('renders titles correctly based on fase prop', () => {
        expect(wrapper.find('h1').text()).toContain('Energy label for Training');
        expect(wrapper.find('h2').text()).toContain('Register a new Training');
    });

    it('adds and displays uploaded files correctly', async () => {
        wrapper.setData({
            fileList: [
                { name: 'file1.xlsx', tool: '' },
                { name: 'file2.xlsx', tool: '' }
            ]
        });
        await wrapper.vm.$nextTick();

        const fileItems = wrapper.findAll('.el-upload-list__item');
        expect(fileItems).toHaveLength(2);
        expect(fileItems.at(0).text()).toContain('file1.xlsx');
        expect(fileItems.at(1).text()).toContain('file2.xlsx');
    });

    it('loads and displays tool options in each file entry dropdown after files are uploaded', async () => {
        wrapper.setData({
            fileList: [
                { name: 'file1.xlsx', tool: '' },
                { name: 'file2.xlsx', tool: '' }
            ]
        });
        await wrapper.vm.$nextTick();
    
        // Find all the tool dropdowns
        const dropdowns = wrapper.findAllComponents({ name: 'el-select' });
        console.log("hola" + dropdowns);
        expect(dropdowns).toHaveLength(2);
    
        // Verify that each dropdown contains the expected options
        dropdowns.forEach((dropdown, index) => {
            expect(dropdown.props().placeholder).toContain('Tool used');
            const options = dropdown.findAllComponents({ name: 'el-option' });
            expect(options).toHaveLength(2);  // Number of tools available
    
            expect(options.at(0).text()).toBe('Tool A');
            expect(options.at(1).text()).toBe('Tool B');
        });
    });

    it('removes file from fileList when delete button is clicked', async () => {
        wrapper.setData({ fileList: [{ name: 'file1.xlsx', tool: '' }] });
        await wrapper.vm.$nextTick();

        expect(wrapper.vm.fileList).toHaveLength(1);

        // Find delete button and click
        await wrapper.find('.el-icon--close').trigger('click');
        expect(wrapper.vm.fileList).toHaveLength(0);
    });

    it('correctly processes and navigates with generated label data on button click', async () => {
        // Mock a file and data processing function
        wrapper.setData({ fileList: [{ name: 'file1.xlsx', tool: 'toolA' }] });
        wrapper.vm.carregarFitxers = vi.fn().mockResolvedValue({ processedData: 'example' });
        await wrapper.vm.$nextTick();
        
        // Simulate button click
        const button = wrapper.findComponent({ ref: 'generateLabelButton' });
        expect(button.exists()).toBe(true); // Check button is found
        await button.trigger('click');
        await flushPromises();

        // Check navigation with expected params
        expect(mockRouter.push).toHaveBeenCalledWith({
            name: 'training form',
            query: { dadesInicials: JSON.stringify({ processedData: 'example' }) },
        });
    });

    it('calls parseExcelJSON and processes an excel file content correctly', async () => {
        const fakeContent = 'Fake binary content for Excel';
        const parsedData = { header1: 100, header2: 200 };
        XLSX.read.mockReturnValueOnce({
            SheetNames: ['Sheet1'],
            Sheets: { 
                Sheet1: { 
                    A1: { v: 'header1' }, 
                    A2: { v: 100 },
                    B1: { v: 'header2' },
                    B2: { v: 200 }
                } 
            }    
        });

        const result = wrapper.vm.parseExcelJSON(fakeContent);
        expect(result).toEqual(parsedData);
    });
});
