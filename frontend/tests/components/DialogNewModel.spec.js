import { mount } from '@vue/test-utils';
import DialogNewModel from '@/components/DialogNewModel.vue';
import ElementPlus from 'element-plus';
import { i18n } from '@/i18n';
import models from '@/controllers/models';
import flushPromises from 'flush-promises';

vi.mock('@/controllers/models');

describe('DialogNewModel.vue', () => {
    let wrapper;

    beforeEach(() => {
        // Mount component
        wrapper = mount(DialogNewModel, {
            global: {
                plugins: [ElementPlus, i18n],
                stubs: {
                    'el-dialog': {
                        template: '<div><slot></slot><slot name="footer"></slot></div>',
                    }
                },
            }
        });
    });

    it('renders dialog with correct form fields', async () => {
        await wrapper.vm.$nextTick();
        const formItems = wrapper.findAllComponents({ name: 'el-form-item' });
        console.log(wrapper.html());
        expect(formItems).toHaveLength(3);
        
        expect(formItems[0].props('label')).toBe('Name');
        expect(formItems[1].props('label')).toBe('Author');
        expect(formItems[2].props('label')).toBe('Description');
    });

    it('updates newModel data when form inputs change', async () => {
        const inputs = wrapper.findAllComponents({ name: 'el-input' });
        
        await inputs[0].setValue('Test Model');
        await inputs[1].setValue('Test Author');
        await inputs[2].setValue('Test Description');

        expect(wrapper.vm.newModel).toEqual({
            nom: 'Test Model',
            autor: 'Test Author',
            informacio: 'Test Description'
        });
    });

    it('emits cancel event when cancel button is clicked', async () => {
        const cancelButton = wrapper.findAllComponents({ name: 'el-button' })[0];
        await cancelButton.trigger('click');
        
        expect(wrapper.emitted('cancel')).toBeTruthy();
        expect(wrapper.emitted('cancel')).toHaveLength(1);
    });

    it('creates model and emits success event when form is submitted', async () => {
        // Mock successful model creation
        models.create.mockResolvedValueOnce({
            status: 201,
            data: { id: 1 }
        });

        wrapper.setData({
            newModel: {
                nom: 'Test Model',
                autor: 'Test Author',
                informacio: 'Test Description'
            }
        });

        // Submit form
        const createButton = wrapper.findAllComponents({ name: 'el-button' })[1];
        await createButton.trigger('click');
        await flushPromises();

        expect(models.create).toHaveBeenCalledWith({
            nom: 'Test Model',
            autor: 'Test Author',
            informacio: 'Test Description'
        });

        expect(wrapper.emitted('modelCreat-ok')).toBeTruthy();
        expect(wrapper.emitted('modelCreat-ok')[0]).toEqual([1]);
    });

    it('clears form data when dialog is closed', async () => {
        wrapper.setData({
            newModel: {
                nom: 'Test Model',
                autor: 'Test Author',
                informacio: 'Test Description'
            }
        });

        await wrapper.vm.closeDialogNewModel();

        // Verify form data is cleared
        expect(wrapper.vm.newModel).toEqual({});
        expect(wrapper.emitted('cancel')).toBeTruthy();
    });
});
