import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/optimization-techniques/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching optimization techniques:", error);
            return null;
        }
    },
}