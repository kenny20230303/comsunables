<template>
  <div style="display: flex; flex-direction: column; height: 100vh;">
    <el-card class="material-card">
      <el-button type="success" size="medium" @click="dialogVisible = true">新增材料</el-button>
    </el-card>

    <el-card class="material-card" style="flex: 1; display: flex; flex-direction: column; overflow: auto;">
      <el-table
          :data="materials"
          style="width: 100%; flex: 1;"
          border
          stripe>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="specifications" label="规格"></el-table-column>
        <el-table-column prop="unit" label="单位"></el-table-column>
        <el-table-column prop="price" label="单价"></el-table-column>
        <el-table-column prop="secure_days" label="安全在库天数"></el-table-column>
        <el-table-column prop="secure_number" label="安全在库数量"></el-table-column>

        <!-- 新增供应商编号列 -->
        <el-table-column label="供应商编号" width="150">
          <template slot-scope="scope">
            <span>{{ getSupplierNumber(scope.row.Supplier_id) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="250">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="editMaterial(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="deleteMaterial(scope.row)">删除</el-button>
            <el-button type="info" size="mini" @click="viewSupplier(scope.row)">查看供应商</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
        :title="currentMaterial.id ? '编辑材料' : '新增材料'"
        :visible.sync="dialogVisible"
        width="30%"
    >
      <el-form :model="currentMaterial" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="currentMaterial.name" placeholder="请输入材料名称"></el-input>
        </el-form-item>
        <el-form-item label="规格">
          <el-input v-model="currentMaterial.specifications" placeholder="请输入规格"></el-input>
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="currentMaterial.unit" placeholder="请输入单位"></el-input>
        </el-form-item>
        <el-form-item label="单价">
          <el-input v-model="currentMaterial.price" placeholder="请输入单价"></el-input>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="currentMaterial.Supplier_id" placeholder="选择供应商">
            <el-option
                v-for="supplier in suppliers"
                :key="supplier.id"
                :label="supplier.number"
                :value="supplier.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="安全在库天数">
          <el-input
              type="number"
              v-model="currentMaterial.secure_days"
              placeholder="请输入安全在库天数"
              @input="handleInput('secure_days')"
          ></el-input>
        </el-form-item>
        <el-form-item label="安全在库数量">
          <el-input
              type="number"
              v-model="currentMaterial.secure_number"
              placeholder="请输入安全在库数量"
              @input="handleInput('secure_number')"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取消</el-button>
    <el-button type="primary" @click="saveMaterial">保存</el-button>
  </span>
    </el-dialog>

    <el-dialog
        title="供应商信息"
        :visible.sync="supplierDialogVisible"
        width="30%"
    >
      <el-form :model="currentSupplier" label-width="100px">
        <el-form-item label="编号">
          <el-input v-model="currentSupplier.number" disabled></el-input>
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="currentSupplier.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="电话号码">
          <el-input v-model="currentSupplier.phone" disabled></el-input>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="currentSupplier.address" disabled></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="supplierDialogVisible = false">关闭</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      materials: [],
      suppliers: [], // 用于存储供应商列表
      dialogVisible: false,
      supplierDialogVisible: false, // 控制供应商信息对话框的显示
      currentMaterial: {
        id: null,
        name: '',
        specifications: '',
        unit: '',
        price: '',
        Supplier_id: '',
        secure_days: '',
        secure_number: ''
      },
      currentSupplier: {
        number: '',
        name: '',
        phone: '',
        address: ''
      },
    };
  },

  mounted() {
    this.fetchMaterials();
    this.fetchSuppliers(); // 获取供应商列表
  },

  methods: {
    fetchMaterials() {
      this.$axios.get('/admin/Material')
          .then((res) => {
            this.materials = res.data;
          });
    },

    fetchSuppliers() {
      this.$axios.get('/admin/Supplier')
          .then((res) => {
            this.suppliers = res.data;
            console.log(res.data);
          });
    },

    editMaterial(material) {
      this.currentMaterial = {...material};
      this.dialogVisible = true;
    },

    deleteMaterial(material) {
      this.$confirm('此操作将永久删除该材料, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        this.$axios.delete('/admin/Material', {data: {id: material.id}})
            .then(() => {
              this.$message.success('删除成功');
              this.fetchMaterials();
            });
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },

    saveMaterial() {
      if (this.currentMaterial.id) {
        this.$axios.put('/admin/Material', this.currentMaterial)
            .then(() => {
              this.$message.success('更新成功');
              this.fetchMaterials();
            });
      } else {
        this.$axios.post('/admin/Material', this.currentMaterial)
            .then(() => {
              this.$message.success('新增成功');
              this.fetchMaterials();
            });
      }
      this.dialogVisible = false;
      this.currentMaterial = {
        id: null,
        name: '',
        specifications: '',
        unit: '',
        price: '',
        Supplier_id: '',
        secure_days: '',
        secure_number: ''
      };
    },

    viewSupplier(material) {
      const supplierId = material.Supplier_id;
      const supplier = this.suppliers.find(s => String(s.id) === String(supplierId)); // 进行类型转换

      if (supplier) {
        this.currentSupplier = {...supplier};
        this.supplierDialogVisible = true;
      } else {
        this.$message.warning('未找到供应商信息');
      }
    },

    getSupplierNumber(supplierId) {
      const supplier = this.suppliers.find(s => String(s.id) === String(supplierId));
      return supplier ? supplier.number : '未找到';
    }
  },
};
</script>

<style scoped>
.material-card {
  margin: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
