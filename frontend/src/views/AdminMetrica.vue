<template>
    <h1>{{ $t("Edit") }} {{ getFase }} {{ $t("metric") }}</h1><br>
    <h2>{{ metrica.nom }}</h2><br>

    <el-alert v-if="estat === 'metrica-update-ok'" :title="$t('Metric correctly updated')" type="success" @close="estat = ''"/>
    <el-alert v-else-if="estat === 'metrica-update-ko'" :title="$t('There was an error while updating the metric')" type="success" @close="estat = ''"/>

    <br>
    <h3>{{ $t('General information') }}</h3><br>
    <el-form label-position="top">
        <el-form-item :label="$t('Description')">
            <el-input
                v-model="metrica.descripcio"
                type="textarea"
            />
        </el-form-item>
        <el-form-item :label="$t('Weight')">
            <el-input-number
                step="0.01"
                v-model="metrica.pes"
                min="0"
                max="1"
            />
        </el-form-item>
        <el-form-item :label="$t('Unit')">
            <el-input v-model="metrica.unitat" style="max-width: 150px"/>
        </el-form-item>
        <el-form-item :label="$t('Influence')">
            <el-select v-model="metrica.influencia" style="max-width: 150px">
                <el-option
                    value="N"
                    :label="$t('Negative')"
                />
                <el-option
                    value="P"
                    :label="$t('Positive')"
                />
            </el-select>
        </el-form-item>
        <br>

        <h3>{{ $t('Intervals') }}</h3><br>


        <br><br>
        <el-button
            @click="updateMetrica"
            color="var(--gaissa_green)"
        >
            {{ $t('Actualitzar informació') }}
        </el-button>
    </el-form><br>

</template>

<script>
import metriques from "@/services/metriques";
export default {
    name: "AdminMetrica",
    data() {
        return {
            estat: null,
            creacio: false,
            fase: '',
            metrica: {
                'pes': 0,
                'influencia': 'N',
            },
        };
    },
    computed: {
        getFase() {
            return (this.metrica.fase === 'T') ? this.$t('training') : this.$t('inference')
        }
    },
    methods: {
        async refrescaMetrica() {
            const response = await metriques.getById(this.$route.params.id_metrica)
            this.metrica = response.data
            console.log(this.metrica)
        },
        async updateMetrica() {
            const response = await metriques.update(this.metrica)
            if (response.status === 200) {
                this.estat = 'metrica-update-ok'
            } else this.estat = 'metrica-update-ko'
            window.scrollTo({top:0})
        }
    },
    async mounted() {
        this.creacio = !this.$route.params.id_metrica       // Si hi ha paràmetre de id mètrica vol dir que estem editant, si no, creant.
        if (this.creacio) {
            console.log("creacio")
        } else {
            this.refrescaMetrica()
        }
    }
}
</script>

<style scoped>

</style>