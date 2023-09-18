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
    async create(model_id, results) {
        let results_adapted = {}
        results.forEach(result => {
            results_adapted[result.id] = (!result.valor) ? null : result.valor
        })

        const inference = {
            'resultats_info': results_adapted,
        }
        const responseInference = await axios.post(`/api/models/${model_id}/inferencies.json`, inference)
        return responseInference
    },
}