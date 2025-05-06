<template>
    <h1>{{ $t("Calculation tools") }}</h1><br>

    <p>{{ $t('This page allows you to handle the calculation tools that the users are offered. These tools will be shown as options in the generation of an efficiency study from a file.') }}</p>

    <el-row justify="end">
        <el-col :span="2">
            <el-button
                style="margin-left: 10px"
                @click="handleAfegir()"
                class="action-button-light"
            >
                <font-awesome-icon :icon="['fas', 'plus']" />
            </el-button>
        </el-col>
    </el-row>
    <el-table :data="tableEines" style="width: 100%">
        <el-table-column :label="$t('Name')" prop="nom" />
        <el-table-column align="right">
            <template #header>
                <el-input v-model="searchEines" size="small" :placeholder="$t('Type to search')" />
            </template>
            <template #default="scope">
                <el-button
                    size="small"
                    class="action-button-light"
                    @click="handleEdit(scope.$index, scope.row)"
                >
                    <font-awesome-icon :icon="['fas', 'pen-to-square']" />
                </el-button>
                <el-button
                    size="small"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)"
                >
                    <font-awesome-icon :icon="['fas', 'trash']" />
                </el-button>
            </template>
        </el-table-column>
    </el-table><br><br><br>

    <el-dialog v-model="dialogEsborrar" :title="$t('Delete calculation tool')">
        <span>
            <p>{{ $t("Are you sure you want to delete ") }} <span style="font-weight: bold">{{ itemEsborrar.nom }}</span>?</p>
            <p>{{ $t("Be aware that if you do so, users would not be able to use this tool to generate energy labels anymore") }}.</p>
        </span>
        <template #footer>
                        <span class="dialog-footer">
                            <el-button @click="dialogEsborrar = false">{{ $t('Cancel') }}</el-button>
                            <el-button type="danger" @click="deleteItem(itemEsborrar)">{{ $t('Delete') }}</el-button>
                        </span>
        </template>
    </el-dialog>
</template>


<script>
import eines from "@/controllers/eines";

export default {
    name: "AdminEines",
    computed: {
        tableEines() {
            return this.filterData(this.eines, this.searchEines)
        },
    },
    data() {
        return {
            searchEines: '',
            eines: [],
            itemEsborrar: null,
            dialogEsborrar: false,
        }
    },
    methods: {
        async refrescaEines() {
            const response = await eines.list()
            this.eines = response.data
        },
        filterData(dataToFilter, filter) {
            return dataToFilter.filter(
                (data) => !filter || data.nom.toLowerCase().includes(filter.toLowerCase())
            )
        },
        handleEdit(index, row) {
            this.$router.push({
                name: 'Admin eina edit',
                params: {id_eina: row.id}
            })
        },
        handleDelete(index, row) {
            this.itemEsborrar = row
            this.dialogEsborrar = true
        },
        handleAfegir() {
            this.$router.push({
                name: 'Admin eina new'
            })
        },
        async deleteItem(item) {
            await eines.delete(item.id)
            await this.refrescaEines()
            this.dialogEsborrar = false
        }
    },
    async mounted() {
        await this.refrescaEines();
    },
}


</script>

<style scoped>

</style>