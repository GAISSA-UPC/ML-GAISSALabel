<template>
    <h1>{{ $t("Energy label for training") }}</h1><br>
    <h2>{{ $t("Register a new training") }}</h2><br>

    <el-alert v-if="estat === 'modelCreat-ok'" :title="$t('Model registered correctly')" type="success" @close="estat = ''"/>
    <el-alert v-else-if="estat === 'modelCreat-ko'" :title="$t('There was an error while creating the model')" type="success" @close="estat = ''"/>

    <el-form label-position="top">
        <el-form-item :label="$t('Model')">
            <el-select v-model="selectedModel">
                <el-option
                    v-for="(model, i) in models" :key="i"
                    :value="model.id"
                    :label="model.nom"
                />
            </el-select>
            <el-button
                style="margin-left: 10px"
                @click="dialogNewModel = true"
                class="action-button-light"
            >
                <font-awesome-icon :icon="['fas', 'plus']" />
            </el-button>
        </el-form-item>
        <br>

        <h3>{{ $t("Metrics") }}</h3><br>
        <el-form-item
            v-for="(metrica, i) in metriques" :key="i"
            :label="metrica.nom"
        >
            <el-input-number
                step="0.01"
                v-model="metrica.valor"
                min="0"
            />
            <p style="margin-left: 10px">{{ metrica.unitat }}</p>
        </el-form-item>
        <br>
        <el-button
            @click="generarEtiqueta"
            color="var(--gaissa_green)"
        >
            {{ $t('Generate label') }}
        </el-button>
    </el-form><br>

    <el-dialog v-model="dialogNewModel"
        :title="$t('Add a new model')"
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
                <el-button @click="dialogNewModel = false">{{ $t('Cancel') }}</el-button>
                <el-button type="success" @click="afegirModel">{{ $t('Create') }}</el-button>
            </span>
        </template>
    </el-dialog>

    <EnergyLabel
        :pdfBase64="labelBase64"
        v-show="labelBase64"
    />
</template>

<script>
    import models from '@/services/models'
    import metriques from '@/services/metriques'
    import trainings from '@/services/trainings'
    import EnergyLabel from "@/components/EnergyLabel.vue";
    export default {
        name: "TrainingForm",
        components: {EnergyLabel},
        data() {
            return {
                estat: '',
                models: null,
                selectedModel: null,
                newModel: {},
                dialogNewModel: false,
                metriques: null,
                labelBase64: null,
            };
        },
        methods: {
            async refrescaModels() {
                const response = await models.list()
                this.models = response.data
            },
            async refrescaMetriques() {
                const response = await metriques.listOrderedFilteredByPhase('T')
                this.metriques = response.data
            },
            async generarEtiqueta() {
                const responseCreate = await trainings.create(this.selectedModel, this.metriques)
                if (responseCreate.status === 201) {
                    const entrenament_id = responseCreate.data['id']
                    const responseLabel = await trainings.retrieve(this.selectedModel, entrenament_id)
                    this.labelBase64 = responseLabel.data['energy_label']
                }
            },
            async afegirModel() {
                const response = await models.create(this.newModel)
                if (response.status === 201) {
                    this.models.push(response.data)
                    this.selectedModel = this.models.length
                }
                this.dialogNewModel = false
                this.estat = 'modelCreat-ok'
            },
            async closeDialogNewModel() {
                this.newModel = {}
                this.dialogNewModel = false
            },
        },
        async mounted() {
            await this.refrescaModels();
            await this.refrescaMetriques();
        },
    };
</script>

<style>
</style>