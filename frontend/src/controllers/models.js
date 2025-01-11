import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        const responseModels = await axios.get("/api/models/", { params: filters });
        return responseModels
    },
    async retrieve(id) {
        const responseModel = await axios.get(`/api/models/${id}.json`)
        return responseModel
    },
    async create(data) {
        const responseModel = await axios.post(`/api/models.json`, data)
        return responseModel
    }
}