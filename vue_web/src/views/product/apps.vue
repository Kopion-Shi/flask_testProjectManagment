<template>
  <div class="app-container">
    <div class="filter-container">
      <el-form :inline="true" :model="search">
        <el-form-item label="归属分类">
          <el-select v-model="search.productId" filterable="true" clearable>
            <el-option value="" label="所有" />
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            >
              <span style="float: left">{{ item.keyCode }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.title }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="应用ID">
          <el-input v-model="search.appId" placeholder="服务ID关键词" style="width: 200px;" clearable />
        </el-form-item>
        <el-form-item label="描 述">
          <el-input v-model="search.note" placeholder="描述模糊搜索" style="width: 200px;" clearable />
        </el-form-item>
        <br>
        <el-form-item label="研  发">
          <el-input v-model="search.developer" placeholder="默认研发" style="width: 210px;" clearable />
        </el-form-item>
        <el-form-item label="产  品">
          <el-input v-model="search.producer" placeholder="默认产品" style="width: 210px;" clearable />
        </el-form-item>
        <el-form-item label="测  试">
          <el-input v-model="search.tester" placeholder="默认测试" style="width: 210px;" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" plain @click="searchClick()">搜索</el-button>
        </el-form-item>
      </el-form>
      <el-button type="primary" icon="el-icon-plus" style="float:right" @click="addApp()">添加应用</el-button>
    </div>
    <!--:data 绑定data()的数组值,会动态根据其变化而变化-->
    <el-table :data="tableData">
      <!--:data prop绑定{}中的key，label为自定义显示的列表头-->
      <el-table-column prop="appId" label="应用ID" />
      <el-table-column prop="note" label="描述" show-overflow-tooltip />
      <el-table-column prop="title" label="归属分类" />
      <el-table-column prop="developer" label="默认研发" />
      <el-table-column prop="producer" label="默认产品" />
      <el-table-column prop="tester" label="默认测试" />
      <el-table-column prop="updateUser" label="更新人" />
      <el-table-column :formatter="formatDate" prop="updateDate" label="更新时间" />
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-link icon="el-icon-edit" @click="updateApp(scope.row)">修改</el-link>
        </template>
      </el-table-column>
    </el-table>
    <br>
    <div>
      <el-pagination
        background
        :total="total"
        :current-page.sync="search.currentPage"
        :page-size="search.pageSize"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[5, 10, 20, 30, 50]"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    <div>
      <el-drawer
        :title="appAction==='ADD'? '添加应用': '修改应用'"
        :visible.sync="drawerVisible"
        size="45%"
        direction="rtl"
      >
        <div>
          <el-form ref="appInfo" :model="appInfo" :rules="rules" label-width="120px">
            <el-form-item label="应用ID" prop="appId">
              <el-input v-model="appInfo.appId" :disabled="appAction==='ADD'? false : true" style="width: 300px" />
            </el-form-item>
            <el-form-item label="归属分类" prop="productId">
              <el-select v-model="appInfo.productId" style="width: 300px">
                <el-option
                  v-for="item in options"
                  :key="item.id"
                  :label="item.title"
                  :value="item.id"
                >
                  <span style="float: left">{{ item.keyCode }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.title }}</span>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="应用描述">
              <el-input v-model="appInfo.note" style="width: 300px" />
            </el-form-item>
            <el-form-item label="测试负责" prop="tester">
              <el-input v-model="appInfo.tester" style="width: 300px" />
            </el-form-item>
            <el-form-item label="研发负责" prop="developer">
              <el-input v-model="appInfo.developer" style="width: 300px" />
            </el-form-item>
            <el-form-item label="产品负责" prop="producer">
              <el-input v-model="appInfo.producer" style="width: 300px" />
            </el-form-item>
            <el-form-item label="默认抄送">
              <el-input v-model="appInfo.cCEmail" style="width: 300px" />
            </el-form-item>
            <el-form-item label="代码地址">
              <el-input v-model="appInfo.gitCode" style="width: 300px" />
            </el-form-item>
            <el-form-item label="相关wiki">
              <el-input v-model="appInfo.wiki" style="width: 300px" />
            </el-form-item>
            <el-form-item label="更多信息">
              <el-input v-model="appInfo.more" style="width: 300px" />
            </el-form-item>
            <el-form-item>
              <span class="dialog-footer">
                <el-button @click="drawerVisible=false">取 消</el-button>
                <el-button type="primary" @click="commitApp('appInfo')">提 交</el-button>
              </span>
            </el-form-item>
          </el-form>
        </div>
      </el-drawer>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { apiAppsProduct, apiAppsSearch } from '@/api/apps'
import store from '@/store'

export default {
  name: 'Apps',
  data() {
    return {
      op_user: store.getters.name,
      // 定义动作
      appAction: 'ADD',
      // 控制抽屉显示隐藏
      drawerVisible: false,
      // 添加/修改绑定的数据
      appInfo: {
        id: '',
        appId: '',
        productId: '',
        note: '',
        tester: '',
        developer: '',
        producer: '',
        cCEmail: '',
        gitCode: '',
        wiki: '',
        more: '',
        creteUser: '',
        updateUser: ''
      },
      // 规则设定
      rules: {
        appId: [
          { required: true, message: '请输应用名称', trigger: 'blur' }
        ],
        productId: [
          { required: true, message: '请选择所属范围', trigger: 'change' }
        ],
        tester: [
          { required: true, message: '请输入测试负责人', trigger: 'blur' }
        ],
        developer: [
          { required: true, message: '请输入开发负责人', trigger: 'blur' }
        ],
        producer: [
          { required: true, message: '请输入产品负责人', trigger: 'blur' }
        ]
      },

      search: {
        productId: '',
        appId: '',
        note: '',
        developer: '',
        producer: '',
        tester: '',
        pageSize: 10,
        currentPage: 1
      },
      options: [],
      total: 0,
      tableData: []
    }
  },
  // 页面生命周期中的创建阶段调用
  created() {
    // 调用methods的方法，即初次加载就请求数据
    this.productList()
    this.searchClick()
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
    productList() {
      apiAppsProduct().then(resp => {
        this.options = resp.data
      })
    },
    searchClick() {
      console.log(this.search)
      apiAppsSearch(this.search).then(response => {
        // 将返回的结果赋值给表格自动匹配
        this.tableData = response.data
        this.total = response.total
      })
    },
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`)
      this.search.pageSize = val
      this.searchClick()
    },
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.search.currentPage = val
      this.searchClick()
    },
    addApp() {
      this.drawerVisible = true
    },
    updateApp() {
      this.drawerVisible = true
    }
  }

}
</script>

<style scoped>
.el-pagination {
  text-align: right;
}
</style>
