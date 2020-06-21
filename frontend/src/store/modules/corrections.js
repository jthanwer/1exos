import api from "@/services/api";
import correctionsService from "@/services/correctionsService";

const state = {
  postedCorrections: [],
  unlockedCorrections: []
};

const mutations = {
  SET_POSTED_CORRECTIONS(state, corrections) {
    state.postedCorrections = corrections;
  },
  POST_CORRECTION(state, newCorrection) {
    state.postedCorrections.push(newCorrection);
  },
  DELETE_CORRECTION(state, data_index) {
    state.postedCorrections.splice(data_index, 1);
  },
  SET_UNLOCKED_CORRECTIONS(state, corrections) {
    state.unlockedCorrections = corrections;
  },
  UNLOCK_CORRECTION(state, correction) {
    state.unlockedCorrections.push(correction);
  }
};

const actions = {
  loadPostedCorrections({ commit }) {
    correctionsService
      .getMyPostedCorrections()
      .then(data => {
        commit("SET_POSTED_CORRECTIONS", data.results);
      })
      .catch(error => {});
  },
  loadUnlockedCorrections({ commit }) {
    correctionsService
      .getMyUnlockedCorrections()
      .then(data => {
        commit("SET_UNLOCKED_CORRECTIONS", data.results);
      })
      .catch(error => {});
  },
  postCorrection({ dispatch, commit }, newCorrection) {
    return new Promise((resolve, reject) => {
      correctionsService
        .postCorrection(newCorrection)
        .then(data => {
          commit("POST_CORRECTION", data);
          resolve(data);
        })
        .catch(error => {});
    });
  },
  deleteCorrection({ dispatch, commit }, payload) {
    correctionsService
      .deleteCorrection(payload.id)
      .then(data => {
        commit("DELETE_CORRECTION", payload.data_index);
      })
      .catch(error => {});
  },
  downloadFile({ dispatch }, exo) {
    correctionsService.downloadFile(exo.id).then(data => {
      const url = window.URL.createObjectURL(new Blob([data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", exo.name);
      document.body.appendChild(link);
      link.click();
    });
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
