<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <div style="display: flex; align-items: center; gap: 20px;">
        <el-input
            v-model="searchQuery"
            placeholder="请输入材料名称进行检索"
            style="width: 300px;"
            @input="searchMaterials"
        ></el-input>
        <el-select v-model="warehouseType" placeholder="选择仓库类型" @change="fetchMaterials">
          <el-option label="事务所仓库" value="事务所仓库"></el-option>
          <el-option label="工厂消耗品仓库" value="工厂消耗品仓库"></el-option>
        </el-select>
      </div>
    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table
          :data="filteredMaterials"
          style="width: 100%; flex: 1;"
          border
          stripe>
        <el-table-column prop="Material_info.id" label="Material_info"></el-table-column>

        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="Material_info.specifications" label="规格"></el-table-column>
        <el-table-column prop="Material_info.unit" label="单位"></el-table-column>

        <el-table-column prop="monthly_plans.MonthlyPlan_type" label="申请计划"></el-table-column>
        <el-table-column prop="monthly_plans.Material_number" label="月度数量"></el-table-column>
        <el-table-column label="剩余可申请数量" prop="remaining_number"></el-table-column>

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
              placeholder="请输入申请数量"
          ></el-input>
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
      warehouseType: '事务所仓库',
      stockDialogVisible: false,
      stockForm: {
        id: null,
        name: '',
        stockQuantity: 0,
        MonthlyPlan_type: '',
        warehouse_type: '事务所仓库'
      },
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    fetchMaterials() {
      const user_id = localStorage.getItem('user_id');

      this.$axios.get('/user/DayPlan', {
        params: {
          user_id: user_id,
          warehouse_type: this.warehouseType
        }
      })
          .then((res) => {
            this.materials = res.data;
            this.filteredMaterials = res.data;
          })
          .catch((error) => {
            console.error('There was an error fetching the materials:', error);
          });
    },

    searchMaterials() {
      this.filteredMaterials = this.searchQuery
          ? this.materials.filter(material => material.name.includes(this.searchQuery))
          : this.materials;
    },

    openStockDialog(material) {
      this.stockForm = {
        id: material.Material_info.id, // Ensure correct ID is used
        name: material.name,
        stockQuantity: 0,
        MonthlyPlan_type: material.monthly_plans.MonthlyPlan_type,
        warehouse_type: this.warehouseType
      };
      this.stockDialogVisible = true;
    },

    saveStock() {
      const user_id = localStorage.getItem('user_id');

      if (!user_id || !this.stockForm.id) {
        this.$message.error('用户ID或材料ID缺失');
        return;
      }

      this.$axios.post('/user/DayPlan', {
        user_id: user_id,
        id: this.stockForm.id,
        stockQuantity: this.stockForm.stockQuantity,
        MonthlyPlan_type: this.stockForm.MonthlyPlan_type,
        warehouse_type: this.stockForm.warehouse_type
      })
          .then(response => {
            if (response.status === 201) {
              this.$message.success('申请成功');
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
