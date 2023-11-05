<template>
    <h1>{{ $t("Energy label for inference") }}</h1><br>

    <el-form label-position="top">
        <el-form-item
            :label="$t('Endpoint where the model is deployed')"
        >
            <el-input v-model="endpoint"/>
        </el-form-item>
        <br>
        <el-form-item
            :label="$t('Input for the inference')"
        >
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