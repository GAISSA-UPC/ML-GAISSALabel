import axios from "@/controllers/backend"

export default {
    async list(tacticId, filters = {}) {
        try {
            const response = await axios.get(`/api/roi/tactics/${tacticId}/parameter-options/`, { params: filters });
            return response;
        } catch (error) {
            console.error(`Error fetching parameter options for tactic ${tacticId}:`, error);
            return null;
        }
    },
    async getById(tacticId, parameterId) {
        try {
            const response = await axios.get(`/api/roi/tactic-parameter-options/${parameterId}/`);
            return response.data;
        } catch (error) {
            console.error(`Error fetching parameter option ${parameterId}:`, error);
            return null;
        }
    }
}