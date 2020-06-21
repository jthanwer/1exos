import axios from "axios";
import { CSRF_TOKEN } from "./csrf_token";
import store from "@/store";

let token = localStorage.getItem("user-token") || "";

const api = axios.create({
  baseURL: "/api/",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    Authorization: token ? "Bearer " + token : "",
    "X-CSRFTOKEN": CSRF_TOKEN
  }
});

api.interceptors.response.use(undefined, err => {
  let res = err.response;
  if (res.status === 401 && res.config) {
    store.dispatch("authentication/authLogout");
  } else {
    return new Promise((resolve, reject) => {
      reject(err);
    });
  }
});

export default api;
