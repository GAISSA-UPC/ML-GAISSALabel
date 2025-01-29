import axios from "@/controllers/backend"

export default {
    async list(techniqueId, filters = {}) {
        try {
            const response = await axios.get(`/api/optimization-techniques/${techniqueId}/technique-parameters/`, { params: filters });
            return response;
        } catch (error) {
            console.error("Error fetching technique parameters:", error);
            return null;
        }
    },
}