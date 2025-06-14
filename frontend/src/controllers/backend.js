import axios from "axios"
import store from "@/store";

axios.interceptors.request.use(
    config => {
        config.headers['Accept'] = 'application/json'
        config.headers['Content-Type'] = 'application/json'
        config.baseURL = 'https://gaissalabel.essi.upc.edu:1444'
        if (store.getters['auth/isLogged']) config.headers['Authorization'] = 'Token ' + store.getters['auth/getToken']
        //config.baseURL = 'http://localhost:8000'
        //config.baseURL = 'http://gaissalabel.essi.upc.edu:81'
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

export default axios
