import api from '@/services/api'

export default {
  create_rating(payload) {
    return api.post('ratings/', payload).then(response => response.data)
  },
  delete_rating(id) {
    return api.delete(`ratings/${id}/`).then(response => response.data)
  },
  modify_rating(id, payload) {
    return api.patch(`ratings/${id}/`, payload).then(response => response.data)
  }
}
