import Vue from "vue";
import App from "./App.vue";
import axios from "axios";
import VModal from "vue-js-modal";
import "./assets/tailwind.css";

axios.defaults.baseURL = "/bolts";
Vue.prototype.$http = axios;

Vue.config.productionTip = false;

Vue.use(VModal);

new Vue({
  render: (h) => h(App),
}).$mount("#app");
