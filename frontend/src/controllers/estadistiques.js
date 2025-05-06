import axios from "@/controllers/backend"

export default {
    async list() {
        const responseEstadistiques = await axios.get(`/api/estadistiques/`)
        return responseEstadistiques
    },
}