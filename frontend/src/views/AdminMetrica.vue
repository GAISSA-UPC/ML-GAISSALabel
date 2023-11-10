<template>
    <h1 v-if="creacio">{{ $t("Register") }} {{ getFase }} {{ $t("metric") }}</h1>
    <h1 v-else>{{ $t("Edit") }} {{ getFase }} {{ $t("metric") }}</h1>
    <br>

    <el-alert v-if="estat === 'metrica-creada-ok'" :title="$t('Metric correctly created')" type="success" @close="estat = '';$route.query.status=''"/>
    <el-alert v-else-if="estat === 'metrica-creada-ko'" :title="$t('There was an error while creating the metric')" type="success" @close="estat = ''"/>
    <el-alert v-if="estat === 'metrica-update-ok'" :title="$t('Metric correctly updated')" type="success" @close="estat = ''"/>
    <el-alert v-else-if="estat === 'metrica-update-ko'" :title="$t('There was an error while updating the metric')" type="success" @close="estat = ''"/>
    <br v-if="estat">

    <el-form label-position="top">
        <div v-if="!creacio">
            <input class="editable_input" v-model="metrica.nom"/>
            <br>
        </div>

        <br>
        <h3>{{ $t('General information') }}</h3><br>
        <el-form-item :label="$t('Name')" v-if="creacio">
            <el-input v-model="metrica.nom" style="max-width: 300px"/>
        </el-form-item>
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
        <el-row v-for="(qualif, i) in qualificacions" :key="i" align="bottom">
            <el-form-item :label="$t('Lower boundary')">
                <el-input-number
                    step="0.1" min="0" max="100000000000000000000"
                    v-model="metrica.intervals.find(interval => interval.qualificacio === qualif.id).limitInferior"
                    style="width: 200px"
                    v-if="metrica.intervals"
                />
            </el-form-item>
            <p :style="{ fontSize: '40px', fontWeight: 'bold', color: qualif.color, width: '30px', marginRight: '20px', marginLeft:'20px'}">
                {{ qualif.id }}
            </p>
            <el-form-item :label="$t('Upper boundary')">
                <el-input-number
                    step="0.1" min="0" max="100000000000000000000"
                    v-model="metrica.intervals.find(interval => interval.qualificacio === qualif.id).limitSuperior"
                    style="width: 200px"
                    v-if="metrica.intervals"
                />
            </el-form-item>
        </el-row>


        <br><br>
        <el-button
            @click="crearMetrica"
            color="var(--gaissa_green)"
            v-if="creacio"
        >
            {{ $t('Register metric') }}
        </el-button>
        <el-button
            v-else
            @click="updateMetrica"
            color="var(--gaissa_green)"
        >
            {{ $t('Update information') }}
        </el-button>
    </el-form><br>

</template>

<script>
import metriques from "@/services/metriques";
export default {
    name: "AdminMetrica",
    data() {
        return {
            estat: this.$route.query.status,
            creacio: false,
            metrica: {
                'pes': 0,
                'influencia': 'N',
                'fase': this.$route.query.fase,
            },
            qualificacions: null,
            editantNom: false,
        };
    },
    computed: {
        getFase() {
            return (this.metrica.fase === 'T') ? this.$t('training') : this.$t('inference')
        },
    },
    methods: {
        async refrescaQualificacions() {
            const response = await metriques.listQualificacionsOrdre()
            this.qualificacions = response.data
        },
        async refrescaMetrica(id=this.$route.params.id_metrica) {
            const response = await metriques.getById(id)
            this.metrica = response.data
        },
        async inicialitzaMetrica() {
            this.metrica.intervals = []
            for (let qualificacio of this.qualificacions) {
                this.metrica.intervals.push({
                    'qualificacio': qualificacio.id
                })
            }
        },
        async crearMetrica() {
            const id = this.metrica.nom.toLowerCase().replace(/\s+/g, '_')
            this.metrica.id = id
            const response = await metriques.create(this.metrica)
            window.scrollTo({top:0})
            if (response.status === 201) {
                this.creacio = false
                this.$router.push({
                    name: "Admin mètrica edit",
                    params: {id_metrica: this.metrica.id},
                    query: {status: 'metrica-creada-ok'}
                })
                this.estat = 'metrica-creada-ok'
                await this.refrescaMetrica(this.metrica.id)
            } else this.estat = 'metrica-creada-ko'
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
        await this.refrescaQualificacions()
        if (this.creacio) {
            await this.inicialitzaMetrica()
        } else {
            await this.refrescaMetrica()
        }
    },
}
</script>

<style scoped>
.editable_input {
    border: none;
    background: none;
    font-size: 24px;
    outline: none;
    color: inherit;
}
</style>