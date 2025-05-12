<template>
    <el-card v-if="source" shadow="always" :body-style="{ padding: '20px' }" style="margin-top: 20px;">
        <h2 class="section-title">{{ $t("Source Information") }}</h2>
        <el-descriptions :column="1" border>
            <el-descriptions-item :label="$t('Title')">
                {{ source.title }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('URL')">
                <a :href="source.url" target="_blank" rel="noopener noreferrer">
                    {{ source.url }}
                </a>
            </el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>

<script>
export default {
    name: "SourceInformationCard",
    props: {
        source: {
            type: Object,
            required: true
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
