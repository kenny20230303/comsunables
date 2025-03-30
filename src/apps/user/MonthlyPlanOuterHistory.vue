<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <el-input
          v-model="searchQuery"
          placeholder="数据综合检索"
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
        <el-table-column prop="number" label="申请数量"></el-table-column>
        <el-table-column prop="current_time" label="申请时间"></el-table-column>

        <el-table-column
            prop="tag"
            label="状态"
            width="120"
            filter-placement="bottom-end">
          <template slot-scope="scope">

            <el-tag v-if="scope.row.type === '已通过'"
                    type="success"
                    disable-transitions>{{ scope.row.type }}
            </el-tag>

            <el-tag v-if="scope.row.type === '未通过'"
                    type="primary"
                    disable-transitions>{{ scope.row.type }}
            </el-tag>


          </template>
        </el-table-column>
        <el-table-column width="120" label="操作">
          <template slot-scope="scope">
            <el-button
                type="primary"
                @click="openEditDialog(scope.row)"
                :disabled="scope.row.type !== '未通过'">
              修改数量
            </el-button>
          </template>
        </el-table-column>


      </el-table>
    </el-card>


    <el-dialog :visible.sync="stockDialogVisible" title="修改数量">
      <el-form :model="stockForm">
        <el-form-item label="数量">
          <el-input v-model="stockForm.stockQuantity" type="number"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="stockDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateQuantity">确 定</el-button>
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
        stockQuantity: 0
      },
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    searchMaterials() {
      const query = this.searchQuery.toLowerCase();
      this.filteredMaterials = this.materials.filter(material => {
        return Object.values(material).some(value =>
            String(value).toLowerCase().includes(query)
        );
      });
    },
    fetchMaterials() {
      const user_id = localStorage.getItem('user_id');
      this.$axios.post('/user/MonthlyPlanOuterHistory', {
        user_id: user_id,
      })
          .then((res) => {
            this.materials = res.data;
            this.filteredMaterials = res.data;
          });
    },
    openEditDialog(material) {
      this.stockForm.id = material.id; // 假设每个材料项都有一个唯一的 id
      this.stockForm.stockQuantity = material.number; // 设置当前数量
      this.stockDialogVisible = true; // 打开对话框
    },
    updateQuantity() {
      const user_id = localStorage.getItem('user_id');
      this.$axios.put('/user/MonthlyPlanOuterHistory', {
        user_id: user_id,
        material_id: this.stockForm.id,
        new_quantity: this.stockForm.stockQuantity
      })
          .then((res) => {
            console.log(res);
            this.stockDialogVisible = false;
            this.fetchMaterials(); // 刷新材料列表
          })
          .catch((error) => {
            console.error('更新数量失败:', error);
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
