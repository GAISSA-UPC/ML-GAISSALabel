import axios from "@/controllers/backend"

export default {
    async informacio() {
        const responseInfo = await axios.get(`/api/gaissalabel/sincronitzacio/`)
        return responseInfo
    },
    async sincronitzar() {
        const responseSincro = await axios.post(`/api/gaissalabel/sincronitzacio/`).then(response => {return response})
    .catch(error => {return error})
        return responseSincro
    }
}