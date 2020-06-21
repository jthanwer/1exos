import Vue from "vue";
import App from "@/App.vue";

import router from "@/router";
import store from "@/store/";

import Buefy from "buefy";
import "@/utils/vee-validate.js";

import { dateFormatter } from "@/utils/dates";
import { sizeFormatter } from "@/utils/file_size";

Vue.config.productionTip = false;

// Filters
Vue.filter("numberFormatter", function(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
});
Vue.filter("dateFormatter", function(value) {
  return dateFormatter(value);
});
Vue.filter("sizeFormatter", function(value) {
  return sizeFormatter(value);
});

Vue.use(Buefy);

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount("#app");
