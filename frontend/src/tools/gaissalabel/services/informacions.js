import axios from "@/controllers/backend"

export default {
    async list() {
        const responseInformacions = await axios.get(`/api/informacions/`)
        return responseInformacions
    },
    async listFilteredByPhase(phase) {
        const responseInformacions = await axios.get(`/api/informacions/?fase=${phase}`)
        return responseInformacions
    },
    async getById(id) {
        const responseInformacio = await axios.get(`/api/informacions/${id}.json`)
        return responseInformacio
    },
    async create(data) {
        const responseInformacio = await axios.post(`/api/informacions/`, data, {
            responseType: 'json'
        })
        return responseInformacio
    },
    async update(data) {
        const responseInformacio = await axios.put(`/api/informacions/${data.id}/`, data, {
            responseType: 'json'
        })
        return responseInformacio
    },
    async delete(id) {
        const responseInformacio = await axios.delete(`/api/informacions/${id}.json`)
        return responseInformacio
    }
}