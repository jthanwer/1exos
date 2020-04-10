import { CSRF_TOKEN } from "./csrf_token.js";
import axios from "axios";

// async function getJSON(response){
//   if (response.status === 204) return '';
//   return response.json()
// }

// export default function apiService(endpoint, method, data){
//   const config = {
//     method: method || "GET",
//     body: data !== undefined ? JSON.stringify(data) : null,
//     headers : {
//       'content-type': 'application/json',
//       'X-CSRFTOKEN' : CSRF_TOKEN
//     }
//   };
//   return fetch(endpoint, config)
//           .then(getJSON)
// }

export default function apiService(endpoint, method, data) {
  const config = {
    method: method || "get",
    url: endpoint,
    data: data !== undefined ? data : null,
    headers: {
      "content-type": "application/json",
      "X-CSRFTOKEN": CSRF_TOKEN
    }
  };
  return axios(config).catch(error => {
    if (error.response.status === 401) {
      this.$store.dispatch("authentication/authLogout");
      this.$router.push({ name: "login" });
    }
  });
}
