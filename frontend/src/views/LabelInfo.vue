<template>
    <h1>{{ $t("Energy label for training") }}</h1><br>

    <el-row>
        <el-col :span="14">
            hola
        </el-col>
        <el-col :span="10">
            <EnergyLabel
                :pdfBase64="labelBase64"
            />
        </el-col>
    </el-row>

    <div v-for="(info, metrica, i) in info" :key="i" style="margin-bottom: 30px">
        <el-row justify="space-between" align="middle">
            <el-col :span="5">
                <el-image :src="getImageDecoded(info.image)" :alt="metrica"/>
            </el-col>
            <el-col :span="18">
                <p align="justify">Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>
                <CustomSlider :marks="marks[metrica]" :max="inf[metrica]" :values="ranges[metrica]" :color="info.color"/>
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
            info: null,
            metriques: null,
            marks: {},
            inf: {},
            ranges: {},
            color: {'co2_eq_emissions': '#f8b830', 'downloads': '#ef7d29'}
        };
    },
    methods: {
        async aconseguirEtiqueta() {
            const response = await trainings.retrieve(1, 1)
            this.labelBase64 = response.data['energy_label']
            this.info = response.data['resultats']
            console.log(this.info)
        },
        async aconseguirInfoMetriques() {
            const response = await metriques.listOrderedFilteredByPhase('T')
            this.metriques = response.data
            console.log(this.metriques)
        },
        async calcularMarks() {
            this.metriques.forEach(metrica => {
                const intervals = metrica['intervals']
                let marks = {0: '',}
                let last = 0
                intervals.reverse().forEach(interval => {
                    const limSup = interval['limitSuperior']
                    const limInf = interval['limitInferior']
                    if (limSup !== 100000000000000000000) {
                        last = interval['limitSuperior']
                        marks[last] = ''//interval['limitSuperior'].toFixed(2)
                    }
                    if (limSup > this.info[metrica.id].value && this.info[metrica.id].value > limInf) {
                        this.ranges[metrica.id] = [limInf, limSup]
                    }
                })
                const toAdd = last/(intervals.length - 1) + last
                marks[toAdd] = ''//toAdd.toFixed(2)
                this.marks[metrica.id] = marks
                this.inf[metrica.id] = toAdd
            })
        },
        getImageDecoded(img) {
            return `data:image/png;base64,${img}`
        },
    },
    async mounted() {
        await this.aconseguirEtiqueta()
        await this.aconseguirInfoMetriques()
        await this.calcularMarks()
    },
};
</script>

<style>
</style>