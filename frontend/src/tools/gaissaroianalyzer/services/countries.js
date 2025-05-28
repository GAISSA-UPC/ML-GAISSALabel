import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/roi/countries/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching countries:", error);
            return null;
        }
    },
    async getById(id) {
        try {
            const response = await axios.get(`/api/roi/countries/${id}/`);
            return response.data;
        } catch (error) {
            console.error("Error fetching country:", error);
            return null;
        }
    }
}
