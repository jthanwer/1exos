import api from "@/services/api";
import filesService from "@/services/filesService";

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
    // axios.get('api/files/')
    filesService.getFiles()
      .then(data => {
        let rowData = data.results
        commit('SET_FILES', rowData)
      })
      .catch(error => {
        console.log(error)
      })
  },
  postFile({ dispatch, commit }, newFile) {
    filesService.postFile(newFile)
      .then(data => {
        commit('POST_FILE', data)
      })
      .catch(error => {
        console.log(error);
      })
  },
  deleteFile({ dispatch, commit }, file_id, data_index) {
    filesService.deleteFile(file_id)
      .then(data => {
        commit('DELETE_FILE', data_index)
      })
      .catch(error => {
        console.log(error)
      })
  },
  downloadFile({ dispatch }, file) {
    filesService.downloadFile(file.file_id)
      .then((data) => {
        const url = window.URL.createObjectURL(new Blob([data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', file.name);
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