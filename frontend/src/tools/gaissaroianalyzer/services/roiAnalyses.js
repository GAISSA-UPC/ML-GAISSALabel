import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/roi/analyses/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching ROI analyses:", error);
            return null;
        }
    },
    
    async getAnalysis(analysisId, params = {}) {
        try {
            const response = await axios.get(`/api/roi/analyses/${analysisId}/`, { params });
            return response.data;
        } catch (error) {
            console.error(`Error fetching analysis ${analysisId}:`, error);
            return null;
        }
    },
    
    async createAnalysis(analysisData) {
        try {
            const response = await axios.post('/api/roi/analyses/', analysisData);
            return response;
        } catch (error) {
            console.error("Error creating ROI analysis:", error);
            return null;
        }
    }
}