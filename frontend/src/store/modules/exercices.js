import api from "@/services/api";
import exercicesService from "@/services/exercicesService";

const state = {
  myExercices: []
};

const mutations = {
  SET_MY_EXERCICES(state, exercices) {
    state.myExercices = exercices
  },
  POST_EXERCICE(state, newExercice) {
    state.myExercices.push(newExercice)
  },
  DELETE_EXERCICE(state, data_index) {
    state.myExercices.splice(data_index, 1)
  }
};

const actions = {
  loadMyExercices({ commit }) {
    exercicesService.getMyExercices()
      .then(data => {
        let myExercices = data.results
        commit('SET_MY_EXERCICES', myExercices)
      })
      .catch(error => {
        console.log(error)
      })
  },
  postExercice({ dispatch, commit }, newExercice) {
    return new Promise((resolve, reject) => {
      exercicesService.postExercice(newExercice)
        .then(data => {
          commit('POST_EXERCICE', data)
          resolve(data)
        })
        .catch(error => {
          console.log(error);
        })
    });
  },
  deleteExercice({ dispatch, commit }, payload) {
    exercicesService.deleteExercice(payload.id)
      .then(data => {
        commit('DELETE_EXERCICE', payload.data_index)
      })
      .catch(error => {
        console.log(error)
      })
  },
  downloadFile({ dispatch }, exo) {
    exercicesService.downloadFile(exo.id)
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