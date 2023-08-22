import axios from "@/services/backend"

export default {
    async listByModel(model_id) {
        const responseTraining = await axios.get(`/api/models/${model_id}/entrenaments.json`)
        return responseTraining
    },
    async retrieve(model_id, training_id) {
        const responseTraining = await axios.get(`/api/models/${model_id}/entrenaments/${training_id}.json`)
        return responseTraining
    },
}