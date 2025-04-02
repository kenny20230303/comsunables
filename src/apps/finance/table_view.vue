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

    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <div v-if="loading">加载中...</div>
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
                  <span>{{ scope.row.percentage.toFixed(2) }}%</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
          
          <el-table :data="department_consumption" style="width: 100%;">
            <el-table-column prop="department_name" label="部门名称"></el-table-column>
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="specifications" label="规格"></el-table-column>
            <el-table-column prop="unit_price" label="单价" :formatter="formatPrice"></el-table-column>
            <el-table-column prop="quantity" label="数量"></el-table-column>
            <el-table-column prop="total_price" label="总价" :formatter="formatPrice"></el-table-column>
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
    };
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
      // 创建一个Map来存储每个部门的总消费
      const departmentMap = new Map();
      
      // 计算每个部门的总消费
      this.department_consumption.forEach(item => {
        const deptName = item.department_name;
        const totalPrice = parseFloat(item.total_price) || 0;
        
        if (departmentMap.has(deptName)) {
          departmentMap.set(deptName, departmentMap.get(deptName) + totalPrice);
        } else {
          departmentMap.set(deptName, totalPrice);
        }
      });
      
      // 转换为数组格式
      const summaryArray = Array.from(departmentMap, ([department_name, total_consumption]) => ({
        department_name,
        total_consumption
      }));
      
      // 计算总消费
      const totalConsumption = summaryArray.reduce((sum, dept) => sum + dept.total_consumption, 0);
      
      // 计算每个部门的消费占比
      summaryArray.forEach(dept => {
        dept.percentage = (dept.total_consumption / totalConsumption) * 100;
      });
      
      // 按消费总额降序排序
      this.departmentSummary = summaryArray.sort((a, b) => b.total_consumption - a.total_consumption);
      
      // 更新饼图数据
      this.updatePieChart();
    },
    
    // 更新饼图数据
    updatePieChart() {
      if (!this.departmentSummary.length) return;
      
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
    },
    
    // 获取部门对应的颜色
    getDepartmentColor(departmentName) {
      // 预定义的颜色列表
      const colors = [
        '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
        '#36A3F7', '#34BFA3', '#6B7DDF', '#F4516C', '#B37FEB'
      ];
      
      // 使用部门名称的哈希值来确定颜色索引
      const hash = departmentName.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
      return colors[hash % colors.length];
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
/* 部门颜色设定 */
.department-summary {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.department-summary h3 {
  margin: 20px 0 10px;
  font-size: 20px; /* 增大标题字体 */
}

.department-summary .el-table .cell {
  font-size: 16px; /* 增大表格内部门名称字体 */
}

.chart-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.pie-chart {
  height: 400px;
  width: 100%;
}

.percentage-bar {
  position: relative;
  height: 20px;
  background-color: #ebeef5;
  border-radius: 10px;
  overflow: hidden;
}

.percentage-fill {
  position: absolute;
  height: 100%;
  left: 0;
  top: 0;
  border-radius: 10px;
}

.percentage-bar span {
  position: absolute;
  width: 100%;
  text-align: center;
  color: #333;
  font-size: 12px;
  line-height: 20px;
}
</style>
