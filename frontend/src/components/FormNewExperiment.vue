<template>
    <h1>{{ $t("Energy label for") }} {{ fase }}</h1><br>
    <h2>{{ $t("Register a new") }} {{ fase }}</h2><br>

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
            @click="mostrarEtiqueta"
            color="var(--gaissa_green)"
        >
            {{ $t('Generate label') }}
        </el-button>
    </el-form><br>

    <DialogNewModel v-model="dialogNewModel"
                    @cancel="dialogNewModel = false"
                    @model-creat-ok="dialogNewModel = false;selectedModel = models.length; estat = 'modelCreat-ok'"
                    @model-creat-ko="dialogNewModel = false; estat = 'modelCreat-ko'"
    />

</template>

<script>
import models from '@/services/models'
import metriques from '@/services/metriques'
import inferencies from '@/services/inferencies'
import trainings from '@/services/trainings'
import DialogNewModel from "@/components/DialogNewModel.vue";
export default {
    name: "FormNewExperiment",
    components: {DialogNewModel},
    props: {
        fase: {required: true, type: String}
    },
    data() {
        return {
            estat: '',
            models: null,
            selectedModel: null,
            newModel: {},
            dialogNewModel: false,
            metriques: null,
        };
    },
    methods: {
        async refrescaModels() {
            const response = await models.list()
            this.models = response.data
        },
        async refrescaMetriques() {
            let faseAbr = null
            if (this.fase === this.$t('Training')) faseAbr = 'T'
            else faseAbr = 'I'
            const response = await metriques.listOrderedFilteredByPhase(faseAbr)
            this.metriques = response.data
        },
        async mostrarEtiqueta() {
            let responseCreate = null
            if (this.fase === this.$t('Training'))
                responseCreate = await trainings.create(this.selectedModel, this.metriques)
            else
                responseCreate = await inferencies.create(this.selectedModel, this.metriques)
            if (responseCreate.status === 201) {
                const experiment_id = responseCreate.data['id']
                if (this.fase === this.$t('Training'))
                    this.$router.push({
                        name: 'Label info for training',
                        params: {id_model: this.selectedModel, id_training: experiment_id}
                    })
                else
                    this.$router.push({
                        name: 'Label info for inference',
                        params: {id_model: this.selectedModel, id_inference: experiment_id}
                    })
            }
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