<template>
    <h1>{{ $t("Energy label for inference") }}</h1><br>
    <h2>{{ $t("Register a new inference") }}</h2><br>

    <div v-if="estat">
        <el-alert v-if="estat === 'inference-ko'"
                  :title="$t('There was an error while trying to inference the model you provided. Review both endpoint and input provided.')"
                  type="error" @close="estat = ''"/>
        <br>
    </div>

    <el-form label-position="top">
        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Endpoint where the model is deployed") }}</h3><br>
        <el-form-item>
            <el-input v-model="endpoint"/>
        </el-form-item>
        <br>
        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Input for the inference") }}</h3><br>
        <el-form-item>
            <el-input v-model="input"/>
        </el-form-item>
        <br>
        <el-button
            @click="calcularEficiencia"
            color="var(--gaissa_green)"
        >
            {{ $t('Calculate efficiency') }}
        </el-button>
    </el-form><br>

</template>

<script>
import calculadors from '@/services/calculadors'
export default {
    name: "InferenceDeploy",
    data() {
        return {
            endpoint: null,
            input: null,
            estat: '',
        };
    },
    methods: {
        async calcularEficiencia() {
            const resultats = await calculadors.calcularEficienciaInferencia(this.endpoint, this.input)
            console.log(resultats.status)
            if (resultats.status === 201) {
                this.$router.push({
                    name: 'inference form',
                    query: {dadesInicials: JSON.stringify(resultats.data)}
                })
            } else {
                this.estat = 'inference-ko'
                window.scrollTo({top:0})
            }
        }
    }
}
</script>

<style scoped>

</style>