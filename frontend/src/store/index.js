import Vue from "vue";
import Vuex from "vuex";
import authentication from "./modules/authentication";
import files from "./modules/files";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    authentication,
    files
  }
});