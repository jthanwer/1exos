import Vue from "vue";
import Vuex from "vuex";
import authentication from "./modules/authentication";
import year from "./modules/year";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    authentication,
    year
  }
});
