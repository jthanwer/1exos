import axios from 'axios'
import { CSRF_TOKEN } from './csrf_token'
import store from '@/store'
import router from '@/router'

let token = localStorage.getItem('user-token') || ''

const api = axios.create({
  baseURL: '/api/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: token ? 'Bearer ' + token : '',
    'X-CSRFTOKEN': CSRF_TOKEN
  }
})

// api.interceptors.request.use(
//   function(config) {
//     return config;
//   },
//   function(err) {
//     Promise.reject(err)
//   })

api.interceptors.response.use(undefined, err => {
  return new Promise((resolve, reject) => {
    let res = err.response
    if (res.status === 401 && res.config && res.config.url !== 'token/') {
      store.dispatch('authentication/authLogout').then(() => {
        reject(err)
        router.push({ name: 'login' })
      })
    } else {
      reject(err)
    }
  })
})

export default api
