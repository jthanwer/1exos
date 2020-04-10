import Vue from "vue";
import App from "@/App.vue";

import router from "@/router";
import store from "@/store/";
// import apiService from "@/common/api.service.js";

import Buefy from "buefy";
// import 'buefy/dist/buefy.css';
import VueApexCharts from "vue-apexcharts";
import VeeValidate from "vee-validate";

// import vuetify from '@/plugins/vuetify';

Vue.config.productionTip = false;

// Filters
Vue.filter("splitNumber", function(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
});

// Prototypes
Vue.prototype.$year_items = [
  2010,
  2011,
  2012,
  2013,
  2014,
  2015,
  2016,
  2017,
  2018,
  2019,
  2020,
  2021,
  2022
];
// Vue.prototype.$http = apiService;

Vue.use(Buefy);
Vue.use(VeeValidate);

new Vue({
  store,
  router,
  VueApexCharts,
  render: h => h(App)
}).$mount("#app");
