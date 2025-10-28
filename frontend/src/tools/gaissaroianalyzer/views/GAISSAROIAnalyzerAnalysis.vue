<template>
    <div class="gaissa-roi-analyzer">
        <h1>{{ $t("GAISSA ROI Analyzer") }}</h1>

        <!-- ROI Analysis Main Component -->
        <ROIAnalysisComponent 
            :analysisId="currentAnalysisId"
            :showExportButton="true"
            :showSwapper="true"
            containerId="roi-analysis-container"
            @analysisLoaded="handleAnalysisLoaded"
            @analysisChanged="handleAnalysisChange" />
    </div>
</template>

<script>
import ROIAnalysisComponent from '../components/ROIAnalysisComponent.vue';

export default {
    name: "GAISSAROIAnalyzerAnalysis",
    components: {
        ROIAnalysisComponent
    },
    data() {
        return {
            analysisData: null,
            currentAnalysisId: null
        };
    },
    watch: {
        '$route.params.id_experiment': {
            immediate: true,
            handler(newId) {
                this.currentAnalysisId = newId;
            }
        }
    },
    methods: {
        handleAnalysisLoaded(data) {
            this.analysisData = data;
        },
        handleAnalysisChange(newAnalysisId) {
            // Navigate to the new analysis
            this.$router.push({
                name: "GAISSA ROI Analyzer Analysis",
                params: {
                    id_experiment: newAnalysisId
                }
            });
        }
    }
};
</script>

<style scoped>
h1 { 
    margin-bottom: 10px; 
}

.gaissa-roi-analyzer {
    padding: 20px;
}

.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin-bottom: 20px;
}

.results-description {
    margin-bottom: 10px;
}

.mobile-card {
    margin-bottom: 20px;
}

.el-button {
    background-color: var(--gaissa_green);
    color: white;
    border-color: var(--gaissa_green);
}

.inferences-control-container {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 12px;
    background-color: #f9f9f9;
    border-radius: 8px;
    border: 1px solid #eee;
}

.inferences-control-label {
    font-weight: bold;
    margin-right: 12px;
    min-width: 150px;
    margin-bottom: 0;
}

.inferences-slider-container {
    flex-grow: 1;
    margin-right: 20px;
}

.inferences-input-container {
    width: 150px;
}

.roi-cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.emissions-section {
    border-top: 1px solid #eee;
    padding-top: 20px;
}

.emissions-card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.view-toggle {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    justify-content: flex-end;
}

.visual-metrics-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
    margin-top: 20px;
}

.export-button-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
}

.action-button {
    display: flex;
    align-items: center;
    gap: 8px;
}

@media (max-width: 1320px) {
    .visual-metrics-container {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 992px) {
    .inferences-control-container {
        flex-direction: column;
        align-items: stretch;
    }

    .inferences-control-label {
        margin-bottom: 10px;
    }

    .inferences-slider-container {
        margin-right: 0;
        margin-bottom: 10px;
    }

    .inferences-input-container {
        width: 100%;
    }
}
</style>
