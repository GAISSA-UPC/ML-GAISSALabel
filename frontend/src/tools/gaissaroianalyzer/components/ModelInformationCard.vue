<template>
    <el-card shadow="always" :body-style="{ padding: '20px' }">
        <h2 class="section-title">{{ $t("Model Information") }}</h2>
        <el-descriptions v-if="modelData" :column="1" border>
            <el-descriptions-item :label="$t('Model architecture')">
                {{ modelData.model_architecture_name }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('ML Tactic')">
                {{ modelData.tactic_parameter_option_details?.tactic_name }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Tactic parameter')">
                {{ modelData.tactic_parameter_option_details?.name }}: {{
                    modelData.tactic_parameter_option_details?.value }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Analysis identifier')">
                {{ modelData.id }}
            </el-descriptions-item>
            <el-descriptions-item v-if="modelData.dateRegistration" :label="$t('Analysis registration date')">
                {{ formatDate(modelData.dateRegistration) }}
            </el-descriptions-item>
            <el-descriptions-item v-if="modelData.country" :label="$t('Country deploy')">
                {{ modelData.country }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Analysis type')">
                {{ isResearch ? $t('Research') : $t('Calculation') }}
            </el-descriptions-item>
        </el-descriptions>
        <p v-else>{{ $t("Loading model information...") }}</p>
    </el-card>
</template>

<script>
export default {
    name: "ModelInformationCard",
    props: {
        modelData: {
            type: Object,
            required: true
        },
        formatDate: {
            type: Function,
            required: true
        }
    },
    computed: {
        isResearch() {
            return this.modelData?.source !== null && this.modelData?.source !== undefined;
        }
    }
};
</script>

<style scoped>
.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin-bottom: 20px;
}
</style>
