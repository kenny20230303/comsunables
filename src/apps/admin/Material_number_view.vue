<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 15px;">
          <el-select 
            v-model="repositoryType" 
            placeholder="选择仓库类型" 
            style="width: 180px;"
            @change="filterByRepositoryType"
          >
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
        
        <div class="total-amount">
          当前在库金额: <span class="amount-value">{{ getTotalAmount() }}</span>
        </div>
      </div>
    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table
          :data="filteredMaterials"
          style="width: 100%; flex: 1;"
          border
          stripe
          :summary-method="getSummary">
        <el-table-column prop="warehouse_type" label="仓库类型"></el-table-column>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="specifications" label="规格"></el-table-column>
        <el-table-column prop="unit" label="单位"></el-table-column>
        <el-table-column prop="price" label="单价"></el-table-column>
        <el-table-column prop="secure_days" label="安全在库天数"></el-table-column>
        <el-table-column prop="secure_number" label="安全在库数量"></el-table-column>
        <el-table-column prop="number" label="当前库存数量"></el-table-column>
        <el-table-column label="金额" :formatter="formatAmount"></el-table-column>

        <el-table-column label="操作" width="80">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="openStockDialog(scope.row)">入库</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
        title="入库材料"
        :visible.sync="stockDialogVisible"
        width="30%"
    >
      <el-form :model="stockForm" label-width="100px">
        <el-form-item label="材料名称">
          <el-input v-model="stockForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="仓库类型">
          <el-input v-model="stockForm.warehouse_type" disabled></el-input>
        </el-form-item>
        <el-form-item label="入库数量">
          <el-input
              type="number"
              v-model="stockForm.stockQuantity"
              placeholder="请输入入库数量"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="stockDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveStock">确认入库</el-button>
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
      repositoryType: 'all', // 默认显示全部仓库类型
      stockDialogVisible: false,
      stockForm: {
        id: null,
        name: '',
        warehouse_type: '',
        stockQuantity: 0
      },
    };
  },

  mounted() {
    this.fetchMaterials();
  },

  methods: {
    fetchMaterials() {
      this.$axios.get('/admin/Material')
          .then((res) => {
            this.materials = res.data;
            this.filterMaterials();
          });
    },

    filterMaterials() {
      // 首先按仓库类型筛选
      let result = [...this.materials];
      
      if (this.repositoryType !== 'all') {
        result = this.materials.filter(material => 
          material.warehouse_type === this.repositoryType
        );
      }
      
      // 再按搜索条件筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(material => {
          const name = material.name ? material.name.toLowerCase() : '';
          const specifications = material.specifications ? material.specifications.toLowerCase() : '';
          const unit = material.unit ? material.unit.toLowerCase() : '';
          const price = material.price ? material.price.toString() : '';
          const secure_days = material.secure_days ? material.secure_days.toString() : '';
          const secure_number = material.secure_number ? material.secure_number.toString() : '';
          const number = material.number ? material.number.toString() : '';

          return name.includes(query) ||
              specifications.includes(query) ||
              unit.includes(query) ||
              price.includes(query) ||
              secure_days.includes(query) ||
              secure_number.includes(query) ||
              number.includes(query);
        });
      }
      
      this.filteredMaterials = result;
    },

    searchMaterials() {
      this.filterMaterials();
    },

    filterByRepositoryType() {
      this.filterMaterials();
    },

    formatAmount(row) {
      return '￥' + (row.price * row.number).toFixed(2);
    },

    getTotalAmount() {
      return '￥' + this.filteredMaterials.reduce((total, material) => {
        return total + (material.price * material.number);
      }, 0).toFixed(2);
    },

    openStockDialog(material) {
      this.stockForm = {
        id: material.id,
        name: material.name,
        warehouse_type: material.warehouse_type,
        stockQuantity: 0
      };
      this.stockDialogVisible = true;
    },

    saveStock() {
      this.$axios.post('/admin/Material/stock', {
        id: this.stockForm.id,
        warehouse_type: this.stockForm.warehouse_type,
        stockQuantity: this.stockForm.stockQuantity
      })
          .then(() => {
            this.$message.success('成功');
            this.fetchMaterials();
            this.stockDialogVisible = false;
          });
    },
  },
};
</script>

<style scoped>
.material-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.total-amount {
  font-size: 16px;
  font-weight: bold;
}

.amount-value {
  color: #409EFF;
  margin-left: 5px;
}
</style>
