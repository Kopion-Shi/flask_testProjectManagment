<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="名称">
          <el-input v-model="search.title" placeholder="支持模糊查询" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="search.keyCode" placeholder="支持模糊查询" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchProduct()">查询</el-button>
        </el-form-item>
      </el-form>
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="dialogProduct()">新增</el-button>
    </div>
    <el-table
      :data="tableData"
      style="width: 100%"
    >
      <el-table-column prop="id" label="编号" width="180" />
      <el-table-column prop="title" label="名称" width="180" />
      <el-table-column prop="keyCode" label="代号" />
      <el-table-column prop="desc" label="描述" show-overflow-tooltip />
      <el-table-column prop="operator" label="操作人" />
      <el-table-column :formatter="formatDate" prop="update" label="操作时间" />
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="dialogProductUpdate(scope.row)">编辑</el-link>
          <el-link icon="el-icon-delete" @click="pSoftRemove(scope.row.id)">停用</el-link>
          <el-link icon="el-icon-delete" @click="pHardRemove(scope.row.id)">删除</el-link>
        </template>
      </el-table-column>

    </el-table>

    <!--对话框嵌套表，使用el-dialog-->
    <el-dialog :title="dialogProductStatus==='ADD'?'添加产品或项目':'修改产品或项目'" :visible.sync="dialogProductShow">
      <el-form :model="product">
        <el-form-item v-if="dialogProductStatus==='UPDATE'" label="编号" label-width="100px">
          <el-input v-model="product.id" placeholder="项目ID" disabled style="width: 80%" />
        </el-form-item>
        <el-form-item label="名称" label-width="100px">
          <el-input v-model="product.title" placeholder="请填写中文名称" style="width: 80%" />
        </el-form-item>
        <el-form-item label="唯一码" label-width="100px">
          <el-input v-model="product.keyCode" placeholder="产品/项目唯一码" style="width: 80%" />
        </el-form-item>
        <el-form-item label="备注" label-width="100px">
          <el-input v-model="product.desc" type="textarea" placeholder="备注说明" style="width: 80%" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogProductShow = false">取 消</el-button>
        <el-button v-if="dialogProductStatus === 'ADD'" type="primary" @click="pCreate()">添加</el-button>
        <el-button v-if="dialogProductStatus === 'UPDATE'" type="primary" @click="pUpdate()">更新</el-button>

      </span>
    </el-dialog>
  </div>
</template>

<script>

import moment from 'moment'
import {
  apiProductCreate,
  apiProductUpdate,
  apiProductDelete,
  apiProductRemove,
  apiProductSearch
} from '@/api/product'
import store from '@/store'

export default {
  name: 'Product',
  data() {
    return {
      op_user: store.getters.name,
      // 定义产品参数
      product: {
        id: undefined,
        title: undefined,
        keyCode: undefined,
        desc: undefined,
        operator: this.op_user
      },
      // 控制嵌套表单显示和隐藏
      dialogProductShow: false,
      dialogProductStatus: '',
      // 展示products_list
      tableData: [],
      // 搜索条件
      search: {
        title: undefined,
        keyCode: undefined
      }
    }
  },
  created() {
    this.searchProduct()
  },
  methods: {

    formatDate(row, column) {
      const date = row[column.property]
      if (date === undefined) {
        return ''
      }
      // 使用moment格式化时间，由于我的数据库是默认时区，偏移量设置0，各自根据情况进行配置
      return moment(date).utcOffset(0).format('YYYY-MM-DD HH:mm')
    },
    dialogProduct() {
      // 添加先初始化空状态
      this.product.id = undefined
      this.product.keyCode = ''
      this.product.title = ''
      this.product.desc = ''
      this.product.operator = this.op_user
      this.dialogProductStatus = 'ADD'
      // 弹出对话框设置为true
      this.dialogProductShow = true
    },
    dialogProductUpdate(row) {
      // 添加先初始化空状态
      this.product.id = row.id
      this.product.keyCode = row.keyCode
      this.product.title = row.title
      this.product.desc = row.desc
      this.product.operator = this.op_user
      this.dialogProductStatus = 'UPDATE'
      // 弹出对话框设置为true
      this.dialogProductShow = true
    },

    pCreate() {
      // 请求API进行添加
      apiProductCreate(this.product).then(response => {
        // 如果request.js没有拦截即表示成功，给出对应提示和操作
        this.$notify({
          title: '成功',
          message: '项目或产品添加成功',
          type: 'success'
        })
        // 关闭对话框
        this.dialogProductShow = false
        // 重新查询刷新数据显示
        this.getProductList()
      })
    },
    pHardRemove(id) {
      this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        // then 点击confirmButton后执行的方法，否则是不执行关闭对话框
      }).then(() => {
        // vue click时候传d的id需要定义参数
        apiProductDelete(id).then(res => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          // 重新查询刷新数据显示
          this.getProductList()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    pSoftRemove(id) {
      this.$confirm('此操作将停用该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
        // then 点击confirmButton后执行的方法，否则是不执行关闭对话框
      }).then(() => {
        // vue click时候传d的id需要定义参数
        apiProductRemove(id).then(res => {
          this.$message({
            type: 'success',
            message: '停用成功!'
          })
          // 重新查询刷新数据显示
          this.getProductList()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    pUpdate() {
      apiProductUpdate(this.product).then(response => {
        this.$notify({
          title: '成功',
          message: '项目或产品修改成功',
          type: 'success'
        })
        // 关闭对话框
        this.dialogProductShow = false
        // 重新查询刷新数据显示
        this.getProductList()
      })
    },
    searchProduct() {
      apiProductSearch(this.search).then(response => {
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
