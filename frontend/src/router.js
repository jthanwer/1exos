import Vue from "vue";
import Router from "vue-router";
import axios from "axios";

import Home from "@/views/Home.vue";
import Search from "@/views/Search.vue";
import PostExo from "@/views/PostExo.vue";
import PostExoWithCorrec from "@/views/PostExoWithCorrec.vue";
import ExerciceDetail from "@/views/ExerciceDetail.vue";
import CorrectionDetail from "@/views/CorrectionDetail.vue";
import ExerciceCorrections from "@/views/ExerciceCorrections.vue";

import Profile from "@/views/Profile.vue";
import MoneyBox from "@/views/MoneyBox.vue";
import Recharge from "@/views/Recharge.vue";
import MyExercices from "@/views/MyExercices.vue";
import MyCorrections from "@/views/MyCorrections.vue";

import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";
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
    next("/se-connecter");
  }
};

export default new Router({
  mode: "history",
  base: "/",
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/exercice/:id/",
      name: "exercice",
      component: ExerciceDetail,
      props: true,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/exercice/:id/corrections/",
      name: "exo-corrections",
      component: ExerciceCorrections,
      props: true,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/correction/:id/",
      name: "correction",
      component: CorrectionDetail,
      props: true,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/rechercher-un-exo/",
      name: "search",
      component: Search
    },
    {
      path: "/poster-un-enonce/",
      name: "post-exo",
      component: PostExo,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/poster-un-enonce-et-sa-correction/",
      name: "post-exo-with-correc",
      component: PostExoWithCorrec,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/",
      name: "profile",
      component: Profile,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/ma-tirelire/",
      name: "tirelire",
      component: MoneyBox,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/ma-tirelire/recharger/",
      name: "recharge",
      component: Recharge,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/mes-exercices/",
      name: "mes-exercices",
      component: MyExercices,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/mon-compte/mes-corrections/",
      name: "mes-corrections",
      component: MyCorrections,
      beforeEnter: ifAuthenticated
    },
    {
      path: "/creer-un-compte/",
      name: "register",
      component: Register,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: "/se-connecter/",
      name: "login",
      component: Login,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: "/*",
      name: "others",
      component: Home
    }
  ]
});