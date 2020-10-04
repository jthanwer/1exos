import api from '@/services/api'
import router from '@/router'
import usersService from '@/services/usersService'

const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
  user: null,
  notifications: null
}

const getters = {
  isAuthenticated: state => !!state.token,
  authStatus: state => state.status
}

const mutations = {
  SET_USER(state, user) {
    state.user = user
  },
  SET_NOTIFICATIONS(state, notifications) {
    state.notifications = notifications
  },
  SET_NOTIFICATION_READ(state, notif_id) {
    const data_index = state.notifications.findIndex(
      element => element.id == notif_id
    )
    state.notifications[data_index].unread = false
  },
  AUTH_REQUEST(state) {
    state.status = 'pending'
  },
  AUTH_SUCCESS(state, token) {
    state.status = 'success'
    state.token = token
  },
  AUTH_ERROR(state) {
    state.status = 'error'
  },
  AUTH_LOGOUT(state) {
    state.token = ''
    state.user = null
  }
}

const actions = {
  registerUser({ commit }, user) {
    return new Promise((resolve, reject) => {
      usersService
        .register(user)
        .then(data => {
          resolve(data)
        })
        .catch(err => {
          reject(err)
        })
    })
  },
  authRequest({ commit, dispatch }, user) {
    return new Promise((resolve, reject) => {
      usersService
        .authenticate(user)
        .then(data => {
          const token = data.access
          localStorage.setItem('user-token', token)
          api.defaults.headers['Authorization'] = 'Bearer ' + token
          commit('AUTH_SUCCESS', token)
          dispatch('getProfileUser')
          dispatch('exercices/loadPostedExercices', null, { root: true })
          dispatch('exercices/loadLikedExercices', null, { root: true })
          dispatch('corrections/loadPostedCorrections', null, { root: true })
          dispatch('corrections/loadUnlockedCorrections', null, { root: true })
          resolve(data)
        })
        .catch(err => {
          commit('AUTH_ERROR')
          localStorage.removeItem('user-token')
          reject(err)
        })
    })
  },
  authLogout({ commit }) {
    return new Promise(resolve => {
      commit('AUTH_LOGOUT')
      delete api.defaults.headers['Authorization']
      localStorage.removeItem('user-token')
      router.push({ name: 'home' })
      resolve()
    })
  },
  getProfileUser({ commit }) {
    return new Promise(resolve => {
      usersService.get_profile().then(data => {
        commit('SET_USER', data)
        resolve(data)
      })
    })
  },
  updateProfileUser({ commit }, updated_user) {
    commit('SET_USER', updated_user)
  },
  getNotifications({ commit }) {
    return new Promise(resolve => {
      usersService.getNotifications().then(data => {
        commit('SET_NOTIFICATIONS', data)
        resolve(data)
      })
    })
  },
  setNotificationRead({ commit }, notif_id) {
    return new Promise(resolve => {
      usersService.setNotificationRead(notif_id).then(data => {
        commit('SET_NOTIFICATION_READ', notif_id)
        resolve(data)
      })
    })
  }
}
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
