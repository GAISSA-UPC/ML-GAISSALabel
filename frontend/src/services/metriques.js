import axios from "@/services/backend"

export default {
    async listOrdered() {
        const responseMetriques = await axios.get(`/api/metriques/?ordering=-pes.json`)
        return responseMetriques
    },
    async listOrderedFilteredByPhase(phase) {
        const responseMetriques = await axios.get(`/api/metriques/?fase=${phase}&ordering=-pes.json`)
        return responseMetriques
    },
    async getById(id) {
        const responseMetrica = await axios.get(`/api/metriques/${id}.json`)
        return responseMetrica
    },
    async update(data) {
        const responseMetrica = await axios.put(`/api/metriques/${data.id}/`, data, {
            responseType: 'json'
        })
        return responseMetrica
    },
    async delete(id) {
        const reponseMetrica = await axios.delete(`/api/metriques/${id}.json`)
        return reponseMetrica
    }
}