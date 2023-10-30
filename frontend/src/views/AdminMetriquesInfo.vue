<template>
    <h1>{{ $t("Metrics and additional information") }}</h1><br>
    <h2 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Training") }}</h2><br>
    <el-row justify="space-between">
        <el-col :span="6">
            <h3>{{ $t("Metrics") }}</h3><br>
        </el-col>
        <el-col :span="2">
            <el-button
                style="margin-left: 10px"
                @click="dialogAfegir = true"
                class="action-button-light"
            >
                <font-awesome-icon :icon="['fas', 'plus']" />
            </el-button>
        </el-col>
    </el-row>
    <el-table :data="tableTrainingMetriques" style="width: 100%">
        <el-table-column :label="$t('Name')" prop="nom" />
        <el-table-column :label="$t('Weight')" prop="pes" />
        <el-table-column align="right">
            <template #header>
                <el-input v-model="searchMetriquesTraining" size="small" :placeholder="$t('Type to search')" />
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
                    @click="handleDelete(scope.$index, scope.row, 'metric')"
                >
                    <font-awesome-icon :icon="['fas', 'trash']" />
                </el-button>
            </template>
        </el-table-column>
    </el-table><br><br>

    <el-row justify="space-between">
        <el-col :span="6">
            <h3>{{ $t("Additional information") }}</h3><br>
        </el-col>
        <el-col :span="2">
            <el-button
                style="margin-left: 10px"
                @click="dialogAfegir = true"
                class="action-button-light"
            >
                <font-awesome-icon :icon="['fas', 'plus']" />
            </el-button>
        </el-col>
    </el-row>
    <el-table :data="tableTrainingInformacions" style="width: 100%">
        <el-table-column :label="$t('Name')" prop="nom" />
        <el-table-column label="" />
        <el-table-column align="right">
            <template #header>
                <el-input v-model="searchInformacionsTraining" size="small" :placeholder="$t('Type to search')" />
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
                    @click="handleDelete(scope.$index, scope.row, 'additional information')"
                >
                    <font-awesome-icon :icon="['fas', 'trash']" />
                </el-button>
            </template>
        </el-table-column>
    </el-table><br><br><br>


    <h2 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Inference") }}</h2><br>
    <el-row justify="space-between">
        <el-col :span="6">
            <h3>{{ $t("Metrics") }}</h3><br>
        </el-col>
        <el-col :span="2">
            <el-button
                style="margin-left: 10px"
                @click="dialogAfegir = true"
                class="action-button-light"
            >
                <font-awesome-icon :icon="['fas', 'plus']" />
            </el-button>
        </el-col>
    </el-row>
    <el-table :data="tableInferenceMetriques" style="width: 100%">
        <el-table-column :label="$t('Name')" prop="nom" />
        <el-table-column :label="$t('Weight')" prop="pes" />
        <el-table-column align="right">
            <template #header>
                <el-input v-model="searchMetriquesInference" size="small" :placeholder="$t('Type to search')" />
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
                    @click="handleDelete(scope.$index, scope.row, 'metric')"
                >
                    <font-awesome-icon :icon="['fas', 'trash']" />
                </el-button>
            </template>
        </el-table-column>
    </el-table><br><br>

    <el-row justify="space-between">
        <el-col :span="6">
            <h3>{{ $t("Additional information") }}</h3><br>
        </el-col>
        <el-col :span="2">
            <el-button
                style="margin-left: 10px"
                @click="dialogAfegir = true"
                class="action-button-light"
            >
                <font-awesome-icon :icon="['fas', 'plus']" />
            </el-button>
        </el-col>
    </el-row>
    <el-table :data="tableInferenceInformacions" style="width: 100%">
        <el-table-column :label="$t('Name')" prop="nom" />
        <el-table-column label="" />
        <el-table-column align="right">
            <template #header>
                <el-input v-model="searchInformacionsInference" size="small" :placeholder="$t('Type to search')" />
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
                    @click="handleDelete(scope.$index, scope.row, 'additional information')"
                >
                    <font-awesome-icon :icon="['fas', 'trash']" />
                </el-button>
            </template>
        </el-table-column>
    </el-table><br><br><br>

    <el-dialog v-model="dialogEsborrar"
               :title="titleDelete"
    >
        <span>
            <p>{{ $t("Are you sure you want to delete ") }} <span style="font-weight: bold">{{ itemEsborrar.nom }}</span>?</p>
            <p>{{ $t("Be aware that if you do so, the generation of the labels will automatically change, and the application will lose the values recollected about this") }} {{ itemEsborrarType }} {{ $t("for all the models that have been registered") }}.</p>
        </span>
        <template #footer>
                        <span class="dialog-footer">
                            <el-button @click="dialogEsborrar = false">{{ $t('Cancel') }}</el-button>
                            <el-button type="danger" @click="deleteItem(itemEsborrar, itemEsborrarType)">{{ $t('Delete') }}</el-button>
                        </span>
        </template>
    </el-dialog>
</template>


<script>
import metriques from "@/services/metriques";
import informacions from "@/services/informacions";

export default {
    name: "AdminMetriquesInfo",
    computed: {
        tableTrainingMetriques() {
            return this.filterData(this.metriquesTraining, this.searchMetriquesTraining)
        },
        tableTrainingInformacions() {
            return this.filterData(this.informacionsTraining, this.searchInformacionsTraining)
        },
        tableInferenceMetriques() {
            return this.filterData(this.metriquesInference, this.searchMetriquesInference)
        },
        tableInferenceInformacions() {
            return this.filterData(this.informacionsInference, this.searchInformacionsInference)
        },
        titleDelete() {
            return this.$t("Delete") + " " + this.itemEsborrarType
        }
    },
    data() {
        return {
            searchMetriquesTraining: '',
            searchInformacionsTraining: '',
            searchMetriquesInference: '',
            searchInformacionsInference: '',
            metriquesTraining: [],
            metriquesInference: [],
            informacionsTraining: [],
            informacionsInference: [],
            itemEsborrar: null,
            itemEsborrarType: "",
            dialogEsborrar: false,
            dialogAfegir: false,
        }
    },
    methods: {
        async refrescaMetriques() {
            const response = await metriques.listOrdered()
            this.metriquesTraining = response.data.filter((metrica) => metrica.fase === "T")
            this.metriquesInference = response.data.filter((metrica) => metrica.fase === 'I')
        },
        async refrescaInformacions() {
            const response = await informacions.list()
            this.informacionsTraining = response.data.filter((informacio) => informacio.fase === 'T')
            this.informacionsInference = response.data.filter((informacio) => informacio.fase === 'I')
        },
        filterData(dataToFilter, filter) {
            return dataToFilter.filter(
                (data) => !filter || data.nom.toLowerCase().includes(filter.toLowerCase())
            )
        },
        handleEdit(index, row) {
            console.log(index, row)
        },
        handleDelete(index, row, type) {
            this.itemEsborrar = row
            this.itemEsborrarType = type
            this.dialogEsborrar = true
        },
        async deleteItem(item, type) {
            if (type === 'metric') {
                await metriques.delete(item.id)
                await this.refrescaMetriques()
            }
            else {      // type === 'additional information'
                await informacions.delete(item.id)
                await this.refrescaInformacions()
            }
            this.dialogEsborrar = false
        }
    },
    async mounted() {
        await this.refrescaMetriques();
        await this.refrescaInformacions();
    },
}


</script>

<style scoped>

</style>