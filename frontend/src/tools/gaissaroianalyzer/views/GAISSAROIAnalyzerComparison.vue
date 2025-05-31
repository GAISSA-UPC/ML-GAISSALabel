<template>
    <div class="gaissa-roi-analyzer-comparison">
        <h1>{{ $t("GAISSA ROI Analyzer") }}</h1>
        <h2>{{ $t("Analysis Comparison") }}</h2>
        
        <p class="description">
            {{ $t("This page allows you to compare two different ROI analyses side by side. Select two analyses from the available options below to visualize their differences and similarities.") }}
        </p>

        <!-- Analysis Selection Section -->
        <el-row :gutter="20" class="selection-row">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h3 class="section-title">{{ $t("First Analysis") }}</h3>
                    
                    <!-- Analysis Type Selector -->
                    <div class="analysis-type-selector">
                        <el-form-item :label="$t('Analysis Type')">
                            <el-select v-model="firstAnalysisType" @change="onFirstAnalysisTypeChange" placeholder="Select type">
                                <el-option value="calculation" :label="$t('Calculation Analysis')" />
                                <el-option value="research" :label="$t('Research Analysis')" />
                            </el-select>
                        </el-form-item>
                    </div>
                    
                    <AnalysisSelector 
                        v-if="firstAnalysisType"
                        ref="firstAnalysisSelector"
                        :analysis-type="firstAnalysisType"
                        :repository-title="$t('Select First Analysis')"
                        :repository-description="getAnalysisDescription(firstAnalysisType)"
                        :analysis-selection-description="getAnalysisSelectionDescription(firstAnalysisType)"
                        :comparison-mode="true"
                        @analysisSelected="onFirstAnalysisSelected"
                    />
                </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <el-card shadow="always" :body-style="{ padding: '20px' }">
                    <h3 class="section-title">{{ $t("Second Analysis") }}</h3>
                    
                    <!-- Analysis Type Selector -->
                    <div class="analysis-type-selector">
                        <el-form-item :label="$t('Analysis Type')">
                            <el-select v-model="secondAnalysisType" @change="onSecondAnalysisTypeChange" placeholder="Select type">
                                <el-option value="calculation" :label="$t('Calculation Analysis')" />
                                <el-option value="research" :label="$t('Research Analysis')" />
                            </el-select>
                        </el-form-item>
                    </div>
                    
                    <AnalysisSelector 
                        v-if="secondAnalysisType"
                        ref="secondAnalysisSelector"
                        :analysis-type="secondAnalysisType"
                        :repository-title="$t('Select Second Analysis')"
                        :repository-description="getAnalysisDescription(secondAnalysisType)"
                        :analysis-selection-description="getAnalysisSelectionDescription(secondAnalysisType)"
                        :comparison-mode="true"
                        @analysisSelected="onSecondAnalysisSelected"
                    />
                </el-card>
            </el-col>
        </el-row>

        <!-- Comparison Results Section -->
        <div v-if="firstAnalysisId && secondAnalysisId" class="comparison-results">
            <el-divider>
                <span class="divider-text">{{ $t("Comparison Results") }}</span>
            </el-divider>
            
            <el-row :gutter="20" class="analysis-comparison-row">
                <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                    <el-card shadow="always" :body-style="{ padding: '20px' }">
                        <template #header>
                            <div class="card-header">
                                <span class="analysis-title">{{ $t("Analysis A") }}</span>
                            </div>
                        </template>
                        <ROIAnalysisComponent 
                            :analysisId="firstAnalysisId"
                            :showExportButton="false"
                            :forceMobile="true"
                            containerId="first-analysis-container" 
                        />
                    </el-card>
                </el-col>
                
                <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                    <el-card shadow="always" :body-style="{ padding: '20px' }">
                        <template #header>
                            <div class="card-header">
                                <span class="analysis-title">{{ $t("Analysis B") }}</span>
                            </div>
                        </template>
                        <ROIAnalysisComponent 
                            :analysisId="secondAnalysisId"
                            :showExportButton="false"
                            :forceMobile="true"
                            containerId="second-analysis-container" 
                        />
                    </el-card>
                </el-col>
            </el-row>
        </div>
        
        <!-- Instructions when no analyses are selected -->
        <div v-else class="instructions">
            <el-alert
                type="info"
                :title="$t('Instructions')"
                :description="$t('Please select two analyses from the sections above to start the comparison. Both analyses need to be selected before the comparison results will be displayed.')"
                show-icon
                :closable="false">
            </el-alert>
        </div>
    </div>
</template>

<script>
import AnalysisSelector from '@/tools/gaissaroianalyzer/components/AnalysisSelector.vue';
import ROIAnalysisComponent from '@/tools/gaissaroianalyzer/components/ROIAnalysisComponent.vue';

export default {
    name: "GAISSAROIAnalyzerComparison",
    components: {
        AnalysisSelector,
        ROIAnalysisComponent
    },
    data() {
        return {
            firstAnalysisId: null,
            secondAnalysisId: null,
            firstAnalysisType: 'calculation',
            secondAnalysisType: 'calculation'
        };
    },
    methods: {
        onFirstAnalysisSelected(analysisId) {
            this.firstAnalysisId = analysisId;
        },
        onSecondAnalysisSelected(analysisId) {
            this.secondAnalysisId = analysisId;
        },
        onFirstAnalysisTypeChange() {
            this.firstAnalysisId = null;
        },
        onSecondAnalysisTypeChange() {
            this.secondAnalysisId = null;
        },
        getAnalysisDescription(analysisType) {
            if (analysisType === 'calculation') {
                return this.$t('Choose a calculation analysis for comparison');
            } else if (analysisType === 'research') {
                return this.$t('Choose a research analysis for comparison');
            }
            return '';
        },
        getAnalysisSelectionDescription(analysisType) {
            if (analysisType === 'calculation') {
                return this.$t('Select an analysis by its creation date:');
            } else if (analysisType === 'research') {
                return this.$t('Select an analysis by its source:');
            }
            return '';
        }
    }
};
</script>

<style scoped>
.gaissa-roi-analyzer-comparison {
    padding: 20px;
}

h1 {
    color: var(--gaissa_green);
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.description {
    margin-bottom: 30px;
    margin-top: 20px;
    font-size: 16px;
    line-height: 1.6;
}

.section-title {
    color: var(--gaissa_green);
    font-weight: bold;
    margin-bottom: 15px;
    text-align: center;
}

.analysis-type-selector {
    margin-bottom: 20px;
}

.analysis-type-selector .el-select {
    width: 100%;
}

.selection-row {
    margin-bottom: 30px;
}

.comparison-results {
    margin-top: 50px;
}

.divider-text {
    font-size: 18px;
    font-weight: bold;
    color: var(--gaissa_green);
}

.analysis-comparison-row {
    margin-top: 30px;
}

.card-header {
    display: flex;
    justify-content: center;
    align-items: center;
}

.analysis-title {
    font-size: 18px;
    font-weight: bold;
    color: var(--gaissa_green);
}

.instructions {
    margin-top: 40px;
    display: flex;
    justify-content: center;
}

.instructions .el-alert {
    max-width: 600px;
}

@media (max-width: 768px) {
    .selection-row {
        margin-bottom: 20px;
    }
    
    .analysis-comparison-row .el-col {
        margin-bottom: 30px;
    }
}
</style>
