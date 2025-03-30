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

          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>月计划申请</span>
            </template>
            <el-menu-item
                v-for="(item, index) in userManagementItems1"
                :key="index"
                :index="item.path"
                @click="navigateTo(item.path)">
              {{ item.name }}
            </el-menu-item>
          </el-submenu>


          <el-submenu index="3">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>日计划申请</span>
            </template>
            <el-menu-item
                v-for="(item, index) in userManagementItems3"
                :key="index"
                :index="item.path"
                @click="navigateTo(item.path)">
              {{ item.name }}
            </el-menu-item>
          </el-submenu>

          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-date"></i>
              <span>计划外申请</span>
            </template>
            <el-menu-item
                v-for="(item, index) in userManagementItems2"
                :key="index"
                :index="item.path"
                @click="navigateTo(item.path)">
              {{ item.name }}
            </el-menu-item>
          </el-submenu>


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
      user_type: 'user',
      userManagementItems1: [
        {path: '/user/user_MonthlyPlan', name: '计划内申请'},
        {path: '/user/user_MonthlyPlanHistory', name: '计划内历史记录'},
      ],
      userManagementItems2: [
        {path: '/user/MonthlyPlanOuter', name: '计划外申请'},
        {path: '/user/MonthlyPlanOuterHistory', name: '计划外历史记录'},
      ],
      userManagementItems3: [
        {path: '/user/DayPlan', name: '日消耗申请'},
        {path: '/user/DayPlanHistory', name: '日消耗历史记录'},
      ],

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
