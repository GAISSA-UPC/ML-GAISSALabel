import axios from "@/services/backend"

export default {
    async list() {
        const responseEstadistiques = await axios.get(`/api/estadistiques/`)
        return responseEstadistiques
    },
}