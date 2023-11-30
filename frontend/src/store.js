import { createStore } from 'vuex'
import createPersistedState from "vuex-persistedstate";

const store = createStore({
    state: {
        token: null,
    },
    getters: {
        getToken(state) {
            return state.token
        },
        isLogged(state) {
            return state.token !== null
        }
    },
    mutations: {
        setToken(state, token) {
            state.token = token
        },
        logout(state) {
            state.token = null
        }
    },
    plugins: [createPersistedState()],
})

export default store