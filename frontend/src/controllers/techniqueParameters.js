import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        try {
            const response = await axios.get('/api/technique-parameters/', { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching technique parameters:", error);
            return null;
        }
    },
}