import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/roi/tactics/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching optimization techniques:", error);
            return null;
        }
    },
    async getById(id) {
        try {
            const response = await axios.get(`/api/roi/tactics/${id}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching optimization technique:", error);
            return null;
        }
    },
    async getCompatibleTacticsWithArchitecture(architectureId) {
        try {
            const response = await axios.get(`/api/roi/model-architectures/${architectureId}/compatible-tactics/`);
            return response;
        } catch (error) {
            console.error(`Error fetching techniques compatible with architecture ${architectureId}:`, error);
            return null;
        }
    }
}