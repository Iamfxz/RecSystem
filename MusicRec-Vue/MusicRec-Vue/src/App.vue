<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>

  export default {
    name: 'App',
    // 挂载后验证是否登录，过期
    mounted() {
      if (localStorage.getItem('loginTime')) {
        this.deTime(localStorage.getItem('loginTime'), Date(), 24)
      }
    }
  }
</script>

<style lang="less">
  #app {
    overflow: auto;
    background: url("assets/img/background2.jpg");
  }

  /*改变vue-layer弹层样式*/
  .vl-notify-mask {
    opacity: 0.8;
  }
</style>
