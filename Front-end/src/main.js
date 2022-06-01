import Vue from 'vue'
import App from './App.vue'
import axios from 'axios';
import router from './router/index.js'
import 'bootstrap'
import '@mdi/font/css/materialdesignicons.css'

Vue.config.productionTip = false
Vue.prototype.$baseUrl = 'http://188.121.120.164:8001'
axios.defaults.withCredentials = true

const app = new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
