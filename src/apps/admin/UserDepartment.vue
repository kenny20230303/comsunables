<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <!-- 顶部按钮区域 -->
    <el-card class="user-type-card">
      <el-button type="success" size="medium" @click="dialogVisible = true">新增部门</el-button>
    </el-card>

    <!-- 表格区域 -->
    <el-card class="user-type-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table
          :data="usertypes"
          style="width: 100%; flex: 1;"
          border
          stripe
      >
        <el-table-column prop="name" label="部门名称"></el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="editUserType(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="deleteUserType(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 弹窗 -->
    <el-dialog
        :title="currentUserType.id ? '编辑部门名称' : '新增部门名称'"
        :visible.sync="dialogVisible"
        width="30%"
    >
      <el-form :model="currentUserType" label-width="50px">
        <el-form-item label="名称">
          <el-input v-model="currentUserType.name" placeholder="请输入部门名称"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUserType">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      usertypes: [],
      dialogVisible: false,
      currentUserType: {id: null, name: ''},
    };
  },

  mounted() {
    this.fetchUserTypes();
  },
  methods: {
    fetchUserTypes() {
      this.$axios.get('/admin/UserDepartment')
          .then((res) => {
            this.usertypes = res.data;
          });
    },
    editUserType(usertype) {
      this.currentUserType = {...usertype};
      this.dialogVisible = true;
    },
    deleteUserType(usertype) {
      this.$confirm('此操作将永久删除该用户类型, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        this.$axios.delete('/admin/UserDepartment', {data: {id: usertype.id}})
            .then(() => {
              this.$message.success('删除成功');
              this.fetchUserTypes();
            });
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },
    saveUserType() {
      if (this.currentUserType.id) {
        this.$axios.put('/admin/UserDepartment', this.currentUserType)
            .then(() => {
              this.$message.success('更新成功');
              this.fetchUserTypes();
            });
      } else {
        this.$axios.post('/admin/UserDepartment', this.currentUserType)
            .then(() => {
              this.$message.success('新增成功');
              this.fetchUserTypes();
            });
      }
      this.dialogVisible = false;
      this.currentUserType = {id: null, name: ''};
    },
  },
};
</script>

<style scoped>
.user-type-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
