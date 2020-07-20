import api from "@/services/api";
import exercicesService from "@/services/exercicesService";

const state = {
  postedExercices: [],
  likedExercices: []
};

const mutations = {
  SET_POSTED_EXERCICES(state, exercices) {
    state.postedExercices = exercices;
  },
  SET_LIKED_EXERCICES(state, exercices) {
    state.likedExercices = exercices;
  },
  POST_EXERCICE(state, newExercice) {
    state.postedExercices.push(newExercice);
  },
  LIKE_EXERCICE(state, newExercice) {
    state.likedExercices.push(newExercice);
  },
  DELETE_EXERCICE(state, data_index) {
    state.postedExercices.splice(data_index, 1);
  },
  DISLIKE_EXERCICE(state, exercice) {
    const index = state.likedExercices.findIndex(liked_exo => liked_exo.id === exercice.id);
    state.likedExercices.splice(index, 1);
  }
};

const actions = {
  loadPostedExercices({ commit }) {
    return new Promise((resolve, reject) => {
      exercicesService.getPostedExercices()
        .then(data => {
          let postedExercices = data.results;
          commit("SET_POSTED_EXERCICES", postedExercices);
          resolve()
        })
        .catch(err => {
          reject(err)
        })
    })
  },
  loadLikedExercices({ commit }) {
    return new Promise((resolve, reject) => {
      exercicesService.getLikedExercices()
        .then(data => {
          let likedExercices = data.results;
          commit("SET_LIKED_EXERCICES", likedExercices);
          resolve()
        })
        .catch(err => reject(err))
    })
  },
  postExercice({ commit }, newExercice) {
    return new Promise((resolve, reject) => {
      exercicesService.postExercice(newExercice)
        .then(data => {
          commit("POST_EXERCICE", data);
          resolve(data);
        })
        .catch(err => reject(err));
    });
  },
  likeExercice({ commit }, exercice) {
    return new Promise((resolve, reject) => {
      exercicesService.likeExercice(exercice.id)
        .then(() => {
          commit("LIKE_EXERCICE", exercice);
        })
        .catch(err => reject(err));
    });
  },
  deleteExercice({ commit }, payload) {
    exercicesService.deleteExercice(payload.id)
      .then(data => {
        commit("DELETE_EXERCICE", payload.data_index);
      });
  },
  dislikeExercice({ commit }, exercice) {
    exercicesService.dislikeExercice(exercice.id)
      .then(data => {
        commit("DISLIKE_EXERCICE", exercice);
      });
  },
  downloadFile({ dispatch }, exo) {
    exercicesService.downloadFile(exo.id).then(data => {
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