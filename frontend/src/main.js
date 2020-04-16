import Vue from "vue";
import App from "@/App.vue";

import router from "@/router";
import store from "@/store/";

import Buefy from "buefy";
import VueApexCharts from "vue-apexcharts";
import VeeValidate from "vee-validate";

import { dateFormatter } from "@/utils/dates"
import { sizeFormatter } from "@/utils/file_size"

// import vuetify from '@/plugins/vuetify';

Vue.config.productionTip = false;

// Filters
Vue.filter("numberFormatter", function(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
});
Vue.filter('dateFormatter', function(value) {
  return dateFormatter(value);
});
Vue.filter('sizeFormatter', function(value) {
  return sizeFormatter(value);
});



Vue.use(Buefy);
Vue.use(VeeValidate);

new Vue({
  store,
  router,
  VueApexCharts,
  render: h => h(App)
}).$mount("#app");