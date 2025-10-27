import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/roi/pipeline-stages/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching ML pipeline stages:", error);
            return null;
        }
    },
    async getById(id) {
        try {
            const response = await axios.get(`/api/roi/pipeline-stages/${id}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching ML pipeline stage:", error);
            return null;
        }
    }
}
