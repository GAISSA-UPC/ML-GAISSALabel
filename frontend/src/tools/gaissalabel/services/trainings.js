import axios from "@/controllers/backend"

export default {
    async listByModel(model_id) {
        const responseTraining = await axios.get(`/api/gaissalabel/models/${model_id}/entrenaments.json`)
        return responseTraining
    },
    async retrieve(model_id, training_id) {
        const responseTraining = await axios.get(`/api/gaissalabel/models/${model_id}/entrenaments/${training_id}.json`)
        return responseTraining
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

        const training = {
            'resultats_info': results_adapted,
            'infoAddicional_valors': informacions_adapted,
        }

        const responseTraining = await axios.post(`/api/gaissalabel/models/${model_id}/entrenaments.json`, training)
        return responseTraining
    },
}