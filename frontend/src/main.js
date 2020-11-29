import Vue from 'vue'
import App from '@/App.vue'

import router from '@/router'
import store from '@/store/'

import Buefy from 'buefy'
import VueAnalytics from 'vue-analytics'
import '@/utils/vee-validate.js'

import { dateFormatter } from '@/utils/dates'
import { sizeFormatter } from '@/utils/file_size'

Vue.config.productionTip = false

// Filters
Vue.filter('numberFormatter', function(value) {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
})
Vue.filter('dateFormatter', function(value) {
  return dateFormatter(value)
})
Vue.filter('sizeFormatter', function(value) {
  return sizeFormatter(value)
})

// Directives
Vue.directive('click-outside', {
  bind: function(el, binding, vnode) {
    el.clickOutsideEvent = function(event) {
      if (!(el == event.target || el.contains(event.target))) {
        vnode.context[binding.expression](event)
      }
    }
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unbind: function(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
})

// Plugins
Vue.use(Buefy)

// Google Analytics
Vue.use(VueAnalytics, {
  id: 'UA-156993400-1',
  router
})

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
