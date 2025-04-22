import axios from "@/controllers/backend";

export default {
    async listByModel(modelId, filters = {}) {
        try {
            const response = await axios.get(`/api/models/${modelId}/gaissa-roi-analyses/`, { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching GAISSA ROI analyses by model:", error);
            return null;
        }
    },
    async getAnalysis(modelId, analysisId) {
        try {
            const response = await axios.get(`/api/models/${modelId}/gaissa-roi-analyses/${analysisId}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching GAISSA ROI analysis:", error);
            return null;
        }
    },
};