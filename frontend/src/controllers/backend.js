import axios from "axios"
import store from "@/store";

axios.interceptors.request.use(
    config => {
        config.headers['Accept'] = 'application/json'
        config.headers['Content-Type'] = 'application/json'
        if (store.getters.isLogged) config.headers['Authorization'] = 'Token ' + store.getters.getToken
        config.baseURL = 'http://localhost:8000'
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

export default axios