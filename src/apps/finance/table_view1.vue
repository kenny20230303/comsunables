<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <div class="filter-container">
        <el-select v-model="value" placeholder="请选择月份" @change="get_table">
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
        
        <el-input 
          v-if="selectedTable === 'department'" 
          v-model="searchKeyword" 
          placeholder="搜索部门名称" 
          prefix-icon="el-icon-search"
          clearable
          @clear="searchKeyword = ''"
          style="width: 200px; margin-left: 20px;"
        ></el-input>
      </div>
    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <div v-if="loading" class="loading-container">
        <el-loading type="primary" text="数据加载中..."></el-loading>
      </div>
      <div v-else-if="error" class="error-container">
        <el-alert :title="error" type="error" show-icon :closable="false"></el-alert>
      </div>
      <div v-else>

        <div v-if="selectedTable === 'daily'">
          <el-table :data="daily_consumption" style="width: 100%; margin-bottom: 20px;">
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="specifications" label="规格"></el-table-column>
            <el-table-column prop="unit_price" label="单价" :formatter="formatPrice"></el-table-column>
            <el-table-column prop="quantity" label="数量"></el-table-column>
            <el-table-column prop="total_price" label="总价" :formatter="formatPrice"></el-table-column>
          </el-table>
        </div>

        <div v-if="selectedTable === 'department'">
          <!-- 添加部门消费汇总 -->
          <div class="department-summary" style="margin-bottom: 20px;">
            <h3>部门消费汇总</h3>
            <div class="chart-container">
              <v-chart class="pie-chart" :option="pieChartOption" autoresize></v-chart>
            </div>
            <!-- 保留表格作为详细数据展示 -->
            <el-table :data="departmentSummary" style="width: 100%; margin-top: 20px;">
              <el-table-column prop="department_name" label="部门名称"></el-table-column>
              <el-table-column prop="total_consumption" label="消费总计" :formatter="formatPrice"></el-table-column>
              <el-table-column label="占比">
                <template slot-scope="scope">
                  <div class="percentage-bar">
                    <div class="percentage-fill" 
                         :style="{width: scope.row.percentage + '%', backgroundColor: getDepartmentColor(scope.row.department_name)}">
                    </div>
                    <span>{{ scope.row.percentage.toFixed(2) }}%</span>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
          
          <el-table 
            :data="filteredDepartmentConsumption" 
            style="width: 100%;"
            border
            stripe
            :default-sort="{prop: 'total_price', order: 'descending'}"
          >
            <el-table-column prop="department_name" label="部门名称" sortable></el-table-column>
            <el-table-column prop="name" label="名称" sortable></el-table-column>
            <el-table-column prop="specifications" label="规格"></el-table-column>
            <el-table-column prop="unit_price" label="单价" :formatter="formatPrice" sortable></el-table-column>
            <el-table-column prop="quantity" label="数量" sortable></el-table-column>
            <el-table-column prop="total_price" label="总价" :formatter="formatPrice" sortable></el-table-column>
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { use } from 'echarts/core';
import { PieChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from 'vue-echarts';

// 注册必要的组件
use([
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  CanvasRenderer
]);

export default {
  components: {
    VChart
  },
  data() {
    return {
      data: [],
      value: '',
      daily_consumption: [],
      department_consumption: [],
      loading: false,
      error: null,
      selectedTable: 'department', // 修改默认值为 'department'（部门消费）
      departmentSummary: [], // 添加部门汇总数据
      pieChartOption: {}, // 饼图配置
      searchKeyword: '', // 搜索关键词
      // 预定义的颜色列表
      colorPalette: [
        '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
        '#36A3F7', '#34BFA3', '#6B7DDF', '#F4516C', '#B37FEB'
      ],
    };
  },
  
  computed: {
    // 过滤后的部门消费数据
    filteredDepartmentConsumption() {
      if (!this.searchKeyword) {
        return this.department_consumption;
      }
      
      const keyword = this.searchKeyword.toLowerCase();
      return this.department_consumption.filter(item => {
        return item.department_name.toLowerCase().includes(keyword) ||
               item.name.toLowerCase().includes(keyword);
      });
    },
  },

  mounted() {
    this.get_infos();
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
            this.calculateDepartmentSummary(); // 计算部门汇总
            this.error = null; // 清除之前的错误信息
          })
          .catch(error => {
            this.error = '获取消费数据时出错!';
            console.error('There was an error downloading the file!', error);
          })
          .finally(() => {
            this.loading = false;
          });
    },
    
    formatPrice(row, column, cellValue) {
      // 如果值为空或不是数字，则返回原值
      if (cellValue === undefined || cellValue === null || isNaN(cellValue)) {
        return cellValue;
      }
      // 将值转换为数字并保留两位小数，添加人民币符号
      return '¥' + Number(cellValue).toFixed(2);
    },
    
    // 计算部门消费汇总
    calculateDepartmentSummary() {
      try {
        // 如果没有部门消费数据，则直接返回
        if (!this.department_consumption || this.department_consumption.length === 0) {
          this.departmentSummary = [];
          this.pieChartOption = {};
          return;
        }
        
        // 使用reduce方法更高效地计算每个部门的总消费
        const departmentMap = this.department_consumption.reduce((acc, item) => {
          const deptName = item.department_name;
          const totalPrice = parseFloat(item.total_price) || 0;
          
          if (!acc[deptName]) {
            acc[deptName] = 0;
          }
          acc[deptName] += totalPrice;
          return acc;
        }, {});
        
        // 转换为数组格式
        const summaryArray = Object.entries(departmentMap).map(([department_name, total_consumption]) => ({
          department_name,
          total_consumption
        }));
        
        // 计算总消费
        const totalConsumption = summaryArray.reduce((sum, dept) => sum + dept.total_consumption, 0);
        
        // 计算每个部门的消费占比
        summaryArray.forEach(dept => {
          dept.percentage = totalConsumption > 0 ? (dept.total_consumption / totalConsumption) * 100 : 0;
        });
        
        // 按消费总额降序排序
        this.departmentSummary = summaryArray.sort((a, b) => b.total_consumption - a.total_consumption);
        
        // 更新饼图数据
        this.updatePieChart();
      } catch (error) {
        console.error('计算部门汇总时出错:', error);
        this.error = '计算部门汇总时出错';
      }
    },
    
    // 更新饼图数据
    updatePieChart() {
      try {
        if (!this.departmentSummary.length) {
          this.pieChartOption = {};
          return;
        }
        
        // 准备饼图数据
        const pieData = this.departmentSummary.map(dept => ({
          name: dept.department_name,
          value: dept.total_consumption,
          percentage: dept.percentage,
          itemStyle: {
            color: this.getDepartmentColor(dept.department_name)
          }
        }));
        
        // 更新饼图配置
        this.pieChartOption = {
          title: {
            text: '部门消费占比',
            left: 'center',
            textStyle: {
              fontSize: 18 // 增大标题字体
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: params => {
              return `${params.name}<br/>消费金额: ¥${Number(params.value).toFixed(2)}<br/>占比: ${params.data.percentage.toFixed(2)}%`;
            }
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            type: 'scroll',
            maxHeight: 250,
            textStyle: {
              fontSize: 16 // 增大图例字体
            }
          },
          series: [
            {
              name: '部门消费',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: true,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: true,
                formatter: '{b}: {d}%',
                fontSize: 16 // 增大饼图标签字体
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 18, // 增大高亮时的字体
                  fontWeight: 'bold'
                },
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              data: pieData
            }
          ]
        };
      } catch (error) {
        console.error('更新饼图数据时出错:', error);
        this.error = '更新饼图数据时出错';
      }
    },
    
    // 获取部门对应的颜色
    getDepartmentColor(departmentName) {
      // 使用预定义的颜色列表
      if (!departmentName) return this.colorPalette[0];
      
      // 使用部门名称的哈希值来确定颜色索引
      const hash = departmentName.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
      return this.colorPalette[hash % this.colorPalette.length];
    }
  }
};
</script>

<style scoped>
.material-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.material-card:hover {
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
}

.filter-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 10px;
}

@media screen and (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-container .el-select,
  .filter-container .el-input {
    margin: 5px 0;
    width: 100%;
  }
}

h3 {
  margin: 20px 0 10px;
  color: #303133;
}

/* 部门颜色设定 */
.department-summary {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.department-summary:hover {
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.1);
}

.department-summary h3 {
  margin: 0 0 20px;
  font-size: 22px;
  font-weight: 600;
  color: #303133;
  text-align: center;
}

.department-summary .el-table .cell {
  font-size: 16px;
}

.chart-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.pie-chart {
  height: 400px;
  width: 100%;
  transition: all 0.3s ease;
}

.percentage-bar {
  position: relative;
  height: 20px;
  background-color: #ebeef5;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.percentage-fill {
  position: absolute;
  height: 100%;
  left: 0;
  top: 0;
  border-radius: 10px;
  transition: width 0.5s ease;
}

.percentage-bar span {
  position: absolute;
  width: 100%;
  text-align: center;
  color: #333;
  font-size: 12px;
  line-height: 20px;
  font-weight: bold;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.7);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.error-container {
  margin: 20px;
}
</style>
