import api from "@/services/api";

export default {
  fetchConstants() {
    return api.get("constants/")
      .then(response => response.data);
  },
};