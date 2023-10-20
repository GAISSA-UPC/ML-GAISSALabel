<template>
    <h1>{{ $t("Energy label for") }} {{ fase }}</h1><br>
    <h2>{{ $t("Register a new") }} {{ fase }}</h2><br>

    <el-alert v-if="estat === 'modelCreat-ok'" :title="$t('Model registered correctly')" type="success" @close="estat = ''"/>
    <el-alert v-else-if="estat === 'modelCreat-ko'" :title="$t('There was an error while creating the model')" type="success" @close="estat = ''"/>

    <div>
        <el-form label-position="top">
            <el-form-item :label="$t('Model')">
                <el-select
                    v-model="selectedModel"
                    @change="canviModel"
                >
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
            <el-form-item
                :label="$t('Files')"
            >
                <el-upload
                    v-model:file-list="fileList"
                    multiple
                    drag
                    style="width: 100%"
                    :auto-upload="false"
                >
                    <font-awesome-icon :icon="['fas', 'cloud-arrow-up']" />
                    <div class="el-upload__text">
                        {{ $t('Drop file here or') }} <em>{{ $t('click to upload') }}</em>
                    </div>
                </el-upload>
            </el-form-item>
            <el-button
                @click="mostrarEtiqueta"
                color="var(--gaissa_green)"
                v-show="fileList.length !== 0"
            >
                {{ $t('Generate label') }}
            </el-button>
        </el-form><br>
    </div>

    <DialogNewModel v-model="dialogNewModel"
                    @cancel="dialogNewModel = false"
                    @model-creat-ok="modelCreat()"
                    @model-creat-ko="dialogNewModel = false; estat = 'modelCreat-ko'"
    />

</template>

<script>
import models from '@/services/models'
import trainings from '@/services/trainings'
import inferencies from '@/services/inferencies'
import {formatData} from '@/utils'
import DialogNewModel from "@/components/DialogNewModel.vue";
export default {
    name: "FileNewExperiment",
    props: {
        fase: {required: true, type: String}
    },
    components: {DialogNewModel},
    data() {
        return {
            estat: '',
            models: null,
            selectedModel: null,
            fileList: [],
            dialogNewModel: false,
        };
    },
    methods: {
        async refrescaModels() {
            const response = await models.list()
            this.models = response.data
        },
        async refrescaExperiments() {
            let response = null
            if (this.fase === this.$t('Training')) response = await trainings.listByModel(this.selectedModel)
            else response = await inferencies.listByModel(this.selectedModel)
            this.experiments = response.data
        },
        async canviModel() {
            await this.refrescaExperiments()
            this.selectedExperiment = null
        },
        async mostrarEtiqueta() {
            if (this.fase === this.$t('Training'))
                this.$router.push({
                    name: 'Label info for training',
                    params: {id_model: this.selectedModel, id_training: 1}
                })
            else
                this.$router.push({
                    name: 'Label info for inference',
                    params: {id_model: this.selectedModel, id_inference: 1}
                })

        },
        async modelCreat() {
            await this.refrescaModels()
            this.dialogNewModel = false
            this.selectedModel = this.models.length
            this.estat = 'modelCreat-ok'
        }
    },
    async mounted() {
        await this.refrescaModels();
    },
};
</script>

<style>
</style>