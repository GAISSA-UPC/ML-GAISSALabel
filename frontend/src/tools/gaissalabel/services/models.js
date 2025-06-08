import axios from "@/controllers/backend"

export default {
    async list(filters = {}) {
        const responseModels = await axios.get("/api/gaissalabel/models/", { params: filters });
        return responseModels
    },
    async retrieve(id) {
        const responseModel = await axios.get(`/api/gaissalabel/models/${id}.json`)
        return responseModel
    },
    async create(data) {
        const responseModel = await axios.post(`/api/gaissalabel/models.json`, data)
        return responseModel
    }
}