<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <div class="search-container">
        <div class="search-inputs">
          <el-input
              v-model="searchQuery"
              placeholder="数据综合检索"
              style="width: 300px;"
              @input="searchMaterials"
          ></el-input>
          <el-date-picker
              v-model="selectedDate"
              type="month"
              placeholder="选择年月"
              style="margin-left: 20px; width: 200px;"
              @change="filterByDate"
          ></el-date-picker>
        </div>
        <div class="total-amount">
          <span class="out-amount">出库金额: <span class="amount-value-out">￥{{ totalOutAmount }}</span></span>
          <span class="in-amount">入库金额: <span class="amount-value-in">￥{{ totalInAmount }}</span></span>
        </div>
      </div>
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
        <el-table-column prop="price" label="单价"></el-table-column>
        <el-table-column prop="type" label="类型"></el-table-column>
        <el-table-column prop="number" label="数量"></el-table-column>
        <el-table-column label="合计金额">
          <template slot-scope="scope">
            ￥{{ (scope.row.price * scope.row.number).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="current_time" label="时间"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      materials: [], // 原始数据
      filteredMaterials: [], // 用于显示的过滤数据
      searchQuery: '', // 搜索框内容
      selectedDate: '', // 当前选中的年月
      uniqueDates: [], // 唯一的年月列表
      totalOutAmount: 0, // 当月出库金额
      totalInAmount: 0, // 当月入库金额
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    // 获取数据并初始化
    fetchMaterials() {
      this.$axios.get('/admin/MaterialHistory')
          .then((res) => {
            this.materials = res.data; // 保存原始数据
            this.filteredMaterials = res.data; // 初始化过滤数据

            // 提取唯一时间（精确到年月部分）
            const dates = [...new Set(this.materials.map(material => {
              return material.current_time.slice(0, 7); // 提取年月部分（格式为 YYYY-MM）
            }))];

            // 按时间排序（降序）
            this.uniqueDates = dates.sort((a, b) => new Date(b) - new Date(a));

            // 默认选中最新年月
            this.selectedDate = this.uniqueDates[0];

            this.filterByDate();
          });
    },

    // 搜索功能
    searchMaterials() {
      const query = this.searchQuery.toLowerCase();
      const filteredBySearch = this.searchQuery
          ? this.materials.filter(material =>
              Object.values(material).some(value =>
                  String(value).toLowerCase().includes(query)
              )
          )
          : this.materials;

      // 如果有年月选择，继续按照年月过滤
      if (this.selectedDate) {
        const selectedDateString = this.selectedDate;
        this.filteredMaterials = filteredBySearch.filter(material =>
            material.current_time.startsWith(selectedDateString)
        );
      } else {
        this.filteredMaterials = filteredBySearch;
      }

      // 更新出入库金额
      this.calculateTotalAmounts();
    },

    // 根据年月过滤数据
    filterByDate() {
      if (this.selectedDate) {
        const selectedDateString = this.selectedDate instanceof Date
            ? this.selectedDate.getFullYear() + '-' + String(this.selectedDate.getMonth() + 1).padStart(2, '0')
            : this.selectedDate;

        // 按年月过滤数据
        this.filteredMaterials = this.materials.filter(material =>
            material.current_time.startsWith(selectedDateString)
        );
      } else {
        // 如果没有选中年月，显示全部数据
        this.filteredMaterials = this.materials;
      }

      // 如果有搜索条件，继续按搜索条件过滤
      if (this.searchQuery) {
        this.searchMaterials();
      }

      // 更新出入库金额
      this.calculateTotalAmounts();
    },

    // 计算出入库金额
    calculateTotalAmounts() {
      this.totalOutAmount = this.filteredMaterials
          .filter(material => material.type === '出库')
          .reduce((total, material) => total + (material.price * material.number), 0)
          .toFixed(2);

      this.totalInAmount = this.filteredMaterials
          .filter(material => material.type === '入库')
          .reduce((total, material) => total + (material.price * material.number), 0)
          .toFixed(2);
    },
  },
};
</script>

<style scoped>
.material-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.total-amount {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 16px;
  font-weight: bold;
}

.out-amount {
  color: #333;
}

.in-amount {
  color: #333;
  margin-left: 15px;
}

.amount-value-out {
  color: #F56C6C;
  margin-left: 5px;
}

.amount-value-in {
  color: #409EFF;
  margin-left: 5px;
}
</style>
