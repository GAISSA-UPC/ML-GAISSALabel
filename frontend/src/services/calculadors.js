import axios from "@/services/backend"

export default {
    async calcularEficienciaInferencia(endpoint, input) {
        const data = {
            'endpoint': endpoint,
            'input': input,
        }
        let responseCalculador = null
        await axios.post(`/api/calculadors/inferencia/`, data)
            .then(response => responseCalculador = response)
            .catch(error => responseCalculador = error)
        return responseCalculador
    }
}