import axios from "axios";
import { CSRF_TOKEN } from "./csrf_token";
import store from '@/store';

let token = localStorage.getItem("user-token") || "";

const api = axios.create({
  baseURL: "/api/",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer " + token,
    "X-CSRFTOKEN": CSRF_TOKEN
  }
});

api.interceptors.response.use(undefined, err => {
  let res = err.response;
  if (res.status === 401 && res.config) {
    store.dispatch('authentication/authLogout');
  }
})

// axios.interceptors.response.use(undefined, err => {
//   let res = err.response;
//   if (res.status === 401 && res.config && !res.config.__isRetryRequest) {
//     return new Promise((resolve, reject) => {
//       refreshLogin(getRefreshToken(),
//         success => {
//           setTokens(success.access_token, success.refresh_token)
//           err.config.__isRetryRequest = true
//           err.config.headers.Authorization = 'Bearer ' + getAccessToken()
//           resolve(axios(err.config))
//         },
//         error => {
//           reject(error)
//         }
//       )
//     });
//   }
// })

export default api