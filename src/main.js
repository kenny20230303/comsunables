import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
//导入element ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

//vue-router
import router from './router';

// 导入Vue-ECharts
import VChart from 'vue-echarts';
// 导入需要的ECharts模块
import 'echarts/lib/chart/pie';
import 'echarts/lib/chart/bar';
import 'echarts/lib/chart/line';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/component/legend';
import 'echarts/lib/component/dataZoom';

Vue.use(ElementUI)

// 注册Vue-ECharts组件
Vue.component('v-chart', VChart)

// 设置 Axios
const axiosInstance = axios.create({
    baseURL: 'http://192.168.110.111:5000',
});
Vue.prototype.$axios = axiosInstance;

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')