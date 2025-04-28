import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/roi/metrics/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching ROI metrics:", error);
            return null;
        }
    },
    async getById(id) {
        try {
            const response = await axios.get(`/api/roi/metrics/${id}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching ROI metric:", error);
            return null;
        }
    },
    async getAplicableMetrics(tacticId) {
        try {
            const response = await axios.get(`/api/roi/tactics/${tacticId}/applicable-metrics/`);
            return response.data;
        } catch (error) {
            console.error(`Error fetching applicable metrics for tactic ${tacticId}:`, error);
            return null;
        }
    }
}