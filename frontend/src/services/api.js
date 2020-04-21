import axios from "axios";
import { CSRF_TOKEN } from "./csrf_token";

let token = localStorage.getItem("user-token") || "";

export default axios.create({
  baseURL: "/api/",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer " + token,
    "X-CSRFTOKEN": CSRF_TOKEN
  }
});