import correctionsService from '@/services/correctionsService'

const state = {
  postedCorrections: [],
  unlockedCorrections: []
}

const mutations = {
  SET_POSTED_CORRECTIONS(state, corrections) {
    state.postedCorrections = corrections
  },
  POST_CORRECTION(state, newCorrection) {
    state.postedCorrections.push(newCorrection)
  },
  DELETE_CORRECTION(state, data_index) {
    state.postedCorrections.splice(data_index, 1)
  },
  SET_UNLOCKED_CORRECTIONS(state, corrections) {
    state.unlockedCorrections = corrections
  },
  UNLOCK_CORRECTION(state, correction) {
    state.unlockedCorrections.push(correction)
  }
}

const actions = {
  loadPostedCorrections({ commit }) {
    return new Promise((resolve, reject) => {
      correctionsService
        .getMyPostedCorrections()
        .then(data => {
          commit('SET_POSTED_CORRECTIONS', data.results)
          resolve()
        })
        .catch(err => reject(err))
    })
  },
  loadUnlockedCorrections({ commit }) {
    return new Promise((resolve, reject) => {
      correctionsService
        .getMyUnlockedCorrections()
        .then(data => {
          commit('SET_UNLOCKED_CORRECTIONS', data.results)
        })
        .catch(err => reject(err))
    })
  },
  postCorrection({ commit }, payload) {
    let config = payload['config']
    let correction = payload['fd']
    return new Promise((resolve, reject) => {
      correctionsService
        .postCorrection(correction, config)
        .then(data => {
          commit('POST_CORRECTION', data)
          resolve(data)
        })
        .catch(err => reject(err))
    })
  },
  collectAndUnlock({ commit }, correc_id) {
    return new Promise((resolve, reject) => {
      correctionsService
        .collectAndUnlock(correc_id)
        .then(data => {
          commit('UNLOCK_CORRECTION', data)
          resolve(data)
        })
        .catch(err => reject(err))
    })
  },
  deleteCorrection({ commit }, payload) {
    return new Promise((resolve, reject) => {
      correctionsService
        .deleteCorrection(payload.id)
        .then(() => {
          commit('DELETE_CORRECTION', payload.data_index)
          resolve()
        })
        .catch(err => {
          reject(err)
        })
    })
  },
  downloadFile(exo) {
    correctionsService.downloadFile(exo.id).then(data => {
      const url = window.URL.createObjectURL(new Blob([data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', exo.name)
      document.body.appendChild(link)
      link.click()
    })
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
