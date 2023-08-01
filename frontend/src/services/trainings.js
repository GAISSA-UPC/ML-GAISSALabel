import axios from "@/services/backend"

export default {
    async retrieve(model_id, training_id) {
        const responseTraining = await axios.get(`/api/models/${model_id}/entrenaments/${training_id}.json`)
        console.log("responseTraining")
        console.log(responseTraining)
        return responseTraining
    }
}