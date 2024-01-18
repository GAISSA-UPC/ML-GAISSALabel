<template>
    <h1 v-if="creacio">{{ $t("Register") }} {{ getFase }} {{ $t("additional information") }}</h1>
    <h1 v-else>{{ $t("Edit") }} {{ getFase }} {{ $t("additional information") }}</h1>
    <br>

    <el-alert v-if="estat === 'informacio-creada-ok'" :title="$t('Additional information correctly created')" type="success" @close="estat = '';$route.query.status=''"/>
    <el-alert v-else-if="estat === 'informacio-creada-ko'" :title="$t('There was an error while creating the additional information')" type="success" @close="estat = ''"/>
    <el-alert v-if="estat === 'informacio-update-ok'" :title="$t('Additional information correctly updated')" type="success" @close="estat = ''"/>
    <el-alert v-else-if="estat === 'informacio-update-ko'" :title="$t('There was an error while updating the additional information')" type="success" @close="estat = ''"/>
    <br v-if="estat">

    <el-form label-position="top">
        <div v-if="!creacio">
            <input class="editable_input" v-model="informacio.nom"/>
            <br>
        </div>

        <br>
        <h3>{{ $t('General information') }}</h3><br>
        <el-form-item :label="$t('Name')" v-if="creacio">
            <el-input v-model="informacio.nom" style="max-width: 300px"/>
        </el-form-item>
        <el-form-item :label="$t('Description')">
            <el-input
                v-model="informacio.descripcio"
                type="textarea"
            />
        </el-form-item>
        <el-form-item :label="$t('Options (separated by ;)')">
            <el-input v-model="informacio.opcions" style="max-width: 300px"/>
        </el-form-item>
        <br>

        <el-button
            @click="crearInformacio"
            color="var(--gaissa_green)"
            v-if="creacio"
        >
            {{ $t('Register additional information') }}
        </el-button>
        <el-button
            v-else
            @click="updateInformacio"
            color="var(--gaissa_green)"
        >
            {{ $t('Update information') }}
        </el-button>
    </el-form><br>

</template>

<script>
import informacions from "@/controllers/informacions";
export default {
    name: "AdminInformacio",
    data() {
        return {
            estat: this.$route.query.status,
            creacio: false,
            informacio: {
                'fase': this.$route.query.fase,
            },
            editantNom: false,
        };
    },
    computed: {
        getFase() {
            return (this.informacio.fase === 'T') ? this.$t('training') : this.$t('inference')
        },
    },
    methods: {
        async refrescaInformacio(id=this.$route.params.id_informacio) {
            const response = await informacions.getById(id)
            this.informacio = response.data
        },
        async crearInformacio() {
            const id = this.informacio.nom.toLowerCase().replace(/\s+/g, '_')
            this.informacio.id = id
            const response = await informacions.create(this.informacio)
            window.scrollTo({top:0})
            if (response.status === 201) {
                this.creacio = false
                this.$router.push({
                    name: "Admin informació edit",
                    params: {id_informacio: this.informacio.id},
                    query: {status: 'informacio-creada-ok'}
                })
                this.estat = 'informacio-creada-ok'
                await this.refrescaInformacio(this.informacio.id)
            } else this.estat = 'informacio-creada-ko'
        },
        async updateInformacio() {
            const response = await informacions.update(this.informacio)
            if (response.status === 200) {
                this.estat = 'informacio-update-ok'
            } else this.estat = 'informacio-update-ko'
            window.scrollTo({top:0})
        }
    },
    async mounted() {
        this.creacio = !this.$route.params.id_informacio       // Si hi ha paràmetre de id informació vol dir que estem editant, si no, creant.
        if (!this.creacio) await this.refrescaInformacio()
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