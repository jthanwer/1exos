import api from '@/services/api'

export default {
  getMyPostedCorrections() {
    return api
      .get('corrections/my_posted_corrections/')
      .then(response => response.data)
  },
  getMyUnlockedCorrections() {
    return api
      .get('corrections/my_unlocked_corrections/')
      .then(response => response.data)
  },
  getCorrection(id) {
    return api.get(`corrections/${id}/`).then(response => response.data)
  },
  postCorrection(file) {
    const config = {
      // onUploadProgress(e) {
      //   var percentCompleted = Math.round((e.loaded * 5000) / e.total)
      // }
    }
    return api
      .post('corrections/', file, config, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => response.data)
  },
  deleteCorrection(id) {
    return api.delete(`corrections/${id}/`).then(response => response.data)
  },
  collectAndUnlock(id, prix) {
    return api
      .post(`corrections/${id}/collect_unlock/`, prix)
      .then(response => response.data)
  },
  getRatings(id) {
    return api
      .get(`corrections/${id}/get_ratings/`)
      .then(response => response.data)
  }
}
