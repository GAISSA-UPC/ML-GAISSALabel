import axios from "@/services/backend"

export default {
    async listByModel(model_id) {
        const responseInference = await axios.get(`/api/models/${model_id}/inferencies.json`)
        return responseInference
    },
    async retrieve(model_id, inference_id) {
        const responseInference = await axios.get(`/api/models/${model_id}/inferencies/${inference_id}.json`)
        return responseInference
    },
}