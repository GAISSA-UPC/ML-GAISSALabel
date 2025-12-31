<template>
    <div class="gaissa-tools-home">
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="hero-content">
                <div class="hero-text">
                    <h1 class="hero-title">{{ $t('Welcome to') }}<br>{{ $t('GAISSA Tools') }}</h1>
                    <p class="hero-subtitle">
                        {{ $t('An open-source platform for comprehensible ML model efficiency assessment and ROI analysis') }}
                    </p>
                    <p class="hero-description">
                        {{ $t('GAISSATools provides cutting-edge solutions to evaluate, optimize, and analyze the efficiency and return on investment of your machine learning models.') }}
                    </p>
                </div>
                <div class="hero-image">
                    <div class="hero-illustration">
                        <font-awesome-icon :icon="['fas', 'brain']" class="brain-icon" />
                        <font-awesome-icon :icon="['fas', 'chart-line']" class="chart-icon" />
                        <font-awesome-icon :icon="['fas', 'leaf']" class="leaf-icon" />
                    </div>
                </div>
            </div>
        </section>

        <!-- Tools Section -->
        <section class="tools-section">
            <div class="section-header">
                <h2>{{ $t('Our Tools') }}</h2>
                <p>{{ $t('Choose the right tool for your needs') }}</p>
            </div>
            
            <div class="tools-grid">
                <!-- GAISSALabel Tool -->
                <div class="tool-card gaissalabel-card" v-if="isGAISSALabelEnabled">
                    <div class="tool-header">
                        <div class="tool-icon">
                            <font-awesome-icon :icon="['fas', 'tag']" />
                        </div>
                        <h3>GAISSALabel</h3>
                    </div>
                    <div class="tool-content">
                        <p>{{ $t('Evaluate the environmental footprint of your ML models during training and inference phases.') }}</p>
                        <ul class="tool-features">
                            <li>{{ $t('Training efficiency assessment') }}</li>
                            <li>{{ $t('Inference footprint analysis') }}</li>
                            <li>{{ $t('Model Improvement Suggestions') }}</li>
                            <li>{{ $t('Environmental impact metrics') }}</li>
                        </ul>
                        <div class="tool-stats">
                            <div class="stat">
                                <span class="stat-number">{{ estadistiques.numModels || 0 }}</span>
                                <span class="stat-label">{{ $t('Models') }}</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">{{ estadistiques.numEntrenaments || 0 }}</span>
                                <span class="stat-label">{{ $t('Trainings') }}</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">{{ estadistiques.numInferencies || 0 }}</span>
                                <span class="stat-label">{{ $t('Inferences') }}</span>
                            </div>
                        </div>
                        <el-button type="primary" size="large" @click="navigateToGAISSALabel" class="tool-button">
                            {{ $t('Get Started') }}
                        </el-button>
                    </div>
                </div>                
                <!-- GAISSA ROI Analyzer Tool -->
                <div class="tool-card roi-analyzer-card" v-if="isGAISSAROIAnalyzerEnabled">
                    <div class="new-banner">NEW</div>
                    <div class="tool-header">
                        <div class="tool-icon">
                            <font-awesome-icon :icon="['fas', 'chart-line']" />
                        </div>
                        <h3>GAISSA ROI Analyzer</h3>
                    </div>
                    <div class="tool-content">
                        <p>{{ $t('Analyze the return on investment and business impact of your ML implementations.') }}</p>
                        <ul class="tool-features">
                            <li>{{ $t('ROI calculation and analysis') }}</li>
                            <li>{{ $t('Research repository access') }}</li>
                            <li>{{ $t('Environmental impact assesment') }}</li>
                            <li>{{ $t('Comparative analysis tools') }}</li>
                        </ul>
                        <div class="tool-stats">
                            <div class="stat">
                                <span class="stat-number">{{ roiStats.pipelineStages || 0 }}</span>
                                <span class="stat-label">{{ $t('Stages') }}</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">{{ roiStats.tactics || 0 }}</span>
                                <span class="stat-label">{{ $t('ML Tactics') }}</span>
                            </div>
                            <div class="stat">
                                <span class="stat-number">{{ roiStats.totalAnalyses || 0 }}</span>
                                <span class="stat-label">{{ $t('Analyses') }}</span>
                            </div>
                        </div>
                        <div class="secondary-action-buttons">
                            <el-button type="default" size="large" @click="navigateToROIRepository" class="tool-button-secondary">
                                {{ $t('Browse Research') }}
                            </el-button>
                            <el-button type="default" size="large" @click="navigateToROIAnalysis" class="tool-button-secondary">
                                {{ $t('Start Analysis') }}
                            </el-button>
                        </div>
                        <div class="tool-actions">
                            <el-button type="primary" size="large" @click="navigateToROIAnalyzer" class="tool-button">
                                {{ $t('Get Started') }}
                            </el-button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features-section">
            <div class="section-header">
                <h2>{{ $t('Why Choose GAISSATools?') }}</h2>
            </div>
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-icon">
                        <font-awesome-icon :icon="['fas', 'leaf']" />
                    </div>
                    <h4>{{ $t('Environmental Focus') }}</h4>
                    <p>{{ $t('Reduce the carbon footprint of your ML models with detailed efficiency insights.') }}</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">
                        <font-awesome-icon :icon="['fas', 'chart-bar']" />
                    </div>
                    <h4>{{ $t('Data-Driven Insights') }}</h4>
                    <p>{{ $t('Make informed decisions with comprehensive analytics and visualizations.') }}</p>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">
                        <font-awesome-icon :icon="['fas', 'rocket']" />
                    </div>
                    <h4>{{ $t('Performance Optimization') }}</h4>
                    <p>{{ $t('Identify bottlenecks and optimize your models for better efficiency.') }}</p>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="cta-section">
            <div class="cta-content">
                <h2>{{ $t('Ready to Get Started?') }}</h2>
                <p>{{ $t('Join the journey towards more efficient and sustainable machine learning.') }}</p>
                <div class="cta-buttons">
                    <el-button type="default" size="large" @click="navigateToGAISSALabel" v-if="isGAISSALabelEnabled">
                        {{ $t('Start with GAISSALabel') }}
                    </el-button>
                    <el-button type="primary" size="large" @click="navigateToROIAnalyzer" v-if="isGAISSAROIAnalyzerEnabled">
                        {{ $t('Explore ROI Analyzer') }}
                    </el-button>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import estadistiques from "@/controllers/estadistiques";
import roiStatistics from "@/tools/gaissaroianalyzer/services/statistics";

export default {
    name: "GAISSAToolsHome",
    data() {
        return {
            estadistiques: {},
            roiStats: {
                pipelineStages: 0,
                tactics: 0,
                totalAnalyses: 0,
            }
        };
    },
    computed: {
        isGAISSALabelEnabled() {
            return this.$store.getters['configuration/isGAISSALabelEnabled'];
        },
        isGAISSAROIAnalyzerEnabled() {
            return this.$store.getters['configuration/isGAISSAROIAnalyzerEnabled'];
        }
    },
    methods: {
        async refrescaEstadistiques() {
            try {
                const response = await estadistiques.list();
                this.estadistiques = response.data;
            } catch (error) {
                console.error('Error fetching statistics:', error);
            }
        },
        async fetchROIStatistics() {
            try {
                const data = await roiStatistics.getStatistics();
                if (data) {
                    this.roiStats.pipelineStages = data.total_pipeline_stages || 0;
                    this.roiStats.tactics = data.total_tactics || 0;
                    this.roiStats.totalAnalyses = data.total_research_analyses + data.total_calculation_analyses || 0;
                }
            } catch (error) {
                console.error('Error fetching ROI statistics:', error);
            }
        },
        navigateToGAISSALabel() {
            this.$router.push({ name: 'gaissalabel-home' });
        },
        navigateToROIAnalyzer() {
            this.$router.push({ name: 'GAISSA ROI Analyzer Home' });
        },
        navigateToROIAnalysis() {
            this.$router.push({ name: 'GAISSA ROI Analyzer New Form' });
        },
        navigateToROIRepository() {
            this.$router.push({ name: 'GAISSA ROI Analyzer Research Repository' });
        }
    },
    async mounted() {
        if (this.isGAISSALabelEnabled) {
            await this.refrescaEstadistiques();
        }
        if (this.isGAISSAROIAnalyzerEnabled) {
            await this.fetchROIStatistics();
        }
    },
};
</script>

<style scoped>
.gaissa-tools-home {
    margin: 0 auto;
    padding: 0 20px;
}

/* Hero Section */
.hero-section {
    padding: 60px 0;
    background: #f8f9fa;
    border-radius: 20px;
    margin-bottom: 60px;
}

.hero-content {
    display: flex;
    align-items: center;
    gap: 60px;
    margin: 0 auto;
    padding: 0 10%;
}

.hero-text {
    flex: 1;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 20px;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.5rem;
    color: #34495e;
    margin-bottom: 20px;
    font-weight: 500;
}

.hero-description {
    font-size: 1.1rem;
    color: #5a6c7d;
    line-height: 1.6;
}

.hero-image {
    display: flex;
    justify-content: center;
    align-items: center;
}

.hero-illustration {
    position: relative;
    width: 280px;
    height: 280px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.brain-icon {
    font-size: 6.4rem;
    color: var(--gaissa_green);
    z-index: 3;
}

.chart-icon {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 4rem;
    color: #3498db;
    z-index: 2;
}

.leaf-icon {
    position: absolute;
    bottom: 20px;
    left: 20px;
    font-size: 4rem;
    color: #27ae60;
    z-index: 2;
}

/* Tools Section */
.tools-section {
    margin-bottom: 80px;
}

.section-header {
    text-align: center;
    margin-bottom: 50px;
}

.section-header h2 {
    font-size: 2.5rem;
    color: #2c3e50;
}

.section-header p {
    font-size: 1.2rem;
    color: #5a6c7d;
}

.tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 40px;
    margin-top: 40px;
}

.tool-card {
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
    display: grid;
}

.new-banner {
    position: absolute;
    top: 10px;
    right: -30px;
    background: #e74c3c;
    color: white;
    padding: 5px 40px;
    font-weight: bold;
    transform: rotate(45deg);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    letter-spacing: 1px;
}

.tool-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.gaissalabel-card {
    border-color: var(--gaissa_green);
}

.gaissalabel-card:hover {
    border-color: var(--gaissa_green);
}

.roi-analyzer-card {
    border-color: #3498db;
}

.roi-analyzer-card:hover {
    border-color: #3498db;
}

.tool-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
}

.tool-header h3 {
    font-size: 1.8rem;
    color: #2c3e50;
    margin: 0;
    font-weight: 600;
}

.tool-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
    flex-shrink: 0;
}

.gaissalabel-card .tool-icon {
    background: var(--gaissa_green);
}

.roi-analyzer-card .tool-icon {
    background: #3498db;
}

.tool-content {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.tool-content p {
    font-size: 1.1rem;
    color: #5a6c7d;
    line-height: 1.6;
    margin-bottom: 25px;
}

.tool-features {
    list-style: none;
    padding: 0;
    margin-bottom: 30px;
}

.tool-features li {
    padding: 8px 0;
    position: relative;
    padding-left: 25px;
    color: #34495e;
}

.tool-features li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: var(--gaissa_green);
    font-weight: bold;
}

.tool-stats {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
}

.stat {
    text-align: center;
    flex: 1;
}

.stat-number {
    display: block;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--gaissa_green);
}

.stat-label {
    font-size: 0.9rem;
    color: #5a6c7d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.roi-analyzer-card .stat-number {
    color: #3498db;
}

.tool-actions {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}

.secondary-action-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: nowrap;
    margin-bottom: 15px;
}

.tool-button,
.tool-button-secondary {
    width: 100%;
    height: 50px;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 10px;
    margin-left: 0;
}

.tool-button {
    background: var(--gaissa_green);
    border-color: var(--gaissa_green);
}

.roi-analyzer-card .tool-button {
    background: #3498db;
    border-color: #3498db;
}

/* Features Section */
.features-section {
    background: #f8f9fa;
    padding: 20px 10px;
    border-radius: 20px;
    margin-bottom: 60px;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.feature-item {
    text-align: center;
    padding: 30px 20px;
}

.feature-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: var(--gaissa_green);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    font-size: 1.5rem;
}

.feature-item h4 {
    font-size: 1.3rem;
    color: #2c3e50;
    margin-bottom: 15px;
    font-weight: 600;
}

.feature-item p {
    color: #5a6c7d;
    line-height: 1.6;
}

/* CTA Section */
.cta-section {
    text-align: center;
    padding: 60px 40px;
    background: var(--gaissa_green);
    border-radius: 20px;
    color: white;
    margin-bottom: 60px;
}

.cta-content h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    font-weight: 700;
}

.cta-content p {
    font-size: 1.2rem;
    margin-bottom: 40px;
    opacity: 0.9;
}

.cta-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
}

.cta-buttons .el-button {
    height: 50px;
    padding: 0 30px;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 10px;
}

@media (max-width: 1000px) {
    .hero-section {
        padding: 10px 0;
    }

    .hero-content {
        text-align: center;
        gap: 10px;
        padding: 0 20px;
    }

    .hero-illustration {
        width: 200px;
        height: 200px;
    }

    .brain-icon {
        font-size: 4rem;
    }

    .chart-icon {
        font-size: 2.5rem;
    }

    .leaf-icon {
        font-size: 2.5rem;
    }
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }

    .hero-content {
        flex-direction: column;
    }

    .tools-grid {
        grid-template-columns: 1fr;
    }

    .features-grid {
        grid-template-columns: 1fr;
    }

    .tool-stats {
        gap: 10px;
        padding: 10px;
    }

    .stat {
        padding: 10px 0;
    }

    .stat-number {
        font-size: 1.5rem;
    }

    .stat-label {
        font-size: 0.8rem;
    }

    .cta-buttons {
        flex-direction: column;
        align-items: center;
    }

    .cta-buttons .el-button {
        width: 100%;
        max-width: 300px;
    }

    .tool-card {
        padding: 20px;
    }

    .tool-button-secondary {
        white-space: normal;
        line-height: 1.3;
        height: 60px;
    }

    .cta-buttons {
        flex-direction: column;
    }

    .cta-buttons .el-button {
        margin-left: 0;
    }
}
</style>
