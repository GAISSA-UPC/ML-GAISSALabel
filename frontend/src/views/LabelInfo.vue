<template>
    <h1>{{ $t("Energy label for training") }}</h1><br>

    <el-row justify="space-between">
        <el-col :span="13">
            <el-descriptions
                class="margin-top"
                border
            >
                <el-descriptions-item>
                    <template #label>
                        <div class="cell-item">
                            <font-awesome-icon :icon="['fas', 'bars']" />
                            {{ $t('Model name') }}
                        </div>
                    </template>
                    hola
                </el-descriptions-item>
            </el-descriptions>
            model:
                id
                name
                information
                data creació
            training/inference
                id
                dataRegistre
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
            </el-col>
            <el-col :span="3" align="middle">
                <p class="prova" :style="{ fontSize: '35px', fontWeight: 'bold', color: info.color }">{{ info.qualificacio }}</p>
                <p style="font-size: 20px">{{ roundIfDecimal(info.value) }} <span v-if="info.unit">{{ info.unit }}</span> </p>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import trainings from '@/services/trainings'
import metriques from "@/services/metriques";
import EnergyLabel from "@/components/EnergyLabel.vue";
import CustomSlider from "@/components/CustomSlider.vue";
export default {
    name: "LabelInfo",
    components: {CustomSlider, EnergyLabel},
    data() {
        return {
            labelBase64: null,
            resultats: null,
            metriques: null,
            marks: {},
            inf: {},
            ranges: {},
            descripcions: {},
        };
    },
    methods: {
        async aconseguirEtiqueta() {
            const response = await trainings.retrieve(this.$route.params.id_model, this.$route.params.id_training)
            this.labelBase64 = response.data['energy_label']
            this.resultats = response.data['resultats']
            console.log(this.resultats)
            console.log(response.data)
        },
        async aconseguirInfoMetriques() {
            const response = await metriques.listOrderedFilteredByPhase('T')
            this.metriques = response.data
            console.log(this.metriques)
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
            })
        },
        getImageDecoded(img) {
            return `data:image/png;base64,${img}`
        },
        roundIfDecimal(value) {
            return Number.isInteger(value) ? value : value.toFixed(2);
        }
    },
    async mounted() {
        await this.aconseguirEtiqueta()
        await this.aconseguirInfoMetriques()
        await this.calculateVariables()
    },
};
</script>

<style>
</style>