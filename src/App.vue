<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    console.log('App.vue.start')
    this.$router.push('/login');

  }
}
</script>


<style>
@font-face {
  font-family: 'YourFont';
  src: url('@/assets/fonts/Public Sans.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}

#app {
  font-family: 'Public Sans', sans-serif;
}

#app {
  -webkit-user-select: text; /* Chrome, Safari, Opera */
  -moz-user-select: text; /* Firefox */
  -ms-user-select: text; /* IE 10+ */
  user-select: text; /* Standard syntax */
}

.el-menu {
  border: 0 !important;
}

.el-menu-item.is-active {
  background-color: #2c3138 !important; /* 设置激活状态的背景颜色 */
}
</style>