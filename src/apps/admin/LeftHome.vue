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
              <span>用户管理</span>
            </template>
            <el-menu-item
                v-for="(item, index) in userManagementItems"
                :key="index"
                :index="item.path"
                @click="navigateTo(item.path)">
              {{ item.name }}
            </el-menu-item>
          </el-submenu>

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
      user_type: 'admin',
      userManagementItems: [
        {path: '/admin/admin_user', name: '用户'},
        {path: '/admin/admin_auditor', name: '审核员'},
        {path: '/admin/admin_finance', name: '财务'},
        {path: '/admin/admin_admin', name: '管理员'}
      ],
      menuItems: [
        {path: '/admin/UserDepartment', title: '部门管理', icon: 'el-icon-menu'},
        {path: '/admin/Supplier', title: '供应商管理', icon: 'el-icon-menu'},
        {path: '/admin/Material', title: '材料信息管理', icon: 'el-icon-menu'},
        {path: '/admin/finance_MonthlyPlan', title: '月计划（内）申请', icon: 'el-icon-menu'},
        {path: '/admin/finance_MonthlyPlanOuter', title: '月计划（外）申请', icon: 'el-icon-menu'},
        {path: '/admin/finance_DayPlan', title: '日常出库管理', icon: 'el-icon-menu'},
        {path: '/admin/Material_Hoistory_view', title: '出入库历史记录', icon: 'el-icon-menu'},
        {path: '/admin/excel_view', title: '月计划（内）表格数据', icon: 'el-icon-menu'},
        {path: '/admin/excel_view_outer', title: '月计划（外）表格数据', icon: 'el-icon-menu'},

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
