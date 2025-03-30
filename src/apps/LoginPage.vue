<template>
  <div id="app">
    <div style="display: flex">
      <div style="flex: 8;background-color: #0058a3;height: 100vh">
        <center>
          <div style="height: 35vh"></div>
          <div style="width: 50%;text-align: left">
            <div>
              <a style="font-size: 40px;color: #ffdb00;font-weight: 900">欢迎!</a>
            </div>
            <div style="padding: 20px 0">
              <a style="font-size: 40px;color: #ffffff;font-weight: 900">IM-消耗品</a>
            </div>
          </div>
        </center>
      </div>
      <div style="flex: 13;background-color: #ffffff;height: 100vh">
        <center>
          <div style="height: 30vh"></div>
          <div style="width: 50%;text-align: left">
            <div>
              <a style="font-size: 30px;color: #111111;"></a>
            </div>
            <div style="padding: 20px 0">
              <div style="padding: 10px 0">
                <el-input v-model="login.username" placeholder="请输入用户名" clearable></el-input>
              </div>
              <div style="padding: 10px 0">
                <el-input v-model="login.password" type="password" placeholder="请输入密码" clearable></el-input>
              </div>

              <div style="padding: 10px 0">
                <el-button @click="loginPost" style="width: 100%" type="primary">登录</el-button>
              </div>

              <div v-if="errorMessage" style="color: red; text-align: center;">
                {{ errorMessage }}
              </div>
            </div>
          </div>
        </center>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      login: {
        username: '',
        password: '',
      },
      errorMessage: ''
    };
  },
  mounted() {
    localStorage.removeItem('user_type');
    localStorage.removeItem('user_id');
  },
  methods: {
    loginPost() {
      if (!this.login.username || !this.login.password) {
        this.errorMessage = '账号和密码不能为空';
        return;
      }
      this.errorMessage = '';
      this.$axios.post('/public/login', this.login)
          .then(res => {
            if (res.data.code == '1') {
              localStorage.setItem('user_type', res.data.user_type_value);
              localStorage.setItem('user_id', res.data.user_id);
              // 根据用户类型进行路由跳转
              if (res.data.user_type_value === 'user') {
                this.$router.push('/user/user_MonthlyPlan');
              } else if (res.data.user_type_value === 'auditor') {
                this.$router.push('/auditor/auditor_DayPlan');
              } else if (res.data.user_type_value === 'finance') {
                this.$router.push('/finance/Supplier');
              } else if (res.data.user_type_value === 'admin') {
                this.$router.push('/admin/admin_user');
              }
            }
          })
          .catch(err => {
            this.errorMessage = '登录失败，请检查您的账号和密码';
            console.error(err);
          });
    }
  }
};
</script>
