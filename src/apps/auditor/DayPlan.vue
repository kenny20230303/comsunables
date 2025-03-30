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
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    fetchMaterials() {
      const user_id = localStorage.getItem('user_id');
      this.$axios.post('/auditor/getDayPlan', { user_id })
          .then((res) => {
            this.materials = res.data;
            this.filteredMaterials = res.data; // Initialize filteredMaterials
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
    },

    approveMaterial(row) {
      this.$axios.put('/auditor/getDayPlan', { id: row.id, number: row.Material_number })
          .then((response) => {
            console.log(response);
            row.auditor = 'True';
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
