<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <el-select v-model="value" placeholder="请选择" @change="get_table">
        <el-option
            v-for="item in data"
            :key="item.value"
            :label="item.label"
            :value="item.value">
        </el-option>
      </el-select>

      <el-select style="padding: 0 20px" v-model="selectedTable" placeholder="选择显示的表格">
        <el-option label="日常消费" value="daily"></el-option>
        <el-option label="部门消费" value="department"></el-option>
      </el-select>

      <el-select v-if="selectedTable === 'department'" v-model="selectedDepartment" placeholder="选择部门">
        <el-option
            v-for="department in uniqueDepartments"
            :key="department"
            :label="department"
            :value="department">
        </el-option>
      </el-select>

    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <div v-if="loading">加载中...</div>
      <div v-else>

        <div v-if="selectedTable === 'daily'">
          <el-table :data="formattedDailyConsumption" style="width: 100%; margin-bottom: 20px;">
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="specifications" label="规格"></el-table-column>
            <el-table-column prop="unit_price" label="单价"></el-table-column>
            <el-table-column prop="quantity" label="数量"></el-table-column>
            <el-table-column prop="total_price" label="总价"></el-table-column>
          </el-table>
        </div>

        <div v-if="selectedTable === 'department'">
          <el-table :data="filteredDepartmentConsumption" style="width: 100%;">
            <el-table-column prop="department_name" label="部门名称"></el-table-column>
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="specifications" label="规格"></el-table-column>
            <el-table-column prop="unit_price" label="单价"></el-table-column>
            <el-table-column prop="quantity" label="数量"></el-table-column>
            <el-table-column prop="total_price" label="总价"></el-table-column>
            <el-table-column label="合计" align="right">
              <template v-slot:default="scope">
                <div v-if="scope.$index === filteredDepartmentConsumption.length - 1">
                  <strong style="color: #f56c6c;">{{ totalFilteredDepartmentPrice.toFixed(2) }}</strong>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>

      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: [],
      value: '',
      daily_consumption: [],
      department_consumption: [],
      loading: false,
      error: null,
      selectedTable: 'daily', // 默认选择日常消费
      selectedDepartment: '', // 选择的部门
      uniqueDepartments: [], // 唯一部门列表
    };
  },

  mounted() {
    this.get_infos();
  },
  computed: {
    formattedDailyConsumption() {
      return this.daily_consumption.map(item => ({
        ...item,
        total_price: item.total_price.toFixed(2), // 保留两位小数
      }));
    },
    formattedDepartmentConsumption() {
      return this.department_consumption.map(item => ({
        ...item,
        total_price: item.total_price.toFixed(2), // 保留两位小数
      }));
    },
    filteredDepartmentConsumption() {
      if (this.selectedDepartment) {
        return this.formattedDepartmentConsumption.filter(item => item.department_name === this.selectedDepartment);
      }
      return this.formattedDepartmentConsumption;
    },
    totalFilteredDepartmentPrice() {
      return this.filteredDepartmentConsumption.reduce((total, item) => {
        return total + parseFloat(item.total_price);
      }, 0);
    },
  },

  methods: {
    get_infos() {
      this.loading = true;
      this.$axios.get('/finance/getMonthlyPlanHtml')
          .then(response => {
            this.data = response.data;
            this.value = response.data[0]?.value || ''; // 使用可选链
            this.get_table(); // 直接在这里获取表格数据
          })
          .catch(error => {
            this.error = '获取信息时出错!';
            console.error('There was an error downloading the file!', error);
          })
          .finally(() => {
            this.loading = false;
          });
    },

    get_table() {
      if (!this.value) return; // 如果没有选择值，直接返回

      this.loading = true;
      this.$axios.post('/finance/getMonthlyPlanHtml', {month: this.value})
          .then(response => {
            this.daily_consumption = response.data.daily_consumption;
            this.department_consumption = response.data.department_consumption;
            this.error = null; // 清除之前的错误信息

            // 提取唯一的部门名称
            this.uniqueDepartments = [...new Set(this.department_consumption.map(item => item.department_name))];

            // 默认选择第一个部门
            this.selectedDepartment = this.uniqueDepartments[0] || ''; // 如果有部门，选择第一个
          })
          .catch(error => {
            this.error = '获取消费数据时出错!';
            console.error('There was an error downloading the file!', error);
          })
          .finally(() => {
            this.loading = false;
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

h3 {
  margin: 20px 0 10px;
}
</style>
