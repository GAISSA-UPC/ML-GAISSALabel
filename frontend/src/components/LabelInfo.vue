<template>
    <h1>{{ $t("Energy label for") }} {{ fase }}</h1><br>

    <el-row justify="space-between">
        <el-col :span="13">
            <el-descriptions
                class="margin-top"
                border
                :column="1"
                v-if="model"
            >
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <font-awesome-icon :icon="['fas', 'id-card-clip']" />
                            {{ $t('Model name') }}
                        </div>
                    </template>
                    {{ model.nom }}
                </el-descriptions-item>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <font-awesome-icon :icon="['fas', 'circle-info']" />
                            {{ $t('Model information') }}
                        </div>
                    </template>
                    {{ model.informacio }}
                </el-descriptions-item>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <font-awesome-icon :icon="['fas', 'calendar-days']" />
                            {{ $t('Model creation date') }}
                        </div>
                    </template>
                    {{ formatData(model.dataCreacio) }}
                </el-descriptions-item>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <font-awesome-icon :icon="['fas', 'dumbbell']" v-if="fase === $t('Training')" />
                            <font-awesome-icon :icon="['fas', 'bullseye']" v-else />
                            {{ fase }} {{ $t('identifier') }}
                        </div>
                    </template>
                    {{ info.id }}
                </el-descriptions-item>
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <font-awesome-icon :icon="['fas', 'calendar-days']" />
                            {{ fase }} {{ $t('registration date') }}
                        </div>
                    </template>
                    {{ formatData(info.dataRegistre) }}
                </el-descriptions-item>
                <el-descriptions-item v-for="(camps, infoAdd, i) in infoAddicional" :key="i">
                    <template #label>
                        <div class="cell-item">
                            <font-awesome-icon :icon="['fas', 'circle-info']" />
                            {{ camps.nom }}
                        </div>
                    </template>
                    {{ camps.valor }}
                </el-descriptions-item>
            </el-descriptions>
        </el-col>
        <el-col :span="10">
            <EnergyLabel
                :pdfBase64="labelBase64"
            />
        </el-col>
    </el-row>

    <div v-for="(info, metrica, i) in resultats" :key="i" style="margin-bottom: 40px">
        <el-row align="middle">
            <el-col :span="5">
                <el-image :src="getImageDecoded(info.image)" :alt="metrica"/>
            </el-col>
            <el-col :span="1"/>     <!-- Just to create space -->
            <el-col :span="15">
                <h3 style="font-weight: bold;margin-bottom: 6px">{{info.nom}}</h3>
                <p align="justify">{{ descripcions[metrica] }}</p>
                <CustomSlider :marks="marks[metrica]" :max="inf[metrica]" :values="ranges[metrica]" :color="info.color"/>
                <p align="justify">{{ recomanacions[metrica] }}</p>
            </el-col>
            <el-col :span="3" align="middle">
                <p :style="{ fontSize: '35px', fontWeight: 'bold', color: info.color }">{{ info.qualificacio }}</p>
                <p style="font-size: 20px">{{ roundIfDecimal(info.value) }} <span v-if="info.unit">{{ info.unit }}</span> </p>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import trainings from '@/services/trainings'
import inferencies from '@/services/inferencies'
import metriques from "@/services/metriques";
import models from '@/services/models'
import EnergyLabel from "@/components/EnergyLabel.vue";
import CustomSlider from "@/components/CustomSlider.vue";
import {formatData} from '@/utils'
export default {
    name: "LabelInfo",
    components: {CustomSlider, EnergyLabel},
    props: {
        fase: {required: true, type: String}
    },
    data() {
        return {
            labelBase64: null,
            resultats: null,
            infoAddicional: null,
            info: null,
            model: null,
            metriques: null,
            marks: {},
            inf: {},
            ranges: {},
            descripcions: {},
            recomanacions: {},
        };
    },
    methods: {
        async refrescaDadesExperiment() {
            let response = null
            if (this.fase === this.$t('Training')) {
                response = await trainings.retrieve(this.$route.params.id_model, this.$route.params.id_training)
                this.info = response.data['infoEntrenament']
            }
            else {
                response = await inferencies.retrieve(this.$route.params.id_model, this.$route.params.id_inference)
                this.info = response.data['infoInferencia']
            }
            this.labelBase64 = response.data['energy_label']
            this.resultats = response.data['resultats']
            this.infoAddicional = this.info['infoAddicional']
        },
        async refrescaInfoMetriques() {
            const faseAbr = (this.fase === 'Training') ? 'T' : 'I'
            const response = await metriques.listOrderedFilteredByPhase(faseAbr)
            this.metriques = response.data
        },
        async refrescaInfoModel() {
            const response = await models.retrieve(this.$route.params.id_model)
            this.model = response.data
        },
        async calculateVariables() {
            this.metriques.forEach(metrica => {
                const intervals = metrica['intervals']
                let marks = {0: '',}
                let last = 0
                let toAdd = 0
                intervals.reverse().forEach(interval => {
                    const limSup = interval['limitSuperior']
                    const limInf = interval['limitInferior']
                    if (limSup === 100000000000000000000) {
                        toAdd = last/(intervals.length - 1) + last
                        marks[toAdd] = ''//toAdd.toFixed(2)
                    }
                    else {
                        last = interval['limitSuperior']
                        marks[last] = ''//interval['limitSuperior'].toFixed(2)
                    }
                    if (limSup > this.resultats[metrica.id].value && this.resultats[metrica.id].value > limInf) {
                        if (limSup === 100000000000000000000) this.ranges[metrica.id] = [limInf, toAdd]
                        else this.ranges[metrica.id] = [limInf, limSup]
                    }
                })
                this.marks[metrica.id] = marks
                this.inf[metrica.id] = toAdd
                this.descripcions[metrica.id] = metrica.descripcio
                this.recomanacions[metrica.id] = metrica.recomanacions
            })
        },
        getImageDecoded(img) {
            return `data:image/png;base64,${img}`
        },
        roundIfDecimal(value) {
            return Number.isInteger(value) ? value : value.toFixed(2);
        },
        formatData,
    },
    async mounted() {
        await this.refrescaDadesExperiment()
        await this.refrescaInfoMetriques()
        await this.refrescaInfoModel()
        await this.calculateVariables()
    },
};
</script>

<style>
</style>