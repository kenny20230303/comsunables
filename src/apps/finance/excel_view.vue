<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <el-input
          style="width: 200px"
          type="success"
          size="medium"
          v-model="searchQuery"
          placeholder="数据综合检索"
      ></el-input>
    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table :data="filteredData" style="width: 100%">
        <el-table-column prop="value" label="日期"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="downloadExcel(scope.row.value)">下载</el-button>
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
      data: [],
      searchQuery: '' // 搜索关键字
    };
  },

  mounted() {
    this.getdownloadExcel();
  },
  computed: {
    filteredData() {
      // 根据搜索关键字过滤数据
      return this.data.filter(item => {
        return item.value.includes(this.searchQuery); // 假设要搜索的字段是 value
      });
    }
  },
  methods: {
    getdownloadExcel() {
      this.$axios.get('/finance/getMonthlyPlanEchars')
          .then(response => {
            this.data = response.data;
          })
          .catch(error => {
            console.error('There was an error downloading the file!', error);
          });
    },
    downloadExcel(value) {
      this.$axios.post('/finance/getMonthlyPlanEchars', { value: value }, { responseType: 'blob' })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `material_information_${new Date().toISOString().slice(0, 7)}.xlsx`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          })
          .catch(error => {
            console.error('There was an error downloading the file!', error);
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
