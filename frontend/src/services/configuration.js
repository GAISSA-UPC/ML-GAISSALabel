import axios from "@/controllers/backend"

export default {
    async getConfiguration() {
        try {
            const response = await axios.get(`/api/configuracio/`);
            return response;
        } catch (error) {
            console.error("Error fetching configuration:", error);
            return { status: 500, data: null };
        }
    },
    
    async updateConfiguration(data) {
        try {
            const response = await axios.patch(`/api/configuracio/`, data);
            return response;
        } catch (error) {
            console.error("Error updating configuration:", error);
            return { status: 500, data: null };
        }
    }
}
