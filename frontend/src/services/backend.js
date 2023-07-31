import axios from "axios"

axios.interceptors.request.use(
    config => {
        config.headers['Accept'] = 'application/json'
        config.headers['Content-Type'] = 'application/json'
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

export default axios