import axios from "@/controllers/backend"

export default {
    async listOrdered() {
        const responseMetriques = await axios.get(`/api/gaissalabel/metriques/?ordering=-pes.json`)
        return responseMetriques
    },
    async listOrderedFilteredByPhase(phase) {
        const responseMetriques = await axios.get(`/api/gaissalabel/metriques/?fase=${phase}&ordering=-pes.json`)
        return responseMetriques
    },
    async getById(id) {
        const responseMetrica = await axios.get(`/api/gaissalabel/metriques/${id}.json`)
        return responseMetrica
    },
    async listQualificacionsOrdre() {
        /*
        Si les qualificacions es poguessin modificar, potser seria més adequat crear un servei qualificacions.js
        Per ara, com que només necessitem aquesta operació, ho posem aquí.
         */
        const responseQualificacions = await axios.get(`/api/gaissalabel/qualificacions/?ordering=ordre`, {
            responseType: 'json'
        })
        return responseQualificacions
    },
    async create(data) {
        const responseMetrica = await axios.post(`/api/gaissalabel/metriques/`, data, {
            responseType: 'json'
        })
        return responseMetrica
    },
    async update(data) {
        const responseMetrica = await axios.put(`/api/gaissalabel/metriques/${data.id}/`, data, {
            responseType: 'json'
        })
        return responseMetrica
    },
    async delete(id) {
        const reponseMetrica = await axios.delete(`/api/gaissalabel/metriques/${id}.json`)
        return reponseMetrica
    }
}