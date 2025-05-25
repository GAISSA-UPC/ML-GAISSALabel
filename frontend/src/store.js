import { createStore } from 'vuex'
import createPersistedState from "vuex-persistedstate";
import configuration from './store/modules/configuration';
import auth from './store/modules/auth';

const store = createStore({
    modules: {
        configuration,
        auth
    },
    plugins: [createPersistedState()],
})

export default store