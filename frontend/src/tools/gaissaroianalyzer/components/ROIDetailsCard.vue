<template>
    <div class="roi-card">
        <h3 v-if="showTitle">{{ costMetric.metric_name }}</h3>
        <el-descriptions :column="columnCount" border>
            <el-descriptions-item :label="$t('Incurred Cost (€)')">
                {{ formatNumber(costMetric.total_new_cost) }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Non-optimized Incurred Cost (€)')">
                {{ formatNumber(costMetric.total_baseline_cost) }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Inference Cost (€)')">
                {{ formatNumber(costMetric.new_cost_per_inference) }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Non-optimized Inference Cost (€)')">
                {{ formatNumber(costMetric.baseline_cost_per_inference) }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Implementation Cost (€)')">
                {{ formatNumber(costMetric.implementation_cost) }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Energy Cost (€/kWh)')">
                {{ formatNumber(costMetric.energy_cost_rate) }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Cost Savings (€)')">
                {{ formatNumber(costMetric.total_savings) }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('Break-Even Point (inferences)')">
                {{ costMetric.break_even_inferences }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t(`ROI (for ${costMetric.num_inferences.toLocaleString('en-US')} inferences)`)">
                {{ formatNumber(costMetric.roi_percentage) }}%
            </el-descriptions-item>
            <el-descriptions-item :label="$t('ROI (for infinite inferences)')">
                {{ formatNumber(costMetric.infinite_roi_percentage) }}%
            </el-descriptions-item>
        </el-descriptions>

        <!-- Recommendation based on Break-Even Point -->
        <div class="recommendation-container" v-if="tacticName">
            <font-awesome-icon v-if="costMetric.break_even_inferences !== 'Infinity'" :icon="['fas', 'lightbulb']"
                class="recommendation-icon positive" />
            <font-awesome-icon v-else :icon="['fas', 'lightbulb']" class="recommendation-icon negative" />
            <div v-if="costMetric.break_even_inferences !== 'Infinity'" class="recommendation positive">
                <strong>We recommend you to apply the tactic {{ tacticName }}</strong>
                if you expect to perform an amount of inferences higher than {{ costMetric.break_even_inferences }}.
            </div>
            <div v-else class="recommendation negative">
                We encourage you to consider a different ML tactic as this one does not provide a positive return on
                investment.
            </div>
        </div>

        <slot name="costMetricCard"></slot>
    </div>
</template>

<script>
export default {
    name: "ROIDetailsCard",
    props: {
        costMetric: {
            type: Object,
            required: true
        },
        formatNumber: {
            type: Function,
            required: true
        },
        tacticName: {
            type: String,
            default: ''
        },
        showTitle: {
            type: Boolean,
            default: false
        },
        columnCount: {
            type: Number,
            default: 2
        }
    }
};
</script>

<style scoped>
.roi-card {
    flex: 1;
    min-width: 20px;
}

.roi-card h3 {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 15px;
}

.recommendation-container {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
    margin-bottom: 20px;
    padding: 15px;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.recommendation-icon.positive {
    font-size: 2rem;
    color: var(--gaissa_green);
}

.recommendation-icon.negative {
    font-size: 2rem;
    color: orange;
}

.recommendation {
    font-size: 1.1rem;
    line-height: 1.5;
    padding: 10px;
    border-radius: 6px;
}

.recommendation.positive {
    background-color: rgba(0, 128, 0, 0.1);
    border-left: 4px solid green;
}

.recommendation.negative {
    background-color: rgba(255, 165, 0, 0.1);
    border-left: 4px solid orange;
}

@media (max-width: 992px) {
    .roi-card {
        min-width: 100%;
        width: 100%;
    }
}
</style>
