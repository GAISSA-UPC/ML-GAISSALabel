import axios from "@/services/backend"

export default {
    async list() {
        const responseEines = await axios.get(`/api/eines.json`)
        return responseEines
    }
}