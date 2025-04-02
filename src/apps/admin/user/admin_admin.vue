<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <!-- Top Button Area -->
    <el-card class="user-card">
      <el-button type="success" size="medium" @click="openDialog()">新增用户</el-button>
    </el-card>

    <!-- Table Area -->
    <el-card class="user-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table
          :data="users"
          style="width: 100%; flex: 1;"
          border
          stripe
      >
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="password" label="密码"></el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="phone" label="电话"></el-table-column>
        <el-table-column prop="user_type" label="用户类型"></el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="editUser(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="deleteUser(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog -->
    <el-dialog
        :title="currentUser.id ? '编辑用户' : '新增用户'"
        :visible.sync="dialogVisible"
        width="30%"
    >


      <el-form :model="currentUser" label-width="80px">
        <el-form-item label="用户名" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
          <el-input v-model="currentUser.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
          <el-input v-model="currentUser.password" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="姓名" :rules="[{ required: true, message: '请输入姓名', trigger: 'blur' }]">
          <el-input v-model="currentUser.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="currentUser.phone" placeholder="请输入电话"></el-input>
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="currentUser.user_type" placeholder="选择用户类型">
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeDialog()">取消</el-button>
        <el-button type="primary" @click="saveUser">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      dialogVisible: false,
      currentUser: {id: null, username: '', name: '', phone: '', user_type: ''},
      usertype: 'admin',
    };
  },

  mounted() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      this.$axios.get('/admin/User', {
        params: {
          usertype: this.usertype
        }
      })
          .then(res => {
            this.users = res.data;
          })
          .catch(err => {
            this.$message.error('获取用户失败: ' + err.message);
          });
    },
    openDialog() {
      this.currentUser = {id: null, username: '', name: '', phone: '', user_type: 'admin'};
      this.dialogVisible = true;
    }
    ,
    editUser(user) {
      this.currentUser = {...user};
      this.dialogVisible = true;
    }
    ,
    deleteUser(user) {
      this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        this.$axios.delete('/admin/User', {data: {id: user.id}})
            .then(() => {
              this.$message.success('删除成功');
              this.fetchUsers();
            })
            .catch(err => {
              this.$message.error('删除失败: ' + err.message);
            });
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    }
    ,
    saveUser() {
      const url = this.currentUser.id ? '/admin/User' : '/admin/User';
      const method = this.currentUser.id ? 'put' : 'post';

      this.$axios[method](url, this.currentUser)
          .then(() => {
            this.$message.success(this.currentUser.id ? '更新成功' : '新增成功');
            this.fetchUsers();
            this.closeDialog();
          })
          .catch(err => {
            this.$message.error('保存失败: ' + err.message);
          });
    }
    ,
    closeDialog() {
      this.dialogVisible = false;
      this.currentUser = {id: null, username: '', name: '', phone: '', user_type: 'user'};
    }
    ,
  },
};
</script>

<style scoped>
.user-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
