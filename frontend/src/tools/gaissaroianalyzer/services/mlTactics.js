import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/roi/tactics/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching ML tactics:", error);
            return null;
        }
    },
    async getById(id) {
        try {
            const response = await axios.get(`/api/roi/tactics/${id}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching ML tactic:", error);
            return null;
        }
    },
    async getCompatibleTacticsWithArchitecture(architectureId, filters = {}) {
        try {
            const response = await axios.get(`/api/roi/model-architectures/${architectureId}/compatible-tactics/`, { params: filters });
            return response;
        } catch (error) {
            console.error(`Error fetching tactics compatible with architecture ${architectureId}:`, error);
            return null;
        }
    }
}