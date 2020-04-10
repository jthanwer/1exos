import axios from "axios";

const state = {
  year: 2019
};

const mutations = {
  INCREASE_YEAR(state, amount = 1) {
    state.year += amount;
  },
  DECREASE_YEAR(state, amount = -1) {
    state.year += amount;
  }
};

const actions = {
  updateYear(context, amount) {
    if (amount >= 0) {
      context.commit("INCREASE_YEAR", amount);
    } else {
      context.commit("DECREASE_YEAR", amount);
    }
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
