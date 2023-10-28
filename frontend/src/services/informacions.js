import axios from "@/services/backend"

export default {
    async list() {
        const responseInformacions = await axios.get(`/api/informacions`)
        return responseInformacions
    },
    async listFilteredByPhase(phase) {
        const responseInformacions = await axios.get(`/api/informacions/?fase=${phase}`)
        return responseInformacions
    }
}