import axios from "@/services/backend"

export default {
    async listOrdered() {
        const responseMetriques = await axios.get(`/api/metriques/?ordering=-pes.json`)
        return responseMetriques
    },
    async listOrderedFilteredByPhase(phase) {
        const responseMetriques = await axios.get(`/api/metriques/?fase=${phase}&ordering=-pes.json`)
        return responseMetriques
    }
}