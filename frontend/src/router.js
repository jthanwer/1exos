import Vue from "vue";
import Router from "vue-router";
import axios from "axios";

import Home from "@/views/Home.vue";
import Search from "@/views/Search.vue";
import Submit from "@/views/Submit.vue";
import ExerciceDetail from "@/views/ExerciceDetail.vue";

import Profile from "@/views/Profile.vue";
import MoneyBox from "@/views/MoneyBox.vue";
import Recharge from "@/views/Recharge.vue";
import MyExercices from "@/views/MyExercices.vue";

import Register from "@/views/Register.vue";
import store from "@/store";

Vue.use(Router);

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters["authentication/isAuthenticated"]) {
    next();
    return;
  } else {
    next("/");
  }
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters["authentication/isAuthenticated"]) {
    let token = store.state.authentication.token;
    axios.defaults.headers.common["Authorization"] = "Bearer " + token;
    next();
    return;
  } else {
    next("/");
  }
};

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
      path: "/exercice/:id/",
      name: "exercice",
      component: ExerciceDetail,
      props: true
    },
    {
      path: "/rechercher-un-exo/",
      name: "search",
      component: Search,
    },
    {
      path: "/poster-un-enonce/",
      name: "submit",
      component: Submit,
    },
    {
      path: "/mon-compte/",
      name: "profile",
      component: Profile,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/ma-tirelire/",
      name: "moneybox",
      component: MoneyBox,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/mes-exercices/",
      name: "mes-exercices",
      component: MyExercices,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/ma-tirelire/recharger/",
      name: "recharge",
      component: Recharge,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/creer-un-compte/",
      name: "register",
      component: Register,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: "/*",
      name: "others",
      component: Home,
    }
  ]
});