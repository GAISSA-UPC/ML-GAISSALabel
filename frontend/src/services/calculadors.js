import axios from "@/services/backend"

export default {
    async calcularEficienciaInferencia(endpoint, input) {
        const data = {
            'endpoint': endpoint,
            'input': input,
        }
        const responseCalculador = await axios.post(`/api/calculadors/inferencia/`, data)
        return responseCalculador['data']
    }
}