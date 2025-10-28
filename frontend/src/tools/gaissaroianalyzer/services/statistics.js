import axios from "@/controllers/backend"

export default {
    async getStatistics() {
        const response = await axios.get(`/api/roi/statistics/`)
        return response.data
    }
}
