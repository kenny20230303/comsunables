<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <el-input
          v-model="searchQuery"
          placeholder="请输入材料名称进行检索"
          style="width: 300px;"
          @input="searchMaterials"
      ></el-input>
    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table
          :data="filteredMaterials"
          style="width: 100%; flex: 1;"
          border
          stripe>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="specifications" label="规格"></el-table-column>
        <el-table-column prop="unit" label="单位"></el-table-column>

        <el-table-column label="操作" width="80">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="openStockDialog(scope.row)">申请</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
        title="申请材料"
        :visible.sync="stockDialogVisible"
        width="30%"
    >
      <el-form :model="stockForm" label-width="100px">
        <el-form-item label="材料名称">
          <el-input v-model="stockForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="申请数量">
          <el-input
              type="number"
              v-model="stockForm.stockQuantity"
              placeholder="请输入入库数量"
          ></el-input>
        </el-form-item>
        <el-form-item label="纳期">
          <el-input v-model="stockForm.naqi"></el-input>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="stockForm.beizhu"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="stockDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveStock">确认申请</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      materials: [],
      filteredMaterials: [],
      searchQuery: '',
      stockDialogVisible: false,
      stockForm: {
        id: null,
        name: '',
        stockQuantity: 0,
        naqi: '',
        beizhu: '',
      },
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    fetchMaterials() {
      this.$axios.get('/user/MonthlyPlanOuter')
          .then((res) => {
            this.materials = res.data;
            this.filteredMaterials = res.data;
          });
    },

    searchMaterials() {
      this.filteredMaterials = this.searchQuery
          ? this.materials.filter(material => material.name.includes(this.searchQuery))
          : this.materials;
    },

    openStockDialog(material) {
      this.stockForm = {
        id: material.id,
        name: material.name,
        stockQuantity: 0
      };
      this.stockDialogVisible = true;
    },

    saveStock() {
      const user_id = localStorage.getItem('user_id');

      if (!user_id || !this.stockForm.id) {
        this.$message.error('用户ID或材料ID缺失');
        return;
      }

      this.$axios.post('/user/MonthlyPlanOuter', {
        user_id: user_id,
        id: this.stockForm.id,
        stockQuantity: this.stockForm.stockQuantity,
        naqi: this.stockForm.naqi,
        beizhu: this.stockForm.beizhu,
      })
          .then(response => {
            if (response.status === 201) {
              this.$message.success('成功');
              this.fetchMaterials();
              this.stockDialogVisible = false;
            }
          })
          .catch(error => {
            if (error.response) {
              const errorMessage = error.response.data.error || '发生未知错误';
              this.$message.error(errorMessage);
            } else if (error.request) {
              this.$message.error('服务器无响应，请稍后重试');
            } else {
              this.$message.error('请求失败，请检查网络连接');
            }
          });
    }
  },
};
</script>

<style scoped>
.material-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
