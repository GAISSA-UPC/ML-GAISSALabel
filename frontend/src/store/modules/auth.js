
const state = {
    token: null,
};

const getters = {
    getToken: state => state.token,
    isLogged: state => state.token !== null
};

const actions = {
    login({ commit }, token) {
        commit('SET_TOKEN', token);
    },
    logout({ commit }) {
        commit('SET_TOKEN', null);
    }
};

const mutations = {
    SET_TOKEN(state, token) {
        state.token = token;
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
