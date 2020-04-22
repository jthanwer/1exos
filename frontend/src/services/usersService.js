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
  getProfileUser(username) {
    return api.get("users/my_profile/")
      .then(response => response.data);
  },
  getClientSecret(payload) {
    return api.post("users/client_secret/", payload)
      .then(response => response.data)
  },
  validatePayment(payload) {
    return api.post("users/validate_payment/", payload)
      .then(response => response.data)
  }
};