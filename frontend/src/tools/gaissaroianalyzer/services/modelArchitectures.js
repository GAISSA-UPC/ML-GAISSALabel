import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/roi/model-architectures/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching model architectures:", error);
            return null;
        }
    },
    async getById(id) {
        try {
            const response = await axios.get(`/api/roi/model-architectures/${id}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching model architecture:", error);
            return null;
        }
    }
}