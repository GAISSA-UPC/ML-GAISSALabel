<template>
    <h1>{{ $t("Energy label for inference") }}</h1><br>
    <h2>{{ $t("Register a new inference") }}</h2><br>

    <p style="font-size: 20px">{{ $t('This page allows you to consult the energy efficiency of your model\'s Inferences. To do so, GAISSALabel is going to directly inference your model.') }}</p>
    <br>

    <div v-if="estat">
        <el-alert v-if="estat === 'inference-ko'"
                  :title="$t('There was an error while trying to inference the model you provided. Review both endpoint and input provided.')"
                  type="error" @close="estat = ''"/>
        <br>
    </div>

    <el-form label-position="top">
        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Endpoint where the model is deployed") }}</h3>
        <p>{{ $t('First, indicate the endpoint where your model is deployed. Please, make sure this endpoint does not require access credentials or any security validation') }}</p><br>
        <el-form-item>
            <el-input v-model="endpoint"/>
        </el-form-item>
        <br>
        <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Input for the inference") }}</h3>
        <p>{{ $t('Now, give one example of input that your model can handle. For now, this functionality is restricted only to text inputs.') }}</p><br>
        <el-form-item>
            <el-input type="textarea" v-model="input"/>
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
import calculadors from '@/controllers/calculadors'
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