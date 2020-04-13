import api from "@/services/api";

export default {
  getFiles() {
    return api.get('files/')
      .then(response => response.data);
  },
  postFile(file) {
    const config = {
      onUploadProgress(e) {
        var percentCompleted = Math.round((e.loaded * 5000) / e.total);
      }
    }
    return api.post('files/', file, config, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => response.data);
  },
  deleteFile(id) {
    return api.delete(`files/${id}/`)
      .then(response => response.data);
  },
  downloadFile(id) {
    return api({
        url: `files/${id}/download/`,
        method: 'GET',
        responseType: 'blob'
      })
      .then(response => response.data);
  }
};