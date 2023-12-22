import axios from "@/services/backend"

export default {
    async list() {
        const responseEines = await axios.get(`/api/eines.json`)
        return responseEines
    },
    async delete(id) {
        const responseEina = await axios.delete(`/api/eines/${id}.json`)
        return responseEina
    }
}