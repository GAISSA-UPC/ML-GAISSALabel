import axios from "@/controllers/backend"

export default {
    async list() {
        const responseEines = await axios.get(`/api/eines.json`)
        return responseEines
    },
    async getById(id) {
        const responseEina = await axios.get(`/api/eines/${id}.json`)
        return responseEina
    },
    async create(data) {
        const responseEina = await axios.post(`/api/eines/`, data, {
            responseType: 'json'
        })
        return responseEina
    },
    async update(data) {
        const responseEina = await axios.put(`/api/eines/${data.id}/`, data, {
            responseType: 'json'
        })
        return responseEina
    },
    async delete(id) {
        const responseEina = await axios.delete(`/api/eines/${id}.json`)
        return responseEina
    }
}