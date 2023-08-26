<template>
    <h1>{{ $t("Energy label for training") }}</h1><br>
    <h2>{{ $t("Register a new training") }}</h2><br>

    <el-form label-position="top">
        <el-form-item :label="$t('Model')">
            <el-select v-model="selectedModel">
                <el-option
                    v-for="(model, i) in models" :key="i"
                    :value="model.id"
                    :label="model.nom"
                />
            </el-select>
        </el-form-item><br>

        <h3>{{ $t("Metrics") }}</h3><br>
        <el-form-item
            v-for="(metrica, i) in metriques" :key="i"
            :label="metrica.nom"
        >
            <el-input-number
                step="0.01"
                v-model="metrica.valor"
                min="0"
            />
            <p style="margin-left: 10px">{{ metrica.unitat }}</p>
        </el-form-item>
        <br>
        <el-button
            @click="generarEtiqueta"
            class="action-button-light"
        >
            {{ $t('Generate label') }}
        </el-button>
    </el-form><br>
    <EnergyLabel
        :pdfBase64="labelBase64"
        v-show="labelBase64"
    />
</template>

<script>
    import models from '@/services/models'
    import metriques from '@/services/metriques'
    import trainings from '@/services/trainings'
    import EnergyLabel from "@/components/EnergyLabel.vue";
    export default {
        name: "TrainingForm",
        components: {EnergyLabel},
        data() {
            return {
                models: null,
                selectedModel: null,
                metriques: null,
                labelBase64: null,
            };
        },
        methods: {
            async refrescaModels() {
                const response = await models.list()
                this.models = response.data
            },
            async refrescaMetriques() {
                const response = await metriques.listOrderedFilteredByPhase('T')
                this.metriques = response.data
            },
            async generarEtiqueta() {
                const responseCreate = await trainings.create(this.selectedModel, this.metriques)
                if (responseCreate.status === 201) {
                    const entrenament_id = responseCreate.data['id']
                    const responseLabel = await trainings.retrieve(this.selectedModel, entrenament_id)
                    this.labelBase64 = responseLabel.data['energy_label']
                }
            },
        },
        async mounted() {
            await this.refrescaModels();
            await this.refrescaMetriques();
        },
    };
</script>

<style>
</style>