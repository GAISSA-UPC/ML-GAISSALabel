import axios from "@/controllers/backend"

export default {
    async login(username, password) {
        const data = {
            "username": username,
            "password": password
        }

        let responseLogin = null
        await axios.post(`/api/core/login/admins/`, data)
            .then(response => responseLogin = response)
            .catch(error => responseLogin = error)

        return responseLogin
    }
}