import axios from "@/services/backend"

export default {
    async sincronitzar() {
        const responseSincro = await axios.post(`/api/sincronitzacio/`).then(response => {return response})
    .catch(error => {return error})
        return responseSincro
    }
}