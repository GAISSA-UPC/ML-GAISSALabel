<template>
    <div class="roi-analyzer-home">
        <!-- Hero Section -->
        <section class="hero-section">
            <h1 class="hero-title">{{ $t('Welcome to GAISSA ROI Analyzer') }}</h1>
            <p class="hero-subtitle">
                {{ $t('Evaluate the return on investment of ML optimization tactics and make data-driven decisions for sustainable AI development.') }}
            </p>
        </section>

        <!-- Statistics Overview -->
        <section class="stats-overview">
            <h2 class="section-title">{{ $t('What are we offering?') }}</h2>
            <el-row :gutter="20" justify="center" class="stat-row">
                <el-col :xs="12" :sm="6" :md="6" :lg="6">
                    <el-card class="stat-card pipeline-card" shadow="hover">
                        <div class="stat-icon">
                            <font-awesome-icon :icon="['fas', 'layer-group']" />
                        </div>
                        <div class="stat-content">
                            <div class="stat-number">{{ statistics.pipelineStages || 0 }}</div>
                            <div class="stat-label">{{ $t('Pipeline Stages') }}</div>
                        </div>
                    </el-card>
                </el-col>
                <el-col :xs="12" :sm="6" :md="6" :lg="6">
                    <el-card class="stat-card tactics-card" shadow="hover">
                        <div class="stat-icon">
                            <font-awesome-icon :icon="['fas', 'cogs']" />
                        </div>
                        <div class="stat-content">
                            <div class="stat-number">{{ statistics.tactics || 0 }}</div>
                            <div class="stat-label">{{ $t('ML Tactics') }}</div>
                        </div>
                    </el-card>
                </el-col>
                <el-col :xs="12" :sm="6" :md="6" :lg="6">
                    <el-card class="stat-card research-card" shadow="hover">
                        <div class="stat-icon">
                            <font-awesome-icon :icon="['fas', 'flask']" />
                        </div>
                        <div class="stat-content">
                            <div class="stat-number">{{ statistics.researchAnalyses || 0 }}</div>
                            <div class="stat-label">{{ $t('Research Analyses') }}</div>
                        </div>
                    </el-card>
                </el-col>
                <el-col :xs="12" :sm="6" :md="6" :lg="6">
                    <el-card class="stat-card calculation-card" shadow="hover">
                        <div class="stat-icon">
                            <font-awesome-icon :icon="['fas', 'calculator']" />
                        </div>
                        <div class="stat-content">
                            <div class="stat-number">{{ statistics.calculationAnalyses || 0 }}</div>
                            <div class="stat-label">{{ $t('Saved Analyses') }}</div>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </section>

        <!-- Pipeline Stages Breakdown -->
        <section class="pipeline-breakdown" v-if="pipelineStagesData.length > 0">
            <h2 class="section-title">{{ $t('Tactics by Pipeline Stage') }}</h2>
            <p class="section-description">
                {{ $t('Our database contains ML optimization tactics organized by their role in the ML workflow.') }}
            </p>
            <el-row :gutter="20" justify="center" class="stat-row">
                <el-col 
                    v-for="stage in pipelineStagesData" 
                    :key="stage.id"
                    :xs="24" 
                    :sm="12" 
                    :md="8">
                    <el-card class="pipeline-stage-card" shadow="hover">
                        <div class="stage-header">
                            <div class="stage-icon" :class="`stage-${stage.id}`">
                                <font-awesome-icon :icon="getStageIcon(stage.name)" />
                            </div>
                            <h3 class="stage-name">{{ stage.name }}</h3>
                        </div>
                        <div class="stage-stats">
                            <div class="stage-stat-item">
                                <div class="stat-badge tactics-badge">
                                    <font-awesome-icon :icon="['fas', 'cogs']" class="stat-badge-icon" />
                                    <span class="stat-badge-value">{{ stage.tactics_count || 0 }}</span>
                                </div>
                                <span class="stat-badge-label">{{ $t('Tactics') }}</span>
                            </div>
                            <div class="stage-stat-item">
                                <div class="stat-badge research-badge">
                                    <font-awesome-icon :icon="['fas', 'flask']" class="stat-badge-icon" />
                                    <span class="stat-badge-value">{{ stage.research_analyses_count || 0 }}</span>
                                </div>
                                <span class="stat-badge-label">{{ $t('Research') }}</span>
                            </div>
                            <div class="stage-stat-item">
                                <div class="stat-badge calculation-badge">
                                    <font-awesome-icon :icon="['fas', 'calculator']" class="stat-badge-icon" />
                                    <span class="stat-badge-value">{{ stage.calculation_analyses_count || 0 }}</span>
                                </div>
                                <span class="stat-badge-label">{{ $t('Saved') }}</span>
                            </div>
                        </div>
                        <div class="stage-total">
                            <span class="total-label">{{ $t('Total Analyses') }}:</span>
                            <span class="total-value">{{ (stage.research_analyses_count || 0) + (stage.calculation_analyses_count || 0) }}</span>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </section>

        <!-- Getting Started Guide -->
        <section class="getting-started">
            <h2 class="section-title">{{ $t('Getting Started') }}</h2>
            <p class="section-description">
                {{ $t('Follow these steps to make the most of the GAISSA ROI Analyzer:') }}
            </p>
            <el-row :gutter="20" class="stat-row">
                <el-col :xs="24" :sm="12" :md="6" :lg="6">
                    <el-card class="guide-card" shadow="hover">
                        <div class="guide-number">1</div>
                        <div class="guide-icon">
                            <font-awesome-icon :icon="['fas', 'book-open']" />
                        </div>
                        <h3 class="guide-title">{{ $t('Explore Research') }}</h3>
                        <p class="guide-description">
                            {{ $t('Browse research-based ROI analyses from published papers to understand proven optimization tactics.') }}
                        </p>
                        <el-button 
                            type="primary" 
                            class="guide-button"
                            @click="$router.push({name: 'GAISSA ROI Analyzer Research Repository'})">
                            {{ $t('View Research') }}
                        </el-button>
                    </el-card>
                </el-col>
                <el-col :xs="24" :sm="12" :md="6" :lg="6">
                    <el-card class="guide-card" shadow="hover">
                        <div class="guide-number">2</div>
                        <div class="guide-icon">
                            <font-awesome-icon :icon="['fas', 'calculator']" />
                        </div>
                        <h3 class="guide-title">{{ $t('Calculate ROI') }}</h3>
                        <p class="guide-description">
                            {{ $t('Create your own ROI analysis by selecting a tactic, model architecture, and providing baseline metrics.') }}
                        </p>
                        <el-button 
                            type="primary" 
                            class="guide-button"
                            @click="$router.push({name: 'GAISSA ROI Analyzer New Form'})">
                            {{ $t('Calculate Now') }}
                        </el-button>
                    </el-card>
                </el-col>
                <el-col :xs="24" :sm="12" :md="6" :lg="6">
                    <el-card class="guide-card" shadow="hover">
                        <div class="guide-number">3</div>
                        <div class="guide-icon">
                            <font-awesome-icon :icon="['fas', 'folder-open']" />
                        </div>
                        <h3 class="guide-title">{{ $t('Review Analyses') }}</h3>
                        <p class="guide-description">
                            {{ $t('Access your previously calculated ROI analyses to review results and make informed decisions.') }}
                        </p>
                        <el-button 
                            type="primary" 
                            class="guide-button"
                            @click="$router.push({name: 'GAISSA ROI Analyzer Calculation Repository'})">
                            {{ $t('My Analyses') }}
                        </el-button>
                    </el-card>
                </el-col>
                <el-col :xs="24" :sm="12" :md="6" :lg="6">
                    <el-card class="guide-card" shadow="hover">
                        <div class="guide-number">4</div>
                        <div class="guide-icon">
                            <font-awesome-icon :icon="['fas', 'balance-scale']" />
                        </div>
                        <h3 class="guide-title">{{ $t('Compare Options') }}</h3>
                        <p class="guide-description">
                            {{ $t('Compare multiple analyses side-by-side to determine the best optimization strategy for your needs.') }}
                        </p>
                        <el-button 
                            type="primary" 
                            class="guide-button"
                            @click="$router.push({name: 'GAISSA ROI Analyzer Comparison'})">
                            {{ $t('Compare') }}
                        </el-button>
                    </el-card>
                </el-col>
            </el-row>
        </section>

        <!-- Video Section -->
        <section class="video-section">
            <h2 class="section-title">{{ $t('Watch Our Introduction Video') }}</h2>
            <div class="video-container">
                <iframe 
                    src="https://www.youtube.com/embed/8JOG4zWyzws" 
                    title="GAISSA ROI Analyzer: Estimating the Return on Investment of Green Tactics in ML-Enabled Systems" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    referrerpolicy="strict-origin-when-cross-origin" 
                    allowfullscreen>
                </iframe>
            </div>
        </section>

        <!-- Call to Action -->
        <section class="cta-section">
            <el-card class="cta-card" shadow="always">
                <h2>{{ $t('Ready to Optimize Your ML Models?') }}</h2>
                <p>{{ $t('Start by exploring our research database or calculate your own ROI analysis.') }}</p>
                <div class="cta-buttons">
                    <el-button 
                        type="primary" 
                        size="large"
                        @click="$router.push({name: 'GAISSA ROI Analyzer Research Repository'})">
                        <font-awesome-icon :icon="['fas', 'book-open']" style="margin-right: 8px" />
                        {{ $t('Browse Research') }}
                    </el-button>
                    <el-button 
                        size="large"
                        @click="$router.push({name: 'GAISSA ROI Analyzer New Form'})">
                        <font-awesome-icon :icon="['fas', 'calculator']" style="margin-right: 8px" />
                        {{ $t('Calculate ROI') }}
                    </el-button>
                </div>
            </el-card>
        </section>
    </div>
</template>

<script>
import statistics from "@/tools/gaissaroianalyzer/services/statistics";

export default {
    name: "GAISSAROIAnalyzerHome",
    data() {
        return {
            statistics: {
                pipelineStages: 0,
                tactics: 0,
                researchAnalyses: 0,
                calculationAnalyses: 0
            },
            pipelineStagesData: []
        };
    },
    methods: {
        async fetchStatistics() {
            try {
                const data = await statistics.getStatistics();
                
                if (data) {
                    // Update overall statistics
                    this.statistics.pipelineStages = data.total_pipeline_stages || 0;
                    this.statistics.tactics = data.total_tactics || 0;
                    this.statistics.researchAnalyses = data.total_research_analyses || 0;
                    this.statistics.calculationAnalyses = data.total_calculation_analyses || 0;
                    
                    // Update pipeline stages data with breakdown
                    this.pipelineStagesData = data.stage_breakdown || [];
                }
            } catch (error) {
                console.error('Error fetching ROI Analyzer statistics:', error);
            }
        },
        getStageIcon(stageName) {
            const iconMap = {
                'Data-centric': ['fas', 'database'],
                'Model optimization': ['fas', 'sliders'],
                'Management': ['fas', 'tasks']
            };
            return iconMap[stageName] || ['fas', 'layer-group'];
        }
    },
    async mounted() {
        await this.fetchStatistics();
    }
};
</script>

<style scoped>
.roi-analyzer-home {
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, #548334 0%, #6fa843 100%);
    border-radius: 20px;
    margin-bottom: 50px;
    color: white;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 20px;
    color: white;
}

.hero-subtitle {
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
    opacity: 0.95;
}

/* Video Section */
.video-section {
    margin-bottom: 60px;
}

.video-container {
    position: relative;
    width: 70%;
    max-width: 996px;
    margin: 0 auto;
    padding-bottom: 39.375%;  /* For width 100%: 56.25%; 16:9 aspect ratio */
    height: 0;
    overflow: hidden;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.video-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 15px;
}

/* Section Titles */
.section-title {
    font-size: 2rem;
    font-weight: bold;
    color: var(--gaissa_green);
    text-align: center;
    margin-bottom: 15px;
}

.section-description {
    text-align: center;
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 40px;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

/* Statistics Overview */
.stats-overview {
    row-gap: 60px;
}

.stat-row {
    row-gap: 20px; /* Vertical spacing between rows */
    margin-bottom: 40px;
}

.stat-card {
    text-align: center;
    border-radius: 15px;
    transition: all 0.3s ease;
    height: 100%;
}

.stat-card:hover {
    transform: translateY(-5px);
}

.stat-icon {
    font-size: 3rem;
    margin-bottom: 15px;
}

.pipeline-card .stat-icon {
    color: #FF9800;
}

.tactics-card .stat-icon {
    color: #2196F3;
}

.research-card .stat-icon {
    color: #9C27B0;
}

.calculation-card .stat-icon {
    color: #4CAF50;
}

.stat-number {
    font-size: 3rem;
    font-weight: bold;
    color: var(--gaissa_green);
    display: block;
    line-height: 1;
    margin-bottom: 10px;
}

.stat-label {
    font-size: 1.1rem;
    color: #666;
    font-weight: 500;
}

/* Pipeline Stages Breakdown */
.pipeline-breakdown {
    margin-bottom: 60px;
}

.pipeline-stage-card {
    padding: 15px;
    border-radius: 15px;
    height: 100%;
    transition: all 0.3s ease;
}

.pipeline-stage-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.stage-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}

.stage-icon {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: white;
}

.stage-icon.stage-1 {
    background: linear-gradient(135deg, #4CAF50, #66BB6A);
}

.stage-icon.stage-2 {
    background: linear-gradient(135deg, #2196F3, #42A5F5);
}

.stage-icon.stage-3 {
    background: linear-gradient(135deg, #FF9800, #FFA726);
}

.stage-icon.stage-4 {
    background: linear-gradient(135deg, #9C27B0, #AB47BC);
}

.stage-icon.stage-5 {
    background: linear-gradient(135deg, #FF5722, #FF7043);
}

.stage-icon.stage-6 {
    background: linear-gradient(135deg, #607D8B, #78909C);
}

.stage-name {
    font-size: 1.3rem;
    font-weight: bold;
    color: #333;
    margin: 0;
}

.stage-stats {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    margin: 25px 0;
}

.stage-stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.stat-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 15px;
    border-radius: 20px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stat-badge-icon {
    font-size: 1.1rem;
}

.stat-badge-value {
    font-size: 1.3rem;
}

.tactics-badge {
    background-color: #E3F2FD;
    color: #2196F3;
}

.research-badge {
    background-color: #F3E5F5;
    color: #9C27B0;
}

.calculation-badge {
    background-color: #E8F5E9;
    color: #4CAF50;
}

.stat-badge-label {
    font-size: 0.85rem;
    color: #666;
    font-weight: 500;
}

.stage-total {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 2px solid #f0f0f0;
    text-align: center;
    font-size: 1.1rem;
}

.total-label {
    color: #666;
    margin-right: 10px;
}

.total-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--gaissa_green);
}

/* Getting Started Guide */
.getting-started {
    margin-bottom: 60px;
}

.guide-card {
    text-align: center;
    border-radius: 15px;
    height: 100%;
    position: relative;
    transition: all 0.3s ease;
}

.guide-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.guide-number {
    position: absolute;
    top: 15px;
    right: 15px;
    width: 40px;
    height: 40px;
    background: var(--gaissa_green);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    font-weight: bold;
}

.guide-icon {
    font-size: 3rem;
    color: var(--gaissa_green);
    margin-bottom: 20px;
    margin-top: 10px;
}

.guide-title {
    font-size: 1.3rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 15px;
}

.guide-description {
    color: #666;
    line-height: 1.6;
    margin-bottom: 25px;
    min-height: 80px;
}

.guide-button {
    background-color: var(--gaissa_green);
    border-color: var(--gaissa_green);
    width: 100%;
}

.guide-button:hover {
    background-color: #6fa843;
    border-color: #6fa843;
}

/* Call to Action */
.cta-section {
    margin-bottom: 40px;
}

.cta-card {
    text-align: center;
    padding: 50px 30px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 20px;
}

.cta-card h2 {
    font-size: 2rem;
    color: var(--gaissa_green);
    margin-bottom: 15px;
}

.cta-card p {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 30px;
}

.cta-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
}

.cta-buttons .el-button {
    min-width: 200px;
    margin-left: 0;
}

.cta-buttons .el-button--primary {
    background-color: var(--gaissa_green);
    border-color: var(--gaissa_green);
}

.cta-buttons .el-button--primary:hover {
    background-color: #6fa843;
    border-color: #6fa843;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }

    .hero-subtitle {
        font-size: 1rem;
    }

    .section-title {
        font-size: 1.5rem;
    }

    .stat-number {
        font-size: 2.5rem;
    }

    .guide-description {
        min-height: auto;
    }

    .cta-card h2 {
        font-size: 1.5rem;
    }

    .cta-buttons {
        flex-direction: column;
        align-items: stretch;
    }

    .cta-buttons .el-button {
        width: 100%;
    }
}

@media (max-width: 992px) {
    .guide-card {
        padding: 10px;
    }

    .pipeline-stage-card {
        padding: 10px;
    }
}

</style>
