import axios from "@/services/backend"

export default {
    async listFilteredByPhase(phase) {
        const responseMetriques = await axios.get(`/api/informacions/?fase=${phase}`)
        return responseMetriques
    }
}