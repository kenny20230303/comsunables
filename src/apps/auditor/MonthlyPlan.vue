<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 20px;">
          <el-input
              v-model="searchQuery"
              placeholder="数据综合检索"
              style="width: 300px;"
              @input="searchMaterials"
          ></el-input>
          <el-date-picker
              v-model="selectedMonth"
              type="month"
              placeholder="选择月份"
              format="yyyy年MM月"
              value-format="yyyy-MM"
              @change="changeMonth"
          ></el-date-picker>
        </div>
        <div class="total-amount">
          <span>当月材料申请总金额: {{ totalAmount }} 元</span>
        </div>
      </div>
    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table :data="filteredMaterials" border stripe>
        <el-table-column prop="name" label="材料名称"></el-table-column>
        <el-table-column prop="specifications" label="材料规格"></el-table-column>
        <el-table-column prop="unit" label="材料单位"></el-table-column>
        <el-table-column prop="user_name" label="用户姓名"></el-table-column>

        <el-table-column label="申请数量" width="150">
          <template slot-scope="scope">
            <div style="display: flex; align-items: center; justify-content: flex-start;">
              <div style="width: 20px; margin-right: 8px; text-align: center;">
                <div style="color: red; font-size: 20px; line-height: 1;" v-if="scope.row.number_change === 'True'">*</div>
              </div>
              <div style="flex-grow: 1;">
                <el-input
                    type="number"
                    v-model="scope.row.Material_number"
                    size="mini"
                    style="width: 100%;"
                ></el-input>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="current_time" label="申请时间"></el-table-column>

        <el-table-column label="操作" width="100">
          <template slot-scope="scope">
            <el-button v-if="scope.row.auditor === 'False'" type="primary" size="mini" @click="approveMaterial(scope.row)">未通过</el-button>
            <el-button v-if="scope.row.auditor === 'True'" type="success" size="mini">已通过</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      materials: [],
      filteredMaterials: [],
      searchQuery: '',
      selectedMonth: this.getCurrentMonth(), // 初始化为当前月份
      totalAmount: 0
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    getCurrentMonth() {
      const date = new Date();
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      return `${year}-${month}`;
    },

    fetchMaterials() {
      const user_id = localStorage.getItem('user_id');
      this.$axios.post('/auditor/getMonthlyPlan', {
        user_id,
        month: this.selectedMonth // 添加月份参数
      })
          .then((res) => {
            this.materials = res.data.materials || res.data || []; // 兼容可能的API响应结构变化
            this.filteredMaterials = this.materials;
            this.totalAmount = res.data.totalAmount || this.calculateTotalAmount();
          });
    },

    calculateTotalAmount() {
      // 计算总金额 (如果API没有直接返回总金额，可以前端计算)
      // 注意：这是一个示例，实际计算可能需要材料单价等信息
      let total = 0;
      this.materials.forEach(item => {
        if (item.price && item.Material_number) {
          total += parseFloat(item.price) * parseFloat(item.Material_number);
        }
      });
      return total.toFixed(2);
    },

    searchMaterials() {
      const query = this.searchQuery.toLowerCase();
      this.filteredMaterials = this.searchQuery
          ? this.materials.filter(material =>
              Object.values(material).some(value =>
                  String(value).toLowerCase().includes(query)
              )
          )
          : this.materials;
    },

    changeMonth() {
      this.fetchMaterials(); // 月份改变时重新获取数据
    },

    approveMaterial(row) {
      this.$axios.put('/auditor/getMonthlyPlan', {
        id: row.id, 
        number: row.Material_number,
        month: this.selectedMonth // 添加月份参数
      })
          .then((response) => {
            console.log(response);
            row.auditor = 'True';
            this.$message.success('材料已通过');
            // 更新总金额
            this.fetchMaterials();
          })
          .catch((error) => {
            console.log(error);
            this.$message.error('更新失败');
          });
    }
  }
};
</script>

<style scoped>
.material-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.total-amount {
  font-size: 16px;
  font-weight: bold;
  color: #409EFF;
}
</style>