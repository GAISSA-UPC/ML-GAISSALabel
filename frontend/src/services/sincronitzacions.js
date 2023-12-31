import axios from "@/services/backend"

export default {
    async informacio() {
        const responseInfo = await axios.get(`/api/sincronitzacio/`)
        return responseInfo
    },
    async sincronitzar() {
        const responseSincro = await axios.post(`/api/sincronitzacio/`).then(response => {return response})
    .catch(error => {return error})
        return responseSincro
    }
}