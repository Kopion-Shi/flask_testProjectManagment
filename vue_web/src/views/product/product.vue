<template>
  <div class="app-container">
    <el-table
      :data="tableData"
      style="width: 100%"
    >
      <el-table-column prop="id" label="编号" width="180" />
      <el-table-column prop="title" label="名称" width="180" />
      <el-table-column prop="keyCode" label="代号" />
      <el-table-column prop="desc" label="描述" show-overflow-tooltip />
      <el-table-column prop="operator" label="操作人" />
      <el-table-column prop="update" label="操作时间" />
    </el-table>
  </div>
</template>

<script>
import { apiProductList } from '@/api/product'
export default {
  name: 'Product',
  data() {
    return {
      tableData: []
    }
  },
  created() { this.getProductList() },
  methods: {
    getProductList() {
      // 固定格式调用api配置方法，并将返回结果回调给response
      apiProductList().then(response => {
        // console.log（）是调试打印，可以在chrome开发者工具中查看
        console.log(response.data)
        // 将返回的结果赋值给变量 tableData
        this.tableData = response.data
      })
    }
  }
}
</script>
<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>
