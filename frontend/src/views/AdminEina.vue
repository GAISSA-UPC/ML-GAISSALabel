<template>
    <h1 v-if="creacio">{{ $t("Register calculation tool") }}</h1>
    <h1 v-else>{{ $t("Edit calculation tool") }}</h1>
    <br>

    <el-alert v-if="estat === 'eina-creada-ok'" :title="$t('Calculation tool correctly created')" type="success" @close="estat = '';$route.query.status=''"/>
    <el-alert v-else-if="estat === 'eina-creada-ko'" :title="$t('There was an error while creating the calculation tool')" type="success" @close="estat = ''"/>
    <el-alert v-if="estat === 'eina-update-ok'" :title="$t('Calculation tool correctly updated')" type="success" @close="estat = ''"/>
    <el-alert v-else-if="estat === 'eina-update-ko'" :title="$t('There was an error while updating the calculation tool')" type="success" @close="estat = ''"/>
    <br v-if="estat">

    <el-form label-position="top">
        <div v-if="!creacio">
            <input class="editable_input" v-model="eina.nom"/>
            <br>
        </div>

        <br>
        <h3>{{ $t('General information') }}</h3><br>
        <el-form-item :label="$t('Name')" v-if="creacio">
            <el-input v-model="eina.nom" style="max-width: 300px"/>
        </el-form-item>
        <el-form-item :label="$t('Description')">
            <el-input
                v-model="eina.descripcio"
                type="textarea"
            />
        </el-form-item>
        <br>

        <h2>{{ $t('Transformations') }}</h2><br>
        <el-row style="justify-content: space-between">
            <el-col :span="11">
                <h3>{{ $t('Training metrics') }}</h3><br>
                <el-form-item
                    v-for="(metricaTrain, i) in metriquesTraining" :key="i"
                    :label="metricaTrain.id"
                >
                    <el-input
                        v-model="metricaTrain.transformacio"
                        :placeholder="metricaTrain.id"/>
                </el-form-item>
            </el-col>
            <el-col :span="11">
                <h3>{{ $t('Training information') }}</h3><br>
                <el-form-item
                    v-for="(infoTrain, i) in informacionsTraining" :key="i"
                    :label="infoTrain.id"
                >
                    <el-input v-model="infoTrain.transformacio" :placeholder="infoTrain.id"/>
                </el-form-item>
            </el-col>
        </el-row><br><br>
        <el-row style="justify-content: space-between">
            <el-col :span="11">
                <h3>{{ $t('Inference metrics') }}</h3><br>
                <el-form-item
                    v-for="(metricaInf, i) in metriquesInference" :key="i"
                    :label="metricaInf.id"
                >
                    <el-input
                        v-model="metricaInf.transformacio"
                        :placeholder="metricaInf.id"/>
                </el-form-item>
            </el-col>
            <el-col :span="11">
                <h3>{{ $t('Inference information') }}</h3><br>
                <el-form-item
                    v-for="(infoInf, i) in informacionsInference" :key="i"
                    :label="infoInf.id"
                >
                    <el-input v-model="infoInf.transformacio" :placeholder="infoInf.id"/>
                </el-form-item>
            </el-col>
        </el-row>

        <br><br>
        <el-button
            @click="crearEina"
            color="var(--gaissa_green)"
            v-if="creacio"
        >
            {{ $t('Register calculation tool') }}
        </el-button>
        <el-button
            v-else
            @click="updateEina"
            color="var(--gaissa_green)"
        >
            {{ $t('Update information') }}
        </el-button>
    </el-form><br>

</template>

<script>
import eines from "@/services/eines";
import metriques from "@/services/metriques";
import informacions from "@/services/informacions";
export default {
    name: "AdminEina",
    data() {
        return {
            estat: this.$route.query.status,
            creacio: false,
            eina: {
                "transformacionsMetriques": [],
                "transformacionsInformacions": [],
            },
            editantNom: false,
            metriquesTraining: null,
            metriquesInference: null,
            informacionsTraining: null,
            informacionsInference: null,
        };
    },
    methods: {
        async refrescaEina(id=this.$route.params.id_eina) {
            const response = await eines.getById(id)
            this.eina = response.data
            await this.inicialitzaEina()
        },
        async refrescaMetriques() {
            const response = await metriques.listOrdered()
            const metriquesData = response.data
            metriquesData.forEach(metrica => {
                const transf = this.eina.transformacionsMetriques.filter(transf => transf.metrica === metrica.id)[0]
                if (transf) metrica.transformacio = transf.valor
            })
            this.metriquesTraining = metriquesData.filter(metrica => metrica.fase === 'T')
            this.metriquesInference = metriquesData.filter(metrica => metrica.fase === 'I')
        },
        async refrescaInformacions() {
            const response = await informacions.list()
            const informacionsData = response.data
            informacionsData.forEach(info => {
                const transf = this.eina.transformacionsInformacions.filter(transf => transf.informacio === info.id)[0]
                if (transf) info.transformacio = transf.valor
            })
            this.informacionsTraining = informacionsData.filter(info => info.fase === 'T')
            this.informacionsInference = informacionsData.filter(info => info.fase === 'I')
        },
        async inicialitzaEina() {
            const transfMetriques = this.eina.transformacionsMetriques
            this.eina.transformacionsMetriques = Object.entries(transfMetriques).map(([valor, metrica]) => {
                return {
                    "valor": valor,
                    "metrica": metrica
                };
            });
            const transfInformacions = this.eina.transformacionsInformacions
            this.eina.transformacionsInformacions = Object.entries(transfInformacions).map(([valor, info]) => {
                return {
                    "valor": valor,
                    "informacio": info
                };
            });
        },
        passarTransformacions(metriques, informacions) {
            this.eina.transformacionsMetriques = []
            metriques.forEach(metrica => {
                if (metrica.transformacio && metrica.transformacio !== '') {
                    this.eina.transformacionsMetriques.push({
                        "valor": metrica.transformacio,
                        "metrica": metrica.id
                    })
                }
            })
            this.eina.transformacionsInformacions = []
            informacions.forEach(info => {
                if (info.transformacio && info.transformacio !== '') {
                    this.eina.transformacionsInformacions.push({
                        "valor": info.transformacio,
                        "informacio": info.id
                    })
                }
            })
        },
        async crearEina() {
            this.passarTransformacions(
                this.metriquesTraining.concat(this.metriquesInference),
                this.informacionsTraining.concat(this.informacionsInference)
            )
            const response = await eines.create(this.eina)
            window.scrollTo({top:0})
            if (response.status === 201) {
                this.creacio = false
                this.$router.push({
                    name: "Admin eina edit",
                    params: {id_eina: response.data.id},
                    query: {status: 'eina-creada-ok'}
                })
                this.estat = 'eina-creada-ok'
                await this.refrescaEina(response.data.id)
            } else this.estat = 'eina-creada-ko'
        },
        async updateEina() {
            this.passarTransformacions(
                this.metriquesTraining.concat(this.metriquesInference),
                this.informacionsTraining.concat(this.informacionsInference)
            )
            const response = await eines.update(this.eina)
            if (response.status === 200) {
                this.estat = 'eina-update-ok'
            } else this.estat = 'eina-update-ko'
            window.scrollTo({top:0})
        }
    },
    async mounted() {
        this.creacio = !this.$route.params.id_eina       // Si hi ha paràmetre de id eina vol dir que estem editant, si no, creant.
        if (!this.creacio) await this.refrescaEina()
        await this.refrescaMetriques()
        await this.refrescaInformacions()
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