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
      <el-table :data="filteredMaterials" border stripe>
        <el-table-column prop="Material_info_id" label="Material_info_id.id"></el-table-column>
        <el-table-column prop="department" label="所在部门"></el-table-column>
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
                <a>{{ scope.row.Material_number }}</a>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="current_time" label="申请时间"></el-table-column>
        <el-table-column label="操作" width="100">
          <template slot-scope="scope">
            {{ scope.row.auditor }}
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
      searchQuery: ''
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    fetchMaterials() {
      this.$axios.post('/finance/getDayPlan')
          .then((res) => {
            this.materials = res.data;
            this.filteredMaterials = res.data; // 初始化过滤后的材料列表
          });
    },

    searchMaterials() {
      const query = this.searchQuery.toLowerCase(); // 转为小写以进行不区分大小写的比较
      this.filteredMaterials = this.searchQuery
          ? this.materials.filter(material => {
            return (
                (material.name && material.name.toLowerCase().includes(query)) ||
                (material.specifications && material.specifications.toLowerCase().includes(query)) ||
                (material.unit && material.unit.toLowerCase().includes(query)) ||
                (material.user_name && material.user_name.toLowerCase().includes(query)) ||
                (material.Material_number && material.Material_number.toString().includes(query)) || // 申请数量
                (material.current_time && material.current_time.toLowerCase().includes(query)) // 申请时间
            );
          })
          : this.materials; // 如果没有查询，显示所有材料
    },


    approveMaterial(row) {
      this.$axios.put('/finance/getDayPlan', {Material_info_id: row.Material_info_id, number: row.Material_number, DailyApplication_id: row.id})
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
