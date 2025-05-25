<template>
    <h1>{{ $t("Tools Configuration") }}</h1><br>
    
    <p>{{ $t('This page allows you to enable or disable the tools available in GAISSA. When disabled, users will not be able to access any functionality of that tool in the backend') }}</p><br>
    
    <div v-if="statusMessage">
        <el-alert v-if="status === 'config-update-ok'" 
                  :title="$t('Configuration successfully updated')" 
                  type="success" 
                  @close="statusMessage = ''" />
        <el-alert v-else-if="status === 'config-update-ko'" 
                  :title="$t('There was an error while updating the configuration')" 
                  type="error" 
                  @close="statusMessage = ''" />
        <br>
    </div>
    
    <el-form label-position="top">
        <h3 class="section-title">{{ $t("GAISSALabel") }}</h3><br>
        <el-form-item :label="$t('Enable GAISSALabel')">
            <el-switch
                v-model="config.gaissa_label_enabled"
                active-color="var(--gaissa_green)"
            />
        </el-form-item>
        <br>
        
        <h3 class="section-title">{{ $t("GAISSA ROI Analyzer") }}</h3><br>
        <el-form-item :label="$t('Enable GAISSA ROI Analyzer')">
            <el-switch
                v-model="config.gaissa_roi_analyzer_enabled"
                active-color="var(--gaissa_green)"
            />
        </el-form-item>
        <br>
        
        <el-button
            @click="updateConfiguration"
            color="var(--gaissa_green)"
        >
            {{ $t('Save configuration') }}
        </el-button>
    </el-form><br>
</template>

<script>

import configurationService from "@/services/configuration";

export default {
    name: "AdminTools",
    data() {
        return {
            config: {
                gaissa_label_enabled: true,
                gaissa_roi_analyzer_enabled: true
            },
            status: '',
            statusMessage: ''
        };
    },
    computed: {
        ...mapGetters({
            isConfigLoaded: 'configuration/isConfigLoaded',
            isGAISSALabelEnabled: 'configuration/isGAISSALabelEnabled',
            isGAISSAROIAnalyzerEnabled: 'configuration/isGAISSAROIAnalyzerEnabled'
        })
    },
    methods: {
        async fetchConfiguration() {
            if (this.isConfigLoaded) {
                // We use stroed values if they are leaded
                this.config = {
                    gaissa_label_enabled: this.isGAISSALabelEnabled,
                    gaissa_label_enabled: this.isGAISSALabelEnabled
                }
            }
            else {
                // If they are not loaded, we fetch them from the API
                const response = await configurationService.getConfiguration();
                if (response.status === 200) {
                    this.config = response.data;
                }
            }
        },
        async updateConfiguration() {
            try {
                const response = await this.$store.dispatch('configuration/updateConfiguration', this.config);
                this.statusMessage = true;
                if (response.status === 200) {
                    this.status = 'config-update-ok';
                } else {
                    this.status = 'config-update-ko';
                }
                window.scrollTo({top: 0});
            } catch (error) {
                this.statusMessage = true;
                this.status = 'config-update-ko';
                console.error('Error updating configuration:', error);
                window.scrollTo({top: 0});
            }
        }
    },
    async mounted() {
        await this.fetchConfiguration();
    }
};
</script>

<style scoped>
.section-title {
    color: var(--gaissa_green);
    font-weight: bold;
}
</style>
