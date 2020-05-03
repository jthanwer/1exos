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
  stripe_createPaymentIntent(payload) {
    return api.post("users/stripe_create_payment_intent/", payload)
      .then(response => response.data)
  },
  stripe_validatePayment(payload) {
    return api.post("users/stripe_validate_payment/", payload)
  }
};