import axios from "@/services/backend"

export default {
    async sincronitzar() {
        const responseSincro = await axios.post(`/api/sincronitzacio/`)
        return responseSincro
    }
}