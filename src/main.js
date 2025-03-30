import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
//导入element ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

//vue-router
import router from './router';

Vue.use(ElementUI)

// 设置 Axios
const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
});
Vue.prototype.$axios = axiosInstance;

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')