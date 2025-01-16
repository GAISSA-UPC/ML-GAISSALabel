import axios from "@/controllers/backend";

export default {
    async listByModel(modelId, filters = {}) {
        try {
            const response = await axios.get(`/api/models/${modelId}/roi-analyses/`, { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching ROI analyses by model:", error);
            return null;
        }
    },
    async getAnalysis(modelId, analysisId) {
        try {
            const response = await axios.get(`/api/models/${modelId}/roi-analyses/${analysisId}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching ROI analysis:", error);
            return null;
        }
    },
};