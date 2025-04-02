<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <el-input
            v-model="searchQuery"
            placeholder="数据综合检索"
            style="width: 300px;"
            @input="searchMaterials"
        ></el-input>
        <div>
          <el-button type="primary" @click="approveAllPending" :disabled="pendingItemsCount === 0">
            一键通过所有未审核 ({{ pendingItemsCount }})
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 统计视图 - 现在作为主要视图 -->
    <el-card class="material-card" style="flex: 1; overflow: auto;">
      <el-tabs v-model="statsTab" @tab-click="handleTabClick">
        <el-tab-pane label="用户申请统计" name="user">
          <div ref="userChart" style="width: 100%; height: 500px;"></div>
          <div class="chart-action-bar">
            <el-button type="primary" @click="showUserDetails" :disabled="!selectedUser">
              查看 {{ selectedUser || '用户' }} 的申请详情
            </el-button>
          </div>
        </el-tab-pane>
        <el-tab-pane label="材料申请统计" name="material">
          <div ref="materialChart" style="width: 100%; height: 500px;"></div>
          <div class="chart-action-bar">
            <el-button type="primary" @click="showMaterialDetails" :disabled="!selectedMaterial">
              查看 {{ selectedMaterial || '材料' }} 的申请详情
            </el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 用户详情弹窗 -->
    <el-dialog 
      :title="`用户 ${selectedUser} 的申请详情`" 
      :visible.sync="userDetailsVisible" 
      width="80%">
      <div v-if="selectedUserApplications.length > 0">
        <div style="margin-bottom: 15px; display: flex; justify-content: space-between;">
          <el-button 
            type="primary" 
            @click="approveUserApplications" 
            :disabled="!hasPendingInUserApps">
            批量通过所有待审核 ({{ pendingInUserAppsCount }})
          </el-button>
          <span>总计: {{ selectedUserApplications.length }} 条记录</span>
        </div>
        <el-table :data="selectedUserApplications" border>
          <el-table-column prop="name" label="材料名称"></el-table-column>
          <el-table-column prop="specifications" label="材料规格"></el-table-column>
          <el-table-column prop="unit" label="材料单位"></el-table-column>
          <el-table-column prop="Material_number" label="申请数量"></el-table-column>
          <el-table-column prop="current_time" label="申请时间"></el-table-column>
          <el-table-column label="状态" width="100">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.auditor === 'False'" type="warning">待审核</el-tag>
              <el-tag v-else type="success">已通过</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button 
                v-if="scope.row.auditor === 'False'" 
                type="primary" 
                size="mini" 
                @click="approveMaterial(scope.row)">
                通过
              </el-button>
              <el-button v-else type="success" size="mini" disabled>已通过</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-document"></i>
        <p>该用户没有申请记录</p>
      </div>
    </el-dialog>

    <!-- 材料详情弹窗 -->
    <el-dialog 
      :title="`材料 ${selectedMaterial} 的申请详情`" 
      :visible.sync="materialDetailsVisible" 
      width="80%">
      <div v-if="selectedMaterialApplications.length > 0">
        <div style="margin-bottom: 15px; display: flex; justify-content: space-between;">
          <el-button 
            type="primary" 
            @click="approveMaterialApplications" 
            :disabled="!hasPendingInMaterialApps">
            批量通过所有待审核 ({{ pendingInMaterialAppsCount }})
          </el-button>
          <span>总计: {{ selectedMaterialApplications.length }} 条记录</span>
        </div>
        <el-table :data="selectedMaterialApplications" border>
          <el-table-column prop="user_name" label="申请用户"></el-table-column>
          <el-table-column prop="specifications" label="材料规格"></el-table-column>
          <el-table-column prop="unit" label="材料单位"></el-table-column>
          <el-table-column prop="Material_number" label="申请数量"></el-table-column>
          <el-table-column prop="current_time" label="申请时间"></el-table-column>
          <el-table-column label="状态" width="100">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.auditor === 'False'" type="warning">待审核</el-tag>
              <el-tag v-else type="success">已通过</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button 
                v-if="scope.row.auditor === 'False'" 
                type="primary" 
                size="mini" 
                @click="approveMaterial(scope.row)">
                通过
              </el-button>
              <el-button v-else type="success" size="mini" disabled>已通过</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="empty-data">
        <i class="el-icon-document"></i>
        <p>该材料没有申请记录</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from 'echarts'; // 确保安装了echarts依赖

export default {
  data() {
    return {
      materials: [],
      filteredMaterials: [],
      searchQuery: '',
      userChart: null,
      materialChart: null,
      statsTab: 'user',
      
      // 用户相关
      selectedUser: null,
      userDetailsVisible: false,
      selectedUserApplications: [],
      
      // 材料相关
      selectedMaterial: null,
      materialDetailsVisible: false,
      selectedMaterialApplications: [],
      
      // 当前时间和用户
      currentDate: '2025-03-30 05:20:11',
      currentUser: 'kenny20230303'
    };
  },

  computed: {
    pendingItemsCount() {
      return this.filteredMaterials.filter(item => item.auditor === 'False').length;
    },
    
    // 用户申请相关计算属性
    hasPendingInUserApps() {
      return this.selectedUserApplications.some(item => item.auditor === 'False');
    },
    
    pendingInUserAppsCount() {
      return this.selectedUserApplications.filter(item => item.auditor === 'False').length;
    },
    
    // 材料申请相关计算属性
    hasPendingInMaterialApps() {
      return this.selectedMaterialApplications.some(item => item.auditor === 'False');
    },
    
    pendingInMaterialAppsCount() {
      return this.selectedMaterialApplications.filter(item => item.auditor === 'False').length;
    }
  },

  mounted() {
    this.fetchMaterials();
    
    // 适当地调整窗口大小时重新渲染图表
    window.addEventListener('resize', this.handleResize);
  },
  
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    
    // 清理图表实例
    if (this.userChart) {
      this.userChart.dispose();
    }
    if (this.materialChart) {
      this.materialChart.dispose();
    }
  },

  watch: {
    statsTab() {
      this.$nextTick(() => {
        this.initCharts();
      });
    },
  },

  methods: {
    handleResize() {
      if (this.userChart) {
        this.userChart.resize();
      }
      if (this.materialChart) {
        this.materialChart.resize();
      }
    },
    
    fetchMaterials() {
      const user_id = localStorage.getItem('user_id');
      this.$axios.post('/auditor/getDayPlan', { user_id })
          .then((res) => {
            this.materials = res.data;
            this.filteredMaterials = res.data;
            
            this.$nextTick(() => {
              this.initCharts();
            });
          })
          .catch(error => {
            console.error('获取数据失败:', error);
            this.$message.error('获取数据失败，请重试');
          });
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
      
      this.$nextTick(() => {
        this.initCharts();
      });
    },
    
    handleTabClick() {
      // 切换标签时，重置选中的项
      this.selectedUser = null;
      this.selectedMaterial = null;
    },
    
    // 一键通过所有未审核
    approveAllPending() {
      const pendingItems = this.filteredMaterials.filter(item => item.auditor === 'False');
      
      if (pendingItems.length === 0) {
        this.$message.info('没有可批准的记录');
        return;
      }
      
      this.$confirm(`确定要一键通过所有 ${pendingItems.length} 条未审核记录吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 显示加载中提示
        const loading = this.$loading({
          lock: true,
          text: '正在批量处理...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        
        const promises = pendingItems.map(item => {
          return this.$axios.put('/auditor/getDayPlan', { 
            id: item.id, 
            number: item.Material_number 
          });
        });
        
        Promise.all(promises)
          .then(() => {
            loading.close(); // 关闭加载提示
            pendingItems.forEach(item => item.auditor = 'True');
            this.$message.success(`成功批准 ${pendingItems.length} 条记录`);
            this.initCharts(); // 刷新图表
          })
          .catch(error => {
            loading.close(); // 关闭加载提示
            console.error(error);
            this.$message.error('批量处理时发生错误');
          });
      }).catch(() => {
        this.$message.info('已取消操作');
      });
    },

    // 通过单个申请
    approveMaterial(row) {
      this.$axios.put('/auditor/getDayPlan', { id: row.id, number: row.Material_number })
          .then(() => {
            row.auditor = 'True';
            this.$message.success('材料已通过');
            
            // 更新相关数据和图表
            if (this.userDetailsVisible) {
              this.updateUserApplications();
            }
            if (this.materialDetailsVisible) {
              this.updateMaterialApplications();
            }
            
            this.initCharts(); // 刷新图表
          })
          .catch((error) => {
            console.error(error);
            this.$message.error('更新失败');
          });
    },
    
    // 显示用户详情
    showUserDetails() {
      if (!this.selectedUser) {
        this.$message.info('请先在图表中选择一个用户');
        return;
      }
      
      this.selectedUserApplications = this.materials.filter(item => 
        item.user_name === this.selectedUser
      );
      
      this.userDetailsVisible = true;
    },
    
    // 批量通过用户申请
    approveUserApplications() {
      const pendingItems = this.selectedUserApplications.filter(item => item.auditor === 'False');
      
      if (pendingItems.length === 0) {
        this.$message.info('没有可批准的记录');
        return;
      }
      
      this.$confirm(`确定要批量通过 ${pendingItems.length} 条记录吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const loading = this.$loading({
          lock: true,
          text: '正在批量处理...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        
        const promises = pendingItems.map(item => {
          return this.$axios.put('/auditor/getDayPlan', { 
            id: item.id, 
            number: item.Material_number 
          });
        });
        
        Promise.all(promises)
          .then(() => {
            loading.close();
            pendingItems.forEach(item => item.auditor = 'True');
            this.$message.success(`成功批准 ${pendingItems.length} 条记录`);
            this.updateUserApplications();
            this.initCharts(); // 刷新图表
          })
          .catch(error => {
            loading.close();
            console.error(error);
            this.$message.error('批量处理时发生错误');
          });
      }).catch(() => {
        this.$message.info('已取消操作');
      });
    },
    
    // 更新用户申请列表
    updateUserApplications() {
      if (!this.selectedUser) return;
      
      this.selectedUserApplications = this.materials.filter(item => 
        item.user_name === this.selectedUser
      );
    },
    
    // 显示材料详情
    showMaterialDetails() {
      if (!this.selectedMaterial) {
        this.$message.info('请先在图表中选择一个材料');
        return;
      }
      
      this.selectedMaterialApplications = this.materials.filter(item => 
        item.name === this.selectedMaterial
      );
      
      this.materialDetailsVisible = true;
    },
    
    // 批量通过材料申请
    approveMaterialApplications() {
      const pendingItems = this.selectedMaterialApplications.filter(item => item.auditor === 'False');
      
      if (pendingItems.length === 0) {
        this.$message.info('没有可批准的记录');
        return;
      }
      
      this.$confirm(`确定要批量通过 ${pendingItems.length} 条记录吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const loading = this.$loading({
          lock: true,
          text: '正在批量处理...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        
        const promises = pendingItems.map(item => {
          return this.$axios.put('/auditor/getDayPlan', { 
            id: item.id, 
            number: item.Material_number 
          });
        });
        
        Promise.all(promises)
          .then(() => {
            loading.close();
            pendingItems.forEach(item => item.auditor = 'True');
            this.$message.success(`成功批准 ${pendingItems.length} 条记录`);
            this.updateMaterialApplications();
            this.initCharts(); // 刷新图表
          })
          .catch(error => {
            loading.close();
            console.error(error);
            this.$message.error('批量处理时发生错误');
          });
      }).catch(() => {
        this.$message.info('已取消操作');
      });
    },
    
    // 更新材料申请列表
    updateMaterialApplications() {
      if (!this.selectedMaterial) return;
      
      this.selectedMaterialApplications = this.materials.filter(item => 
        item.name === this.selectedMaterial
      );
    },

    // 初始化图表
    initCharts() {
      if (this.statsTab === 'user') {
        this.initUserChart();
      } else if (this.statsTab === 'material') {
        this.initMaterialChart();
      }
    },
    
    // 初始化用户统计图表
    initUserChart() {
      // 清除旧的点击事件处理程序
      if (this.userChart) {
        this.userChart.off('click');
        this.userChart.dispose();
      }
      
      // 按用户统计
      const userStats = {};
      const pendingByUser = {};
      const approvedByUser = {};
      
      this.filteredMaterials.forEach(item => {
        if (!userStats[item.user_name]) {
          userStats[item.user_name] = 0;
          pendingByUser[item.user_name] = 0;
          approvedByUser[item.user_name] = 0;
        }
        userStats[item.user_name]++;
        if (item.auditor === 'False') {
          pendingByUser[item.user_name]++;
        } else {
          approvedByUser[item.user_name]++;
        }
      });

      // 获取用户列表并排序（按申请总数降序）
      const users = Object.keys(userStats).sort((a, b) => userStats[b] - userStats[a]);
      
      this.userChart = echarts.init(this.$refs.userChart);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['待审核', '已通过']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: users,
          axisLabel: {
            fontSize: 12,
            formatter: function(value) {
              // 如果名称太长，则截断并添加省略号
              if (value && value.length > 12) {
                return value.substring(0, 12) + '...';
              }
              return value;
            }
          }
        },
        series: [
          {
            name: '待审核',
            type: 'bar',
            stack: 'total',
            itemStyle: {
              color: '#E6A23C'
            },
            data: users.map(user => pendingByUser[user]),
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true,
              position: 'inside'
            }
          },
          {
            name: '已通过',
            type: 'bar',
            stack: 'total',
            itemStyle: {
              color: '#67C23A'
            },
            data: users.map(user => approvedByUser[user]),
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true,
              position: 'inside'
            }
          }
        ]
      };
      
      this.userChart.setOption(option);
      
      // 添加点击事件处理
      this.userChart.on('click', (params) => {
        if (params.componentType === 'series') {
          this.selectedUser = params.name;
          this.$message.success(`已选择用户: ${params.name}`);
        }
      });
    },
    
    // 初始化材料统计图表 - 使用饼图
    initMaterialChart() {
      // 清除旧的点击事件处理程序
      if (this.materialChart) {
        this.materialChart.off('click');
        this.materialChart.dispose();
      }
      
      // 按材料统计
      const materialStats = {};
      const pendingByMaterial = {};
      const approvedByMaterial = {};
      
      this.filteredMaterials.forEach(item => {
        if (!materialStats[item.name]) {
          materialStats[item.name] = 0;
          pendingByMaterial[item.name] = 0;
          approvedByMaterial[item.name] = 0;
        }
        materialStats[item.name]++;
        if (item.auditor === 'False') {
          pendingByMaterial[item.name]++;
        } else {
          approvedByMaterial[item.name]++;
        }
      });

      // 排序并只保留前10个材料
      const sortedMaterials = Object.entries(materialStats)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
      
      const materialNames = sortedMaterials.map(item => item[0]);
      const materialCounts = sortedMaterials.map(item => item[1]);
      
      this.materialChart = echarts.init(this.$refs.materialChart);
      
      const option = {
        title: {
          text: '申请量最多的前10种材料',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          top: 'center',
          type: 'scroll',
          formatter: (name) => {
            const value = materialStats[name];
            const pending = pendingByMaterial[name];
            return `${name} (总数: ${value}, 待审核: ${pending})`;
          }
        },
        series: [
          {
            name: '申请数量',
            type: 'pie',
            radius: ['35%', '60%'],
            center: ['60%', '50%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              formatter: '{b}: {c} ({d}%)'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            data: materialNames.map((name, index) => ({
              value: materialCounts[index],
              name: name,
              // 根据待审核数量设置不同的颜色
              itemStyle: {
                color: pendingByMaterial[name] > 0 ? '#E6A23C' : '#67C23A'
              }
            }))
          }
        ]
      };
      
      this.materialChart.setOption(option);
      
      // 添加点击事件处理
      this.materialChart.on('click', (params) => {
        if (params.componentType === 'series') {
          this.selectedMaterial = params.name;
          this.$message.success(`已选择材料: ${params.name}`);
        }
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

.chart-action-bar {
  margin-top: 20px;
  text-align: center;
}

.empty-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #909399;
}

.empty-data i {
  font-size: 48px;
  margin-bottom: 10px;
}
</style>