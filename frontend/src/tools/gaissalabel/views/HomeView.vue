<template>
    <div class="gaissalabel-home">
        <!-- Hero Section -->
        <section class="hero-section">
            <h1>{{ $t('Welcome to GAISSALabel!') }}</h1>
            <h2 class="hero-subtitle">
                {{ $t('The tool you are seeking for to easy assess the footprint of ML models and help you improve your models\' efficiency.') }}
            </h2>
        </section>

        <!-- Introduction -->
        <section class="intro-section">
            <p class="intro-text">
                {{ $t('GAISSALabel is a tool that can assist you in evaluating both the training and inference phases of any machine learning model. \
                To navigate through the various available pages, utilize the left menu. \
                During both the training and inference phases, you have the capability to generate efficiency results for your models or retrieve existing ones.') }}
            </p>
        </section>

        <!-- Statistics Overview -->
        <section class="stats-section">
            <h3 class="section-title">{{ $t('For now, we have registered') }}</h3>
            <el-row justify="center" :gutter="30" class="stats-row">
                <el-col :xs="24" :sm="8" :md="8">
                    <el-card class="stat-card" shadow="hover">
                        <div class="stat-icon">
                            <font-awesome-icon :icon="['fas', 'cube']" />
                        </div>
                        <h1 class="stat-number">{{ estadistiques.numModels || 0 }}</h1>
                        <h2 class="stat-label">{{ $t('models') }}</h2>
                    </el-card>
                </el-col>
                <el-col :xs="12" :sm="8" :md="8">
                    <el-card class="stat-card" shadow="hover">
                        <div class="stat-icon">
                            <font-awesome-icon :icon="['fas', 'graduation-cap']" />
                        </div>
                        <h1 class="stat-number">{{ estadistiques.numEntrenaments || 0 }}</h1>
                        <h2 class="stat-label">{{ $t('trainings') }}</h2>
                    </el-card>
                </el-col>
                <el-col :xs="12" :sm="8" :md="8">
                    <el-card class="stat-card" shadow="hover">
                        <div class="stat-icon">
                            <font-awesome-icon :icon="['fas', 'bolt']" />
                        </div>
                        <h1 class="stat-number">{{ estadistiques.numInferencies || 0 }}</h1>
                        <h2 class="stat-label">{{ $t('inferences') }}</h2>
                    </el-card>
                </el-col>
            </el-row>
        </section>

        <!-- Video Section -->
        <section class="video-section">
            <h3 class="section-title">{{ $t('Watch Our Introduction Video') }}</h3>
            <div class="video-container">
                <iframe 
                    src="https://www.youtube.com/embed/GK4DBUwxWDQ" 
                    title="GAISSALabel: A Tool For ML Energy Labeling" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    referrerpolicy="strict-origin-when-cross-origin" 
                    allowfullscreen>
                </iframe>
            </div>
        </section>

        <!-- Research Paper Reference -->
        <section class="paper-section">
            <el-card class="paper-card" shadow="hover">
                <div class="paper-content">
                    <h3 class="paper-title">{{ $t('Published Research') }}</h3>
                    <p class="paper-description">
                        {{ $t('GAISSALabel has been published and presented at the Foundations of Software Engineering Conference (FSE 2024).') }}
                    </p>
                    <div class="paper-citation">
                        <p><strong>{{ $t('Citation') }}:</strong></p>
                        <p class="citation-text">
                            Pau Duran, Joel Castaño, Cristina Gómez, and Silverio Martínez-Fernández. 2024. 
                            GAISSALabel: A Tool for Energy Labeling of ML Models. 
                            In Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering (FSE 2024). 
                            Association for Computing Machinery, New York, NY, USA, 622–626.
                        </p>
                    </div>
                    <el-button 
                        type="primary" 
                        class="paper-button"
                        @click="openPaper">
                        <font-awesome-icon :icon="['fas', 'external-link-alt']" style="margin-right: 8px" />
                        {{ $t('Read the Paper') }}
                    </el-button>
                </div>
            </el-card>
        </section>

        <!-- Call to Action -->
        <section class="cta-section">
            <p class="cta-text">
                {{ $t('We appreciate your trust. Let us start the journey towards creating more environmentally friendly machine learning models!') }}
            </p>
        </section>
    </div>
</template>

<script>
import estadistiques from "@/controllers/estadistiques";

export default {
    name: "HomeView",
    data() {
        return {
            estadistiques: {},
        };
    },
    methods: {
        async refrescaEstadistiques() {
            const response = await estadistiques.list()
            this.estadistiques = response.data
        },
        openPaper() {
            window.open('https://dl.acm.org/doi/10.1145/3663529.3663811', '_blank');
        }
    },
    async mounted() {
        await this.refrescaEstadistiques();
    },
};
</script>

<style scoped>
.gaissalabel-home {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, var(--gaissa_green) 0%, #6fa843 100%);
    border-radius: 20px;
    margin-bottom: 40px;
    color: white;
}

.hero-section h1 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 15px;
    color: white;
}

.hero-subtitle {
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
    opacity: 0.95;
    text-align: center;
    color: white;
}

/* Introduction Section */
.intro-section {
    margin-bottom: 40px;
}

.intro-text {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #5a6c7d;
    text-align: justify;
    max-width: 900px;
    margin: 0 auto;
}

/* Section Titles */
.section-title {
    font-size: 1.8rem;
    font-weight: bold;
    color: var(--gaissa_green);
    text-align: center;
    margin-bottom: 30px;
}

/* Statistics Section */
.stats-section {
    margin-bottom: 50px;
}

.stats-row {
    margin-top: 20px;
}

.stat-card {
    text-align: center;
    border-radius: 15px;
    background-color: var(--gaissa_green_light);
    border: 2px solid var(--gaissa_green);
    transition: all 0.3s ease;
    height: 100%;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.stat-icon {
    font-size: 2.5rem;
    color: var(--gaissa_green);
    margin-bottom: 15px;
}

.stat-number {
    font-size: 3rem;
    font-weight: bold;
    color: var(--gaissa_green);
    margin: 10px 0;
}

.stat-label {
    font-size: 1.2rem;
    color: var(--gaissa_green);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
}

/* Video Section */
.video-section {
    margin: 50px 0;
    text-align: center;
}

.video-container {
    position: relative;
    width: 70%;
    max-width: 996px;
    margin: 0 auto;
    padding-bottom: 39.375%;
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

/* Paper Section */
.paper-section {
    margin: 50px 0;
}

.paper-card {
    border-radius: 15px;
    border: 2px solid var(--gaissa_green);
    transition: all 0.3s ease;
}

.paper-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.paper-content {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
}

.paper-icon {
    flex-shrink: 0;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: var(--gaissa_green);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}

.paper-title {
    font-size: 1.8rem;
    color: var(--gaissa_green);
    margin-bottom: 15px;
    font-weight: 600;
}

.paper-description {
    font-size: 1.1rem;
    color: #5a6c7d;
    line-height: 1.6;
    margin-bottom: 20px;
}

.paper-citation {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    border-left: 4px solid var(--gaissa_green);
}

.paper-citation p {
    margin: 0 0 10px 0;
    color: #34495e;
}

.paper-citation p:last-child {
    margin-bottom: 0;
}

.citation-text {
    font-style: italic;
    color: #5a6c7d;
    line-height: 1.6;
}

.paper-button {
    background-color: var(--gaissa_green);
    border-color: var(--gaissa_green);
    font-size: 1.1rem;
    padding: 12px 30px;
    height: auto;
}

.paper-button:hover {
    background-color: #6fa843;
    border-color: #6fa843;
}

/* Call to Action Section */
.cta-section {
    text-align: center;
    padding: 40px 20px;
    background: #f8f9fa;
    border-radius: 15px;
    margin-bottom: 40px;
}

.cta-text {
    font-size: 1.2rem;
    color: #34495e;
    line-height: 1.8;
    max-width: 800px;
    margin: 0 auto;
    font-weight: 500;
}

/* Responsive Design */
@media (max-width: 992px) {
    .video-container {
        width: 90%;
        padding-bottom: 50.625%; /* Adjust aspect ratio for smaller screens */
    }

    .paper-content {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .stats-row {
        row-gap: 20px;
    }
}

@media (max-width: 768px) {
    .hero-section h1 {
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

    .video-container {
        width: 100%;
        padding-bottom: 56.25%; /* Full 16:9 on mobile */
    }

    .paper-title {
        font-size: 1.5rem;
    }

    .paper-description {
        font-size: 1rem;
    }

    .intro-text {
        text-align: left;
    }
}

@media (max-width: 400px) {
    .stat-number {
        font-size: 2.2rem;
    }

    .stat-label {
        font-size: 0.9rem;
    }
}

</style>
