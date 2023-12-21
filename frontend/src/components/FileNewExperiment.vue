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
                    :show-file-list="false"
                >
                    <font-awesome-icon :icon="['fas', 'cloud-arrow-up']" />
                    <div class="el-upload__text">
                        {{ $t('Drop file here or') }} <em>{{ $t('click to upload') }}</em>
                    </div>
                </el-upload>

                <ul class="el-upload-list el-upload-list--text" style="width: 100%">
                    <li v-for="(file, index) in fileList" :key="index" class="el-upload-list__item is-ready" tabindex="0">
                        <div class="el-upload-list__item-info">
                            <a class="el-upload-list__item-name">
                                <i class="el-icon el-icon--document">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                                        <path fill="currentColor" d="M832 384H576V128H192v768h640zm-26.496-64L640 154.496V320zM160 64h480l256 256v608a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32m160 448h384v64H320zm0-192h160v64H320zm0 384h384v64H320z"></path>
                                    </svg>
                                </i>
                                <span class="el-upload-list__item-file-name" :title="file.name">{{ file.name }}</span>
                                <el-select style="margin-left: 10px" v-model="file.tool" :placeholder="$t('Tool used')" :clearable="true">
                                    <el-option key="hola" label="hola" value="hola" />
                                </el-select>
                            </a>
                        </div>
                        <el-button class="el-icon el-icon--close" @click="fileList.splice(index, 1)">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                                <path fill="currentColor" d="M764.288 214.592 512 466.88 259.712 214.592a31.936 31.936 0 0 0-45.12 45.12L466.752 512 214.528 764.224a31.936 31.936 0 1 0 45.12 45.184L512 557.184l252.288 252.288a31.936 31.936 0 0 0 45.12-45.12L557.12 512.064l252.288-252.352a31.936 31.936 0 1 0-45.12-45.184z"></path>
                            </svg>
                        </el-button>
                    </li>
                </ul>
            </el-form-item>
            <el-button
                @click="gestioFitxers"
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
import DialogNewModel from "@/components/DialogNewModel.vue";
import * as XLSX from "xlsx";
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
        async refrescaEines() {

        },
        async canviModel() {
            await this.refrescaExperiments()
            this.selectedExperiment = null
        },
        async gestioFitxers() {
            const info = await this.carregarFitxers()
            const nameRouter = (this.fase === this.$t('Training')) ? 'training form' : 'inference form'
            this.$router.push({
                name: nameRouter,
                query: {dadesInicials: JSON.stringify(info)}
            })
        },
        // Funció per carregar fitxers i reestructurar tota la info en un sol JSON.
        async carregarFitxers() {
            // Creem una promesa x cada fitxers, perquè es faci paral·lelament
            const promises = Array.from(this.fileList).map((file) => {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        const contingut = event.target.result;
                        // Agafem només la info de la primera fila
                        const contingutFormatted = this.parseExcelJSON(contingut)[0];
                        resolve(contingutFormatted);
                    };
                    reader.onerror = reject;
                    reader.readAsBinaryString(file.raw);
                });
            });
            try {
                // Recollim totes les promeses i les ajuntem en un sol JSON (info)
                const info = await Promise.all(promises);
                return info.reduce((acc, data) => ({ ...acc, ...data }), {});
            } catch (error) {
                console.error("Error carregant els fitxers:", error);
            }
        },
        parseExcelJSON(contingut) {
            const data = XLSX.read(contingut, { type: 'binary' });
            const camps = data.Sheets[data.SheetNames[0]];
            const jsonData = XLSX.utils.sheet_to_json(camps);
            return jsonData;
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