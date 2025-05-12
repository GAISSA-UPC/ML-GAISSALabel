<template>
    <div class="metric-card">
        <!-- Percentage Change -->
        <div class="change-indicator">
            <div class="arrow-container">
                <font-awesome-icon v-if="calculateCostReductionPercent > 0" :icon="['fas', 'down-long']"
                    class="change-arrow positive" />
                <font-awesome-icon v-else-if="calculateCostReductionPercent == 0" :icon="['fas', 'equals']"
                    class="change-arrow positive" />
                <font-awesome-icon v-else :icon="['fas', 'up-long']" class="change-arrow negative" />
            </div>
            <div :class="['change-percentage', calculateCostReductionPercent >= 0 ? 'positive' : 'negative']">
                {{ formatNumber(Math.abs(calculateCostReductionPercent)) }}%
            </div>
        </div>

        <div class="metric-data">
            <!-- Metric Title and Description -->
            <div class="metric-info">
                <h3 class="metric-title">{{ $t('Incurred Cost') }}</h3>
                <p class="metric-description">
                    {{ $t('Total cost associated with running the model for') }}
                    {{ formatNumber(costMetric.num_inferences) }}
                    {{ $t('inferences.') }}
                </p>
            </div>
            <!-- Metric Comparison Area -->
            <div class="metric-comparison">
                <div class="values-comparison">
                    <!-- Optimized Value -->
                    <div class="value-container optimized">
                        <div class="value-label">{{ $t("Optimized") }}</div>
                        <div :class="['value', calculateCostReductionPercent >= 0 ? 'positive' : 'negative']">
                            {{ formatNumber(costMetric.total_new_cost) }} <span class="unit">€</span>
                        </div>
                    </div>
                    <!-- Non-Optimized Value -->
                    <div class="value-container baseline">
                        <div class="value-label">{{ $t("Non-optimized") }}</div>
                        <div class="value">
                            {{ formatNumber(costMetric.total_baseline_cost) }} <span class="unit">€</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CostMetricCard",
    props: {
        costMetric: {
            type: Object,
            required: true
        },
        formatNumber: {
            type: Function,
            required: true
        }
    },
    computed: {
        calculateCostReductionPercent() {
            // Handle cases where baseline cost is zero or non-numeric
            const baselineCost = parseFloat(this.costMetric.total_baseline_cost);
            const newCost = parseFloat(this.costMetric.total_new_cost);

            if (isNaN(baselineCost) || isNaN(newCost)) return 0;
            if (baselineCost === 0) {
                return -Infinity;
            }

            const reduction = baselineCost - newCost;
            const percentage = (reduction / baselineCost) * 100;

            return parseFloat(percentage.toFixed(2));
        }
    }
};
</script>

<style scoped>
.metric-card {
    display: flex;
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 8px;
    background-color: #f8f8f8;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    flex-direction: row;
    min-width: 0;
}

.metric-data {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.metric-title {
    font-size: 1.4rem !important;
    font-weight: bold;
    margin-bottom: 5px;
    color: #333;
}

.metric-description {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 20px;
}

.metric-comparison {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 15px;
    border-top: 1px dashed #ddd;
}

.change-indicator {
    display: flex;
    flex-direction: row;
    gap: 5px;
    align-items: center;
    flex: 0;
    margin-right: 20px;
}

.change-percentage {
    font-size: 2.5rem;
    font-weight: bold;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.change-percentage.positive {
    color: green;
}

.change-percentage.negative {
    color: orange;
}

.arrow-container {
    margin-top: 5px;
}

.change-arrow {
    font-size: 2rem;
    font-weight: bold;
}

.change-arrow.positive {
    color: green;
}

.change-arrow.negative {
    color: orange;
}

.values-comparison {
    display: flex;
    justify-content: flex-start;
    gap: 40px;
    flex: 2;
    margin-left: 10px;
}

.value-container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    text-align: right;
}

.value-label {
    font-size: 0.9rem;
    color: #777;
    margin-bottom: 10px;
}

.value {
    font-size: 1.6rem;
    font-weight: bold;
    letter-spacing: -0.5px;
    line-height: 0.5;
}

.value.positive {
    color: green;
}

.value.negative {
    color: orange;
}

.unit {
    font-size: 0.9rem;
    opacity: 0.7;
    margin-left: 3px;
}

@media (max-width: 992px) {
    .metric-card {
        flex-direction: column;
        align-items: center;
    }

    .values-comparison {
        width: 100%;
        justify-content: space-between;
        gap: 10px;
        margin-left: 0;
    }

    .value-container {
        align-items: center;
    }
}
</style>
