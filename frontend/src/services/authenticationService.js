import api from "@/services/api";

export default {
  authenticate(user) {
    return api.post(`token/`, user)
      .then(response => response.data);
  },
  register(user) {
    return api.post("auth/registration/", user)
      .then(response => response.data);
  }
};