import configurationService from "@/services/configuration";

const state = {
    gaissa_label_enabled: true,
    gaissa_roi_analyzer_enabled: true,
    loaded: false
};

const getters = {
    isGAISSALabelEnabled: state => state.gaissa_label_enabled,
    isGAISSAROIAnalyzerEnabled: state => state.gaissa_roi_analyzer_enabled,
    isConfigLoaded: state => state.loaded
};

const actions = {
    async fetchConfiguration({ commit }) {
        try {
            const response = await configurationService.getConfiguration();
            if (response.status === 200) {
                commit('SET_CONFIGURATION', response.data);
            }
            return response;
        } catch (error) {
            console.error('Error fetching configuration:', error);
            throw error;
        }
    },
    async updateConfiguration({ commit }, config) {
        try {
            const response = await configurationService.updateConfiguration(config);
            if (response.status === 200) {
                commit('SET_CONFIGURATION', config);
            }
            return response;
        } catch (error) {
            console.error('Error updating configuration:', error);
            throw error;
        }
    }
};

const mutations = {
    SET_CONFIGURATION(state, config) {
        state.gaissa_label_enabled = config.gaissa_label_enabled;
        state.gaissa_roi_analyzer_enabled = config.gaissa_roi_analyzer_enabled;
        state.loaded = true;
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
