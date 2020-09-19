import api from '@/services/api'

export default {
  getPostedCorrections() {
    return api
      .get('corrections/my_posted_corrections/')
      .then(response => response.data)
  },
  getUnlockedCorrections() {
    return api
      .get('corrections/my_unlocked_corrections/')
      .then(response => response.data)
  },
  getCorrection(id) {
    return api.get(`corrections/${id}/`).then(response => response.data)
  },
  postCorrection(correction, config) {
    return api
      .post('corrections/', correction, config)
      .then(response => response.data)
  },
  deleteCorrection(id) {
    return api.delete(`corrections/${id}/`).then(response => response.data)
  },
  collectAndUnlock(id) {
    return api
      .post(`corrections/${id}/collect_unlock/`)
      .then(response => response.data)
  },
  getRatings(id) {
    return api
      .get(`corrections/${id}/get_ratings/`)
      .then(response => response.data)
  }
}
