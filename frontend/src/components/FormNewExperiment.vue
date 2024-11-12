<template>
    <h1>{{ $t("Energy label for") }} {{ fase }}</h1><br>
    <h2>{{ $t("Register a new") }} {{ fase }}</h2><br>

    <div v-if="estat">
        <el-alert v-if="estat === 'modelCreat-ok'" :title="$t('Model registered correctly')" type="success" @close="estat = ''"/>
        <el-alert v-else-if="estat === 'modelCreat-ko'" :title="$t('There was an error while creating the model')" type="error" @close="estat = ''"/>
        <el-alert v-else-if="estat === 'select-model'" :title="$t('Please, select (or create) some model')" type="error" @close="estat = ''"/>
        <br>
    </div>

    <p style="font-size: 20px">{{ $t('This page allows you to evaluate the energy efficiency of your models\'') }} {{ fase }}s. {{ $t('You may go through the following sections to provide the necessary information.') }}</p>
    <br>

    <el-form label-position="top">
        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Model") }}</h3>
        <p>{{ $t('First, please indicate the model you are working with. If it is a new one or not listed above, you can register a new model.') }}</p><br>
        <el-form-item>
            <el-select v-model="selectedModel" filterable>
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

        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Metrics") }}</h3>
        <p>{{ $t('Next, introduce the results for each of the metric you have described. Please, try to compute all of them, to accomplish a more accurate efficiency study.') }}</p><br>
        <el-form-item
            v-for="(metrica, i) in metriques" :key="i"
            :label="metrica.nom"
        >
            <el-input-number
                step="0.01"
                v-model="metrica.valor"
                min="0"
                style="width: 200px"
            />
            <p style="margin-left: 10px">{{ metrica.unitat }}</p>
            <el-alert v-if="metrica.calcul" type="info" show-icon :closable="false" style="margin-top: 10px">
                <p style="font-size: 14px">{{ metrica.calcul }}</p>
            </el-alert>
        </el-form-item>
        <br>

        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Additional information") }}</h3>
        <p>{{ $t('Finally, if you want, you can add some additional information related to the experiment. This information will not be taken into account when generating the efficiency result, but may be interesting for you or other developers to know.') }}</p><br>
        <el-form-item
            v-for="(infoAdd, i) in informacions" :key="i"
            :label="infoAdd.nom"
        >
            <el-select
                v-if="infoAdd.opcions_list"
                v-model="infoAdd.valor"
                clearable
            >
                <el-option
                    v-for="(opcio, i) in infoAdd.opcions_list" :key="i"
                    :value="opcio"
                    :label="opcio"
                />
            </el-select>
            <el-input
                style="max-width: 195px"
                v-else
                v-model="infoAdd.valor"
            />
        </el-form-item>
        <br>
        <el-button
            ref="generateLabelButton"
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
import models from '@/controllers/models'
import metriques from '@/controllers/metriques'
import informacions from "@/controllers/informacions";
import inferencies from '@/controllers/inferencies'
import trainings from '@/controllers/trainings'
import DialogNewModel from "@/components/DialogNewModel.vue";
export default {
    name: "FormNewExperiment",
    components: {DialogNewModel},
    props: {
        fase: {required: true, type: String},
        dadesInicials: {required: false, type: Object, default: null},
    },
    data() {
        return {
            estat: '',
            models: null,
            selectedModel: null,
            newModel: {},
            dialogNewModel: false,
            metriques: null,
            informacions: null,
        };
    },
    methods: {
        async refrescaModels() {
            const response = await models.list()
            this.models = response.data
        },
        async refrescaMetriques() {
            const faseAbr = (this.fase === this.$t('Training'))? 'T' : 'I'
            const response = await metriques.listOrderedFilteredByPhase(faseAbr)
            this.metriques = response.data
        },
        async refrescaInformacions() {
            const faseAbr = (this.fase === this.$t('Training'))? 'T' : 'I'
            const response = await informacions.listFilteredByPhase(faseAbr)
            this.informacions = response.data
        },
        async inicialitzarMetriques() {
            this.metriques.forEach((metrica) => {
                if (metrica.id in this.dadesInicials) {
                    metrica.valor = this.dadesInicials[metrica.id]
                }
            })
        },
        async inicialitzarInformacions() {
            this.informacions.forEach((informacio) => {
                if (informacio.id in this.dadesInicials) {
                    informacio.valor = this.dadesInicials[informacio.id]
                }
            })
        },
        async mostrarEtiqueta() {
            if (this.selectedModel) {
                let responseCreate = null
                if (this.fase === this.$t('Training'))
                    responseCreate = await trainings.create(this.selectedModel, this.metriques, this.informacions)
                else
                    responseCreate = await inferencies.create(this.selectedModel, this.metriques, this.informacions)
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
            } else {
                this.estat = 'select-model'
                window.scrollTo({top:0})
            }
        },
    },
    async mounted() {
        await this.refrescaModels();
        await this.refrescaMetriques();
        await this.refrescaInformacions();
        if (this.dadesInicials) {
            await this.inicialitzarMetriques();
            await this.inicialitzarInformacions();
        }
    },
};
</script>

<style>
p {
    font-size: 18px
}
</style>