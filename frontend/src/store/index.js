import Vue from "vue";
import Vuex from "vuex";
import general from "./modules/general";
import authentication from "./modules/authentication";
import exercices from "./modules/exercices";
import corrections from "./modules/corrections";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    general,
    authentication,
    exercices,
    corrections
  }
});