import api from '@/services/api'

export default {
  authenticate(user) {
    return api.post('token/', user).then(response => response.data)
  },
  register(user) {
    return api.post('users/', user).then(response => response.data)
  },
  get_profile() {
    return api.get('users/my_profile/').then(response => response.data)
  },
  update_profile(id, payload) {
    return api.patch(`users/${id}/`, payload).then(response => response.data)
  },
  stripe_createPaymentIntent(payload) {
    return api
      .post('users/stripe_create_payment/', payload)
      .then(response => response.data)
  },
  stripe_validatePayment(payload) {
    return api.post('users/stripe_validate_payment/', payload)
  },
  check_credentials(payload) {
    return api
      .post('users/check_credentials/', payload)
      .then(response => response.data)
  },
  change_password(payload) {
    return api.post('users/change_password/', payload)
  },
  reset_password(payload) {
    return api.post('accounts/password/reset/', payload)
  },
  getEtablissements() {
    return api
      .get(`users/etablissements/`)
      .then(response => response.data.results)
  },
  getProfs() {
    return api.get(`users/profs/`).then(response => response.data.results)
  },
  getNotifications() {
    return api.get(`users/notifications/`).then(response => response.data)
  },
  setNotificationRead(id) {
    return api.get(`notifications/${id}/read/`)
  },
  setIsNew() {
    return api.get(`users/set_is_new/`)
  }
}
