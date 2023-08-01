import axios from "axios"

axios.interceptors.request.use(
    config => {
        config.headers['Accept'] = 'application/json'
        config.headers['Content-Type'] = 'application/json'
        config.baseURL = 'http://localhost:8000'
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

export default axios