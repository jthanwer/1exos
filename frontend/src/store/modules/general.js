import api from "@/services/api";
import generalService from "@/services/generalService";

const state = {
  constants: {},
};

const getters = {};

const mutations = {
  SET_CONSTANTS(state, constants) {
    state.constants = constants;
  },
};

const actions = {
  updateConstants({ commit }) {
    generalService.fetchConstants().then(data => {
      commit("SET_CONSTANTS", data);
    });
  },
}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};