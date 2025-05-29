<template>
    <div class="emissions-card">
        <h3 v-if="showTitle">{{ $t('Environmental Impact') }}</h3>
        
        <div class="emissions-details-container">
            <!-- Left column: Carbon intensity and region table -->
            <div class="emissions-details-left">
                <el-descriptions :column="1" border>
                    <el-descriptions-item :label="$t('Carbon Intensity')">
                        {{ formatNumber(emissionsData.country_carbon_intensity_kgCO2Kwh * 1000) }} gCO₂/kWh
                    </el-descriptions-item>
                    <el-descriptions-item :label="$t('Region')">
                        {{ emissionsData.emissions_country_used || $t('Global Average') }}
                    </el-descriptions-item>
                </el-descriptions>

                <!-- Environmental Context -->
                <div class="environmental-context">
                    <el-alert type="info" :closable="false" show-icon>
                        <template #title>
                            {{ $t('Environmental Context') }}
                        </template>
                        <p>{{ getEnvironmentalContext() }}</p>
                    </el-alert>
                </div>
            </div>

            <!-- Right column: Environmental Impact Visual -->
            <div class="emissions-details-right">
                <div class="environmental-impact-visual">
                    <div class="impact-comparison">
                        <div class="impact-item baseline">
                            <font-awesome-icon :icon="['fas', 'cloud']" class="cloud-icon baseline" />
                            <div class="impact-label">{{ $t('Baseline inference emissions') }}</div>
                            <div class="impact-value">{{ formatEmissions(emissionsData.baseline_emissions_gCO2) }} CO₂</div>
                        </div>
                        
                        <font-awesome-icon :icon="['fas', 'arrow-right']" class="arrow-icon" />
                        
                        <div class="impact-item optimized">
                            <font-awesome-icon :icon="['fas', 'leaf']" class="leaf-icon optimized" />
                            <div class="impact-label">{{ $t('Optimized inference emissions') }}</div>
                            <div class="impact-value">{{ formatEmissions(emissionsData.new_emissions_gCO2) }} CO₂</div>
                        </div>
                    </div>
                    
                    <div class="savings-highlight">
                        <font-awesome-icon :icon="['fas', 'seedling']" class="savings-icon" />
                        <div class="savings-text">
                            <strong>{{ formatEmissions(emissionsData.emissions_saved_gCO2) }} {{ $t('CO₂ saved') }}</strong>
                            <div class="savings-context">{{ $t('for') }} {{ formatNumber(numInferences) }} {{ $t('inferences') }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "EmissionsReductionCard",
    props: {
        emissionsData: {
            type: Object,
            required: true
        },
        numInferences: {
            type: Number,
            required: true
        },
        formatNumber: {
            type: Function,
            required: true
        },
        showTitle: {
            type: Boolean,
            default: true
        },
        columnCount: {
            type: Number,
            default: 2
        }
    },
    methods: {
        formatEmissions(value) {
            const num = parseFloat(value);
            if (isNaN(num)) return '0 g';
            
            // Automatically choose kg or g based on the size of the number
            if (num >= 1000) {
                return this.formatNumber(num / 1000) + ' kg';
            }
            
            return this.formatNumber(num) + ' g';
        },
        getEnvironmentalContext() {
            const saved = parseFloat(this.emissionsData.emissions_saved_gCO2);
            const savedKg = saved / 1000;
            
            // Provide context for the emissions savings with appropriate references
            if (savedKg >= 100) {
                // 1 liter of gasoline = ~2.3 kg CO₂
                const liters = savedKg / 2.3;
                return this.$t('This emissions reduction is equivalent to avoiding the CO₂ from burning approximately') + ' ' + 
                       this.formatNumber(liters) + ' ' + this.$t('liters of gasoline.');
            } else if (savedKg >= 10) {
                // 1 tree absorbs ~22 kg CO₂ per year
                const trees = savedKg / 22;
                return this.$t('This emissions reduction is equivalent to the CO₂ absorbed by approximately') + ' ' + 
                       this.formatNumber(trees) + ' ' + this.$t('tree(s) in a year.');
            } else if (savedKg >= 1) {
                // Car driving: ~0.12 kg CO₂ per km (average car)
                const km = savedKg / 0.12;
                return this.$t('This emissions reduction is equivalent to avoiding') + ' ' + 
                       this.formatNumber(km) + ' ' + this.$t('km of car driving.');
            } else if (saved >= 50) {
                // Mobile phone charging: ~8g CO₂ per full charge
                const phoneCharges = saved / 45.8;
                return this.$t('This emissions reduction is equivalent to approximately') + ' ' + 
                       this.formatNumber(phoneCharges) + ' ' + this.$t('mobile phone usage days.');
            } else {
                return this.$t('Every gram of CO₂ saved contributes to environmental sustainability.');
            }
        }
    }
};
</script>

<style scoped>
.emissions-card {
    flex: 1;
    min-width: 100px;
}

.emissions-card h3 {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 15px;
    color: #2e7d32;
    display: flex;
    align-items: center;
    gap: 8px;
}



/* Two-column layout for emissions details */
.emissions-details-container {
    display: flex;
    gap: 20px;
    margin-top: 20px;
}

.emissions-details-left {
    flex: 1;
    min-width: 100px;
}

.emissions-details-right {
    flex: 1.5;
    min-width: 100px;
}

.environmental-impact-visual {
    margin: 20px 0;
    padding: 20px;
    background: linear-gradient(135deg, #e8f5e8 0%, #f3e5f5 100%);
    border-radius: 12px;
    border: 2px solid #e0e0e0;
}

.impact-comparison {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
    margin-bottom: 20px;
}

.impact-item {
    text-align: center;
    flex: 1;
    max-width: 160px;
}

.cloud-icon.baseline {
    font-size: 2.5rem;
    color: #f57c00;
    margin-bottom: 8px;
}

.leaf-icon.optimized {
    font-size: 2.5rem;
    color: #2e7d32;
    margin-bottom: 8px;
}

.arrow-icon {
    font-size: 1.5rem;
    color: #666;
}

.impact-label {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 4px;
}

.impact-value {
    font-weight: bold;
    font-size: 0.95rem;
}

.savings-highlight {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 15px;
    background: rgba(46, 125, 50, 0.1);
    border-radius: 8px;
    border: 1px solid #2e7d32;
}

.savings-icon {
    font-size: 1.8rem;
    color: #2e7d32;
}

.savings-text {
    text-align: center;
}

.savings-text strong {
    color: #2e7d32;
    font-size: 1.1rem;
}

.savings-context {
    font-size: 0.9rem;
    color: #666;
    margin-top: 2px;
}

.environmental-context {
    margin-top: 20px;
}

.environmental-context .el-alert {
    border-left: 4px solid #2e7d32;
}

.environmental-context p {
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.4;
}

/* Responsive design */
@media (max-width: 768px) {
    .emissions-details-container {
        flex-direction: column;
        gap: 15px;
    }
    
    .emissions-details-left,
    .emissions-details-right {
        flex: 1;
        min-width: 100%;
    }
    
    .impact-comparison {
        flex-direction: column;
        gap: 15px;
    }
    
    .arrow-icon {
        transform: rotate(90deg);
    }
    
    .environmental-impact-visual {
        padding: 15px;
        margin: 0;
    }
    
    .savings-highlight {
        flex-direction: column;
        text-align: center;
        gap: 8px;
    }
}
</style>
