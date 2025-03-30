<template>
  <div id="app">
    <div style="display: flex; height: 100vh; overflow: hidden;">
      <div style="width: 250px; background-color: #353d44; height: 100%; display: flex; flex-direction: column;">
        <el-menu
            :default-active="activeMenu"
            background-color="#353d44"
            text-color="#ffffff"
            active-text-color="#ffffff"
            active-background-color="#2c3138"
            style="flex: 1; overflow: auto;">

          <el-menu-item
              v-for="(item, index) in menuItems"
              :key="index"
              :index="item.path"
              @click="navigateTo(item.path)">
            <i :class="item.icon"></i>
            <span>{{ item.title }}</span>
          </el-menu-item>


        </el-menu>

        <el-menu
            :default-active="activeMenu"
            background-color="#353d44"
            text-color="#ffffff"
            active-text-color="#ffffff"
            active-background-color="#2c3138"
            style="margin-top: auto; background-color: #353d44;">
          <el-menu-item
              index="/login"
              @click="logout">
            <i class="el-icon-menu"></i>
            <span>退出登录</span>
          </el-menu-item>
        </el-menu>
      </div>

      <div style="flex: 1; overflow: auto;">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      user_type: 'auditor',
      menuItems: [
        {path: '/auditor/auditor_DayPlan', title: '日常出库审核', icon: 'el-icon-menu'},
        {path: '/auditor/auditor_MonthlyPlan', title: '月计划（内）申请管理', icon: 'el-icon-menu'},
        {path: '/auditor/auditor_MonthlyPlanOuter', title: '月计划（外）申请管理', icon: 'el-icon-menu'},

      ]

    };
  },
  computed: {
    activeMenu() {
      return this.$route.path;
    }
  },
  mounted() {
    this.checkUserStatus();
    this.interval = setInterval(this.checkUserStatus, 3000);
  },
  methods: {
    checkUserStatus() {
      const user_type = localStorage.getItem('user_type');
      const user_id = localStorage.getItem('user_id');

      if (!user_type || user_type === 'none' || !user_id || user_id === 'none' || user_type !== this.user_type) {
        this.$router.push('/login');
        clearInterval(this.interval);
      }
    },
    navigateTo(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },
    logout() {
      this.navigateTo('/login');
    }
  },
  beforeDestroy() {
    clearInterval(this.interval);
  }
}
</script>

<style>

</style>
