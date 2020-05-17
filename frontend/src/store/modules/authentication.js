import api from "@/services/api";
import usersService from "@/services/usersService";

const state = {
  token: localStorage.getItem("user-token") || "",
  status: "",
  user: null
};

const getters = {
  isAuthenticated: state => !!state.token,
  authStatus: state => state.status
};

const mutations = {
  SET_USER(state, user) {
    state.user = user;
  },
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
    state.user = "";
  }
};

const actions = {
  registerUser({ commit, dispatch }, user) {
    return new Promise((resolve, reject) => {
      usersService.register(user)
        .then(data => {
          resolve(data)
        })
        .catch(err => {
          reject(err)
        });
    });
  },
  authRequest({ commit, dispatch }, user) {
    return new Promise((resolve, reject) => {
      usersService.authenticate(user)
        .then(data => {
          const token = data.access;
          localStorage.setItem("user-token", token);
          api.defaults.headers["Authorization"] = "Bearer " + token;
          commit("AUTH_SUCCESS", token);
          dispatch("getProfileUser")
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
  },
  getProfileUser({ commit, getters }) {
    if (getters.isAuthenticated) {
      return new Promise((resolve, reject) => {
        usersService.getProfileUser()
          .then(data => {
            commit("SET_USER", data);
            resolve(data);
          })
      })
    }
  }
}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};