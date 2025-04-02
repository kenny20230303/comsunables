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
      <el-table
          :data="paginatedData"
          style="width: 100%; flex: 1;"
          border
          stripe>
        <!--<el-table-column prop="DailyApplication_info.id" label="id"></el-table-column>-->
        <el-table-column prop="DailyApplication_info.name" label="名称"></el-table-column>
        <el-table-column prop="DailyApplication_info.specifications" label="规格"></el-table-column>
        <el-table-column prop="DailyApplication_info.unit" label="单位"></el-table-column>
        <el-table-column prop="Material_number" label="申请数量"></el-table-column>
        <el-table-column prop="current_time" label="申请时间"></el-table-column>

        <el-table-column
            prop="tag"
            label="状态"
            width="120"
            filter-placement="bottom-end">
          <template slot-scope="scope">

            <el-tag v-if="scope.row.type === '已通过'"
                    type="success"
                    disable-transitions>{{ scope.row.type }}
            </el-tag>

            <el-tag v-if="scope.row.type === '未通过'"
                    type="primary"
                    disable-transitions>{{ scope.row.type }}
            </el-tag>


          </template>
        </el-table-column>
        <el-table-column width="120" label="操作">
          <template slot-scope="scope">
            <el-button
                type="primary"
                @click="openEditDialog(scope.row)"
                :disabled="scope.row.type !== '未通过'">
              修改数量
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredMaterials.length">
        </el-pagination>
      </div>
    </el-card>

    <el-dialog :visible.sync="stockDialogVisible" title="修改数量">
      <el-form :model="stockForm">
        <el-form-item label="数量">
          <el-input v-model="stockForm.stockQuantity" type="number"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="stockDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateQuantity">确 定</el-button>
      </span>
    </el-dialog>


  </div>
</template>

<script>
export default {
  data() {
    return {
      materials: [],
      filteredMaterials: [],
      searchQuery: '',
      stockDialogVisible: false,
      stockForm: {
        id: null,
        name: '',
        stockQuantity: 0
      },
      currentPage: 1,
      pageSize: 10,
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  computed: {
    paginatedData() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.filteredMaterials.slice(startIndex, endIndex);
    }
  },

  methods: {
    searchMaterials() {
      const query = this.searchQuery.toLowerCase();
      this.filteredMaterials = this.materials.filter(material => {
        return Object.values(material).some(value =>
            String(value).toLowerCase().includes(query)
        );
      });
      this.currentPage = 1; // 搜索后重置为第一页
    },
    fetchMaterials() {
      const user_id = localStorage.getItem('user_id');
      this.$axios.post('/user/DayPlanHistory', {
        user_id: user_id,
        get_all: true // 添加参数，获取所有申请记录
      })
          .then((res) => {
            // 按日期降序排序，确保最近日期优先显示
            const sortedData = res.data.sort((a, b) => {
              return new Date(b.current_time) - new Date(a.current_time);
            });
            this.materials = sortedData;
            this.filteredMaterials = sortedData;
            this.currentPage = 1; // 重置为第一页
          });
    },

    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1; // 页大小改变后重置为第一页
    },
    
    handleCurrentChange(val) {
      this.currentPage = val;
    },

    openEditDialog(material) {
      console.log(material)
      this.stockForm.id = material.DailyApplication_info.id; // 假设每个材料项都有一个唯一的 id
      this.stockForm.stockQuantity = material.Material_number; // 设置当前数量
      this.stockDialogVisible = true; // 打开对话框
    },

    updateQuantity() {
      console.log(this.stockForm.stockQuantity)
      const user_id = localStorage.getItem('user_id');
      this.$axios.put('/user/DayPlan', {
        user_id: user_id,
        material_id: this.stockForm.id,
        new_quantity: this.stockForm.stockQuantity
      })
          .then((res) => {
            console.log(res);
            this.stockDialogVisible = false;
            this.fetchMaterials(); // 刷新材料列表
          })
          .catch((error) => {
            console.error(error); // 打印整个错误对象
            this.$message.error('数据异常超出');
          });
    }
  },
};
</script>

<style scoped>
.material-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination-container {
  margin-top: 15px;
  display: flex;
  justify-content: center;
}
</style>
