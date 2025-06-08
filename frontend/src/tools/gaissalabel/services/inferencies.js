import axios from "@/controllers/backend"

export default {
    async listByModel(model_id) {
        const responseInference = await axios.get(`/api/gaissalabel/models/${model_id}/inferencies.json`)
        return responseInference
    },
    async retrieve(model_id, inference_id) {
        const responseInference = await axios.get(`/api/gaissalabel/models/${model_id}/inferencies/${inference_id}.json`)
        return responseInference
    },
    async create(model_id, results, informacions) {
        let results_adapted = {}
        results.forEach(result => {
            results_adapted[result.id] = (!result.valor) ? null : result.valor
        })
        let informacions_adapted = {}
        informacions.forEach(info => {
            if (info.valor) informacions_adapted[info.id] = info.valor
        })

        const inference = {
            'resultats_info': results_adapted,
            'infoAddicional_valors': informacions_adapted,
        }

        const responseInference = await axios.post(`/api/gaissalabel/models/${model_id}/inferencies.json`, inference)
        return responseInference
    },
}