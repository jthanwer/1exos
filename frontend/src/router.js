import Vue from "vue";
import Router from "vue-router";
import axios from "axios";

import Home from "@/views/Home.vue";
import Profile from "@/views/Profile.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import store from "@/store";

Vue.use(Router);

// const ifNotAuthenticated = (to, from, next) => {
//   if (!store.getters["authentication/isAuthenticated"]) {
//     next();
//     return;
//   } else {
//     next("/");
//   }
// };
//
// const ifAuthenticated = (to, from, next) => {
//   if (store.getters["authentication/isAuthenticated"]) {
//     // Put the token into header after refreshing
//     let token = store.state.authentication.token;
//     axios.defaults.headers.common["Authorization"] = "Bearer " + token;
//     next();
//     return;
//   } else {
//     next("/login");
//   }
// };

export default new Router({
  mode: "history",
  base: "/",
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/mon-compte",
      name: "profile",
      component: Profile,
      // beforeEnter: ifAuthenticated
    },
    {
      path: "/login",
      name: "login",
      component: Login,
      // beforeEnter: ifNotAuthenticated
    },
    {
      path: "/register",
      name: "register",
      component: Register,
      // beforeEnter: ifNotAuthenticated
    },
    {
      path: "/*",
      name: "others",
      component: Home,
      // beforeEnter: ifAuthenticated
    }
  ]
});