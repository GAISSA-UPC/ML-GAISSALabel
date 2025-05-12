<template>
    <el-card v-if="sources && sources.length > 0" shadow="always" :body-style="{ padding: '20px' }"
        style="margin-top: 20px;">
        <h2 class="section-title">{{ $t("Tactic Sources") }}</h2>
        <p class="results-description">
            {{ $t("This analysis provides an estimation of the expected effects of applying the tactic. The estimated reductions and efficiency improvements are calculated based on the data and results obtained from the following research studies:") }}
        </p>
        <el-descriptions v-for="(source, index) in sources" :key="index" :column="1" border
            :style="{ marginBottom: index < sources.length - 1 ? '15px' : '0' }">
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
    name: "TacticSourcesCard",
    props: {
        sources: {
            type: Array,
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

.results-description {
    margin-bottom: 10px;
}
</style>
