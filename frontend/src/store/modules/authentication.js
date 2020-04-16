import api from "@/services/api";
import usersService from "@/services/usersService";

const state = {
  token: localStorage.getItem("user-token") || "",
  status: ""
};

const getters = {
  isAuthenticated: state => !!state.token,
  authStatus: station => state.status
};

const mutations = {
  AUTH_REQUEST(state) {
    state.status = "loading";
  },
  AUTH_SUCCESS(state, token) {
    state.status = "success";
    state.token = token;
  },
  AUTH_ERROR(state) {
    state.status = "error";
  },
  AUTH_LOGOUT(state) {
    state.token = "";
  }
};

const actions = {
  registerUser({ commit, dispatch }, user) {
    return new Promise((resolve, reject) => {
      usersService.register(user)
        .then(data => {
          dispatch("authRequest", user)
          resolve(data)
        })
        .catch(err => {
          reject(err)
        });
    });
  },
  authRequest({ commit }, user) {
    return new Promise((resolve, reject) => {
      usersService.authenticate(user)
        .then(data => {
          const token = data.access;
          localStorage.setItem("user-token", token);
          api.defaults.headers["Authorization"] = "Bearer " + token;
          commit("AUTH_SUCCESS", token);
          resolve(data);
        })
        .catch(err => {
          commit("AUTH_ERROR");
          localStorage.removeItem("user-token");
          reject(err);
        });
    });
  },
  authLogout({ commit }) {
    return new Promise((resolve, reject) => {
      commit("AUTH_LOGOUT");
      delete api.defaults.headers["Authorization"];
      localStorage.removeItem("user-token");
      resolve();
    });
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};