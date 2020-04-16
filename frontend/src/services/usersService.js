import api from "@/services/api";

export default {
  authenticate(user) {
    return api.post("token/", user)
      .then(response => response.data);
  },
  register(user) {
    return api.post("users/", user)
      .then(response => response.data);
  },
  getClientSecret(payload) {
    console.log(payload);
    return api.post("users/client_secret/", payload)
      .then(response => response.data)
  }
};