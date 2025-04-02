<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <div style="display: flex; align-items: center; gap: 20px;">
        <el-select 
          v-model="selectedWarehouseType"
          placeholder="选择仓库类型"
          style="width: 180px;"
          @change="fetchMaterials">  <!-- 修改为调用fetchMaterials -->
          <el-option label="全部" value="all"></el-option>
          <el-option label="事务所仓库" value="事务所仓库"></el-option>
          <el-option label="工厂消耗品仓库" value="工厂消耗品仓库"></el-option>
        </el-select>
        <el-input
          v-model="searchQuery"
          placeholder="数据综合检索"
          style="width: 300px;"
          @input="searchMaterials"
        ></el-input>

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
                  @change="handleNumberChange(scope.row)"
                ></el-input>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="current_time" label="申请时间"></el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            {{ scope.row.auditor }}
            <el-input
              v-model="scope.row.remark"
              placeholder="输入备注"
              size="mini"
              style="width: 120px; margin-bottom: 5px;"
              v-if="scope.row.finance === 'False'"
            ></el-input>
            <el-button v-if="scope.row.finance === 'False'" type="primary" size="mini" @click="approveMaterial(scope.row)">未出库</el-button>
            <el-button v-if="scope.row.finance === 'True'" type="success" size="mini">已出库</el-button>
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
      selectedWarehouseType: 'all'
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    fetchMaterials() {
      // 添加console.log来调试仓库类型选择
      console.log('当前选择的仓库类型:', this.selectedWarehouseType);
      
      this.$axios.post('/finance/getDayPlan', null, {
        params: {
          warehouse_type: this.selectedWarehouseType !== 'all' ? this.selectedWarehouseType : null
        }
      })
          .then((res) => {
            console.log('获取到的数据:', res.data);
            this.materials = res.data;
            this.filteredMaterials = res.data; // 初始化过滤后的材料列表
            this.searchMaterials(); // 应用筛选
          });
    },

    searchMaterials() {
      const query = this.searchQuery.toLowerCase(); // 转为小写以进行不区分大小写的比较
      console.log('搜索关键词:', query);
      console.log('当前选择的仓库类型:', this.selectedWarehouseType);
      
      // 先按仓库类型筛选
      let filteredByType = this.materials;
      if (this.selectedWarehouseType !== 'all') {
        console.log('按仓库类型筛选前的数据数量:', filteredByType.length);
        filteredByType = this.materials.filter(material => {
          console.log('材料的仓库类型:', material.warehouse_type);
          return material.warehouse_type === this.selectedWarehouseType;
        });
        console.log('按仓库类型筛选后的数据数量:', filteredByType.length);
      }
      
      // 再按搜索关键词筛选
      this.filteredMaterials = this.searchQuery
          ? filteredByType.filter(material => {
            return (
                (material.name && material.name.toLowerCase().includes(query)) ||
                (material.specifications && material.specifications.toLowerCase().includes(query)) ||
                (material.unit && material.unit.toLowerCase().includes(query)) ||
                (material.user_name && material.user_name.toLowerCase().includes(query)) ||
                (material.Material_number && material.Material_number.toString().includes(query)) || // 申请数量
                (material.current_time && material.current_time.toLowerCase().includes(query)) // 申请时间
            );
          })
          : filteredByType; // 如果没有查询，显示按类型筛选后的材料
      
      console.log('最终筛选后的数据数量:', this.filteredMaterials.length);
    },


    approveMaterial(row) {
      this.$axios.put('/finance/getDayPlan', {
        Material_info_id: row.Material_info_id,
        number: row.Material_number,
        DailyApplication_id: row.id,
        remark: row.remark  // 新增备注字段
      })
          .then((response) => {
            console.log(response);
            row.finance = 'True';
            this.$message.success('材料已通过');
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
</style>
