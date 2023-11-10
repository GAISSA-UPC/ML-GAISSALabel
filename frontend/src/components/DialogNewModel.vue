<template>
    <el-dialog :title="$t('Add a new model')"
               @close="closeDialogNewModel"
    >
        <el-form :model="newModel" label-position="top">
            <el-form-item :label="$t('Name')">
                <el-input
                    v-model="newModel.nom"
                />
            </el-form-item>
            <el-form-item :label="$t('Description')">
                <el-input
                    v-model="newModel.informacio"
                    type="textarea"
                />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="this.$emit('cancel')">{{ $t('Cancel') }}</el-button>
                <el-button type="success" @click="afegirModel">{{ $t('Create') }}</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
import models from "@/services/models";

export default {
    name: "DialogNewModel",
    emits: ['modelCreat-ok', 'modelCreat-ko', 'cancel'],
    data() {
        return {
            newModel: {},
        };
    },
    methods: {
        async afegirModel() {
            const response = await models.create(this.newModel)
            if (response.status === 201) {
                this.$emit('modelCreat-ok')
            }
        },
        async closeDialogNewModel() {
            this.newModel = {}
            this.$emit('cancel')
        },
    },
}
</script>

<style scoped>

</style>