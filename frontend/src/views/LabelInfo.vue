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
            </el-col>
        </el-row>
    </div>
</template>

<script>
import trainings from '@/services/trainings'
import EnergyLabel from "@/components/EnergyLabel.vue";
export default {
    name: "LabelInfo",
    components: {EnergyLabel},
    data() {
        return {
            labelBase64: null,
            info: null,
        };
    },
    methods: {
        async aconseguirEtiqueta() {
            const response = await trainings.retrieve(1, 1)
            this.labelBase64 = response.data['energy_label']
            this.info = response.data['resultats']
        },
        getImageDecoded(img) {
            return `data:image/png;base64,${img}`
        }
    },
    async mounted() {
        await this.aconseguirEtiqueta();
    },
};
</script>

<style>
</style>