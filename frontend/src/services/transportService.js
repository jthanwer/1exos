import api from "@/services/api";

export default {
  get_transport(transport, year) {
    let endpoint = `${transport}/?year=${year}`;
    return api.get(endpoint)
      .then(response => response.data);
  },
  get_all_transport(transport, year) {
    return api.get(`all-transport/${year}/`)
      .then(response => response.data);
  },
  post_transport(transport, data, id) {
    let endpoint = `${transport}/`;
    return api.post(endpoint, data)
      .then(response => response.data);
  },
  put_transport(transport, data, id) {
    let endpoint = `${transport}/${id}/`;
    return api.put(endpoint, data)
      .then(response => response.data);
  },
  delete_transport(transport, id) {
    let endpoint = `${transport}/${id}/`;
    return api.delete(endpoint, id)
      .then(response => response.data);
  }
};