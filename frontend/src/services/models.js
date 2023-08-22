import axios from "@/services/backend"

export default {
    async list() {
        const responseModels = await axios.get(`/api/models.json`)
        return responseModels
    }
}