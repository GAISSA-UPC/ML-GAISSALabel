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
        <!-- ToDo -->

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
export default {
    name: "AdminEina",
    data() {
        return {
            estat: this.$route.query.status,
            creacio: false,
            eina: {},
            editantNom: false,
        };
    },
    methods: {
        async refrescaEina(id=this.$route.params.id_eina) {
            const response = await eines.getById(id)
            this.eina = response.data
            this.inicialitzaEina()
        },
        async inicialitzaEina() {
            const transfMetriques = this.eina.transformacionsMetriques
            this.eina.transformacionsMetriques = Object.entries(transfMetriques).map(([valor, metrica]) => {
                return {
                    "valor": valor,
                    "metrica": metrica
                };
            });
            const transfInformacionns = this.eina.transformacionsInformacions
            this.eina.transformacionsInformacions = Object.entries(transfInformacionns).map(([valor, info]) => {
                return {
                    "valor": valor,
                    "informacio": info
                };
            });
        },
        async crearEina() {
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