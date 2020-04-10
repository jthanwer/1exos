import api from "@/services/api";

export default {
  get_nb_user_lab() {
    return api.get("user/lab/nbusers/")
      .then(response => response.data);
  },
  get_profile() {
    return api.get("user/profile/")
      .then(response => response.data);
  },
  put_profile(new_profile) {
    return api.put("user/profile/", new_profile)
      .then(response => response.data);
  },
  change_password(data) {
    return api.put("user/profile/change_password/", data)
  },
};