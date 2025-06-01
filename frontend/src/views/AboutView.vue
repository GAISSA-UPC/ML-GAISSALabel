<template>
    <h1>{{ $t('About') }}</h1><br>

    <h3>{{ $t('GAISSA Tools is an open-source platform that provides comprehensible cutting-edge solutions for machine learning model efficiency assessment and analysis. \
    This platform includes GAISSALabel for evaluating training and inference phases, and GAISSA ROI Analyzer for return on investment analysis. \
    This application has been developed as part of the') }} <a href="https://gaissa.upc.edu/en" target="_blank">{{ $t('GAISSA') }}</a>
        {{ $t('project, at the') }} <a href="https://gessi.upc.edu/en" target="_blank">{{ $t('GESSI') }}</a> {{ $t('research group.') }}</h3><br>
    <h3>{{ $t('By using our platform, you are joining a community of researchers and developers committed to addressing the environmental impact of AI. \
    Your actions can help drive the development of more sustainable practices in machine learning, contributing towards a greener future. \
    Let\'s embark on this journey towards Green AI together!') }}</h3><br>

    <div class="content-center">
        <div class="image-container">
            <img src="/gaissalogo.webp" style="max-width: 25%" alt="GAISSA logo"/>
        </div>
        
        <!-- Carbon Badge Section -->
        <div class="carbon-section">
            <h3>{{ $t('Website Carbon Footprint') }}</h3>
            <div id="wcb" class="carbonbadge"></div>
        </div>
    </div>
</template>

<script>
export default {
    name: "AboutView",
    mounted() {
        const script = document.createElement('script')
        script.src = 'https://unpkg.com/website-carbon-badges@1.1.3/b.min.js'
        script.defer = true
        document.body.appendChild(script)
    },
    beforeUnmount() {
        const script = document.querySelector('script[src="https://unpkg.com/website-carbon-badges@1.1.3/b.min.js"]')
        if (script) {
            script.remove()
        }
    }
}
</script>

<style scoped>
h3 {
    text-align: justify;
}

.content-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    margin-top: 50px;
}

.image-container {
    width: 100%;
    text-align: center;
    transform: translateX(10px);
}

.carbon-section {
    width: 100%;
    text-align: center;
}

.carbon-section h3 {
    text-align: center;
    margin-bottom: 1rem;
}

#wcb.carbonbadge {
    display: inline-block;
}
</style>