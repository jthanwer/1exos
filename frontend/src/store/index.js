import Vue from "vue";
import Vuex from "vuex";
import authentication from "./modules/authentication";
import exercices from "./modules/exercices";
import corrections from "./modules/corrections";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    authentication,
    exercices,
    corrections
  }
});
