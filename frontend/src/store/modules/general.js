import api from "@/services/api";
import generalService from "@/services/generalService";

const state = {
  constants: {
    "START_POINTS": 4,
    "CHANGE": 4,
    "BONUS": 0.2,
    "SELFCORREC_POINTS": -1,
    "DEADLINE_POINTS": 3,
    "MULTIPLECORREC_POINTS": 3,
    "MEAN_PRICES": {
      "0": -1,
      "1": -1,
      "2": -1,
      "3": -1,
      "4": -1,
      "5": -1,
      "6": -1
    }
  }
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