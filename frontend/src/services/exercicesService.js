import api from '@/services/api'

export default {
  getAllExercices() {
    return api.get('exercices/').then(response => response.data)
  },
  getPostedExercices() {
    return api
      .get('exercices/my_posted_exercices/')
      .then(response => response.data)
  },
  getLikedExercices() {
    return api
      .get('exercices/my_liked_exercices/')
      .then(response => response.data)
  },
  searchExercices(text_query) {
    return api.get(`exercices/${text_query}`).then(response => response.data)
  },
  postExercice(file) {
    const config = {
      // onUploadProgress(e) {
      //   var percentCompleted = Math.round((e.loaded * 5000) / e.total)
      // }
    }
    return api
      .post('exercices/', file, config, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => response.data)
  },
  getExercice(id) {
    return api.get(`exercices/${id}/`).then(response => response.data)
  },
  deleteExercice(id) {
    return api.delete(`exercices/${id}/`).then(response => response.data)
  },
  downloadFile(id) {
    return api({
      url: `exercices/${id}/download/`,
      method: 'GET',
      responseType: 'blob'
    }).then(response => response.data)
  },
  getExerciceCorrections(id) {
    return api
      .get(`exercices/${id}/corrections/`)
      .then(response => response.data)
  },
  likeExercice(id) {
    return api.get(`exercices/${id}/like/`)
  },
  dislikeExercice(id) {
    return api.get(`exercices/${id}/dislike/`)
  }
}
