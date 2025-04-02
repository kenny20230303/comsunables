<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <!-- 顶部按钮区域 -->
    <el-card class="supplier-card">
      <el-button type="success" size="medium" @click="dialogVisible = true">新增供应商</el-button>
    </el-card>

    <!-- 表格区域 -->
    <el-card class="supplier-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table
          :data="suppliers"
          style="width: 100%; flex: 1;"
          border
          stripe
      >
        <el-table-column prop="number" label="编号"></el-table-column>
        <el-table-column prop="name" label="联系人"></el-table-column>
        <el-table-column prop="phone" label="电话号码"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="editSupplier(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="deleteSupplier(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 弹窗 -->
    <el-dialog
        :title="currentSupplier.id ? '编辑供应商信息' : '新增供应商'"
        :visible.sync="dialogVisible"
        width="30%"
    >
      <el-form :model="currentSupplier" label-width="80px">
        <el-form-item label="编号">
          <el-input v-model="currentSupplier.number" placeholder="请输入供应商编号"></el-input>
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="currentSupplier.name" placeholder="请输入联系人"></el-input>
        </el-form-item>
        <el-form-item label="电话号码">
          <el-input v-model="currentSupplier.phone" placeholder="请输入电话号码"></el-input>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="currentSupplier.address" placeholder="请输入地址"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSupplier">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      suppliers: [],
      dialogVisible: false,
      currentSupplier: {id: null, number: '', name: '', phone: '', address: ''},
    };
  },

  mounted() {
    this.fetchSuppliers();
  },
  methods: {
    fetchSuppliers() {
      this.$axios.get('/admin/Supplier')
          .then((res) => {
            this.suppliers = res.data;
          });
    },
    editSupplier(supplier) {
      this.currentSupplier = {...supplier};
      this.dialogVisible = true;
    },
    deleteSupplier(supplier) {
      this.$confirm('此操作将永久删除该供应商, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        this.$axios.delete('/admin/Supplier', {data: {id: supplier.id}})
            .then(() => {
              this.$message.success('删除成功');
              this.fetchSuppliers();
            });
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },
    saveSupplier() {
      if (this.currentSupplier.id) {
        this.$axios.put('/admin/Supplier', this.currentSupplier)
            .then(() => {
              this.$message.success('更新成功');
              this.fetchSuppliers();
            })
            .catch(error => {
              // 处理更新失败的情况
              this.$message.error('更新失败: ' + (error.response.data.error || '未知错误'));
            });
      } else {
        this.$axios.post('/admin/Supplier', this.currentSupplier)
            .then(() => {
              this.$message.success('新增成功');
              this.fetchSuppliers();
            })
            .catch(error => {
              // 处理添加失败的情况
              this.$message.error('新增失败: ' + (error.response.data.error || '未知错误'));
            });
      }
      this.dialogVisible = false;
      this.currentSupplier = {id: null, number: '', name: '', phone: '', address: ''};
    }
    ,
  },
};
</script>

<style scoped>
.supplier-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
