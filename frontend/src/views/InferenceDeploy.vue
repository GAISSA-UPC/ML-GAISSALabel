<template>
    <h1>{{ $t("Energy label for inference") }}</h1><br>
    <h2>{{ $t("Register a new inference") }}</h2><br>

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
        };
    },
    methods: {
        async calcularEficiencia() {
            const resultats = await calculadors.calcularEficienciaInferencia(this.endpoint, this.input)
            this.$router.push({
                name: 'inference form',
                query: {dadesInicials: JSON.stringify(resultats)}
            })
        }
    }
}
</script>

<style scoped>

</style>