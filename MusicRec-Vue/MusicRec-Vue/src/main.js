// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import './assets/style/common.less'
import tool from './assets/js/tool'
import store from './store'
import layer from 'vue-layer'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import 'vue-layer/lib/vue-layer.css';
import 'default-passive-events'

Vue.use(ElementUI);
Vue.prototype.$layer = layer(Vue)
Vue.use(tool)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
})
