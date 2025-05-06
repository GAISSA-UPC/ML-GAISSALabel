import axios from "axios"
import store from "@/store";

axios.interceptors.request.use(
    config => {
        config.headers['Accept'] = 'application/json'
        config.headers['Content-Type'] = 'application/json'
        config.baseURL = 'https://gaissalabel.essi.upc.edu:1444'
        if (store.getters.isLogged) config.headers['Authorization'] = 'Token ' + store.getters.getToken
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

export default axios
