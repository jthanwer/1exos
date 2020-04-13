import axios from "axios";

const state = {
  rowData: []
};

const mutations = {
  SET_FILES(state, files) {
    state.rowData = files
  },
  POST_FILE(state, newFile) {
    state.rowData.push(newFile)
  },
  DELETE_FILE(state, data_index) {
    state.rowData.splice(data_index, 1)
  }
};

const actions = {
  loadFiles({ commit }) {
    axios.get('api/files/')
      .then(data => {
        let rowData = data.data.results
        commit('SET_FILES', rowData)
      })
      .catch(error => {
        console.log(error)
      })
  },
  postFile({ dispatch, commit }, newFile) {
    const config = {
      onUploadProgress(e) {
        var percentCompleted = Math.round((e.loaded * 5000) / e.total);
      }
    };
    axios.post('api/files/', newFile, config, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(res => {
        commit('POST_FILE', res.data)
      })
      .catch(error => {
        console.log(error);
      })
  },
  deleteFile({ dispatch, commit }, file_id, data_index) {
    axios.delete('api/files/' + file_id)
      .then(res => {
        commit('DELETE_FILE', data_index)
      })
      .catch(error => {
        console.log(error)
      })
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};