<template>
    <el-alert v-if="estat === 'sincro-ok'" :title="$t('The synchronization was successful!')" type="success" @close="estat = ''"/>
    <el-alert v-else-if="estat === 'sincro-ko'" :title="$t('There was an error while synchronizing the database. Please, try again later.')" type="error" @close="estat = ''"/>
    <br v-if="estat">

    <h1>{{ $t("Database Synchronization") }}</h1><br>

    <p>{{ $t("In this page you can synchronize the database of models and their corresponding trainings with the ones \
    that are registered in the following providers: ") }}</p><br>

    <ul style="margin-left: 40px">
        <li>Hugging Face</li>
    </ul><br>

    <p>{{ $t("Be aware that the process of synchronization may take up to 5 minutes in some cases.") }}</p><br>

    <el-button @click="sincronitzar"
               color="var(--gaissa_green)"
    >
        {{ $t('Synchronize') }}
    </el-button>

    <br><br><br>

    <div v-if="createdModels" >
        <h2 style="color: var(--gaissa_green);font-weight: bold">{{ $t('Created models') }}</h2><br>
        <p v-if="createdModels.length === 0">{{ $t('There were no models created. There were all already registered.') }}</p>
        <ul style="margin-left: 40px" v-else>
            <li v-for="(model, i) in createdModels" :key="i">{{model}}</li>
        </ul>
        <br><br>
    </div>
    <div v-if="updatedModels">
        <h2 style="color: var(--gaissa_green);font-weight: bold">{{ $t('Updated models') }}</h2><br>
        <p v-if="updatedModels.length === 0">{{ $t('There were no models updated. There were all already up to date.') }}</p>
        <ul style="margin-left: 40px" v-else>
            <li v-for="(model, i) in updatedModels" :key="i">{{model}}</li>
        </ul><br><br>
    </div>

</template>


<script>
import sincronitzacions from "@/services/sincronitzacions";
import { ElLoading } from 'element-plus'

export default {
    name: "AdminSincro",
    data() {
        return {
            estat: '',
            createdModels: null,
            updatedModels: null,
        }
    },
    methods: {
        async sincronitzar() {
            const loading = ElLoading.service({
                lock: true,
                text: this.$t('Synchronizing'),
                background: 'rgba(0, 0, 0, 0.7)',
            })
            const response = await sincronitzacions.sincronitzar()
            loading.close()
            if (response.status === 200) {
                this.estat = 'sincro-ok'
                this.createdModels = response.data['Created models']
                this.updatedModels = response.data['Updated models']
            } else {
                this.estat = 'sincro-ko'
            }
        },
    },
    async mounted() {
    },
}


</script>

<style scoped>

</style>