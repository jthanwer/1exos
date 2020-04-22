import api from "@/services/api";
import correctionsService from "@/services/correctionsService";

const state = {
  myCorrections: []
};

const mutations = {
  SET_MY_CORRECTIONS(state, exercices) {
    state.myCorrections = exercices
  },
  POST_CORRECTION(state, newCorrection) {
    state.myCorrections.push(newCorrection)
  },
  DELETE_CORRECTION(state, data_index) {
    state.myCorrections.splice(data_index, 1)
  }
};

const actions = {
  loadMyCorrections({ commit }) {
    correctionsService.getMyCorrections()
      .then(data => {
        let myCorrections = data.results
        commit('SET_MY_CORRECTIONS', myCorrections)
      })
      .catch(error => {
        console.log(error)
      })
  },
  postCorrection({ dispatch, commit }, newCorrection) {
    return new Promise((resolve, reject) => {
      console.log(newCorrection)
      correctionsService.postCorrection(newCorrection)
        .then(data => {
          commit('POST_CORRECTION', data)
          resolve(data)
        })
        .catch(error => {
          console.log(error);
        })
    });
  },
  deleteCorrection({ dispatch, commit }, payload) {
    correctionsService.deleteCorrection(payload.id)
      .then(data => {
        commit('DELETE_CORRECTION', payload.data_index)
      })
      .catch(error => {
        console.log(error)
      })
  },
  downloadFile({ dispatch }, exo) {
    correctionsService.downloadFile(exo.id)
      .then((data) => {
        const url = window.URL.createObjectURL(new Blob([data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', exo.name);
        document.body.appendChild(link);
        link.click();
      })
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};