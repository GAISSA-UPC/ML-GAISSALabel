import axios from "axios"
import store from "@/store";

axios.interceptors.request.use(
    config => {
        config.headers['Accept'] = 'application/json'
        config.headers['Content-Type'] = 'application/json'
        
        // Add auth token if logged in
        if (store.getters['auth/isLogged']) {
            config.headers['Authorization'] = 'Token ' + store.getters['auth/getToken']
        }
        
        // Use environment variable for API base URL
        // Automatically uses .env.development or .env.production based on build mode
        config.baseURL = import.meta.env.VITE_API_BASE_URL
        
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

export default axios
