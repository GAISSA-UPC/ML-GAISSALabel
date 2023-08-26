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
    async create(model_id, results) {
        let results_adapted = {}
        results.forEach(result => {
            results_adapted[result.id] = (!result.valor) ? null : result.valor
        })

        const training = {
            'resultats_info': results_adapted,
        }
        const responseTraining = await axios.post(`/api/models/${model_id}/entrenaments.json`, training)
        return responseTraining
    },
}