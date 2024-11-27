<template>
    <h1>{{ $t('About') }}</h1><br>

    <h3>{{ $t('GAISSALabel is a tool that can assist you in evaluating both the training and inference phases of any machine learning model. \
    This application has been developed as part of the') }} <a href="https://gaissa.upc.edu/en" target="_blank">{{ $t('GAISSA') }}</a>
        {{ $t('project, at the') }} <a href="https://gessi.upc.edu/en" target="_blank">{{ $t('GESSI') }}</a> {{ $t('research group.') }}</h3><br>
    <h3>{{ $t('By using our platform, you are joining a community of researchers and developers committed to addressing the environmental impact of AI. \
    Your actions can help drive the development of more sustainable practices in machine learning, contributing towards a greener future. \
    Let\'s embark on this journey towards Green AI together!') }}</h3><br>
    <div style="display: flex;justify-content: center;width: 100%;margin-top: 50px">
        <img src="/gaissalogo.webp" style="max-width: 25%" alt="GAISSA logo"/>
    </div>

</template>

<script>
export default {
    name: "AboutView"
};
</script>

<style>
h3 {
    text-align: justify
}
</style>
