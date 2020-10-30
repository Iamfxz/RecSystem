<template>
  <el-pagination
    @size-change="handleSizeChange"
    @current-change="setCurrent"
    :current-page="currentPage"
    :page-size="this.display"
    layout="total, sizes, prev, pager, next, jumper"
    :total="this.total">
  </el-pagination>
</template>

<script>
  export default {
    name: 'paging',
    data () {
      return {
        current: this.currentPage
      }
    },
    props: {
      total: {// 数据总条数
        type: Number,
        default: 0
      },
      display: {// 每页显示条数
        type: Number,
        default: 30
      },
      currentPage: {// 当前页码
        type: Number,
        default: 1
      },
      pagegroup: {// 分页条数
        type: Number,
        default: 5,
        // coerce: function (v) {
        //   v = v > 0 ? v : 5
        //   return v % 2 === 1 ? v : v + 1
        // }
      },
      refresh: { // 不是必须 搜索后默认第一页
        type: Boolean,
        default: false
      }
    },
    computed: {
      page: function () { // 总页数,向上取整
        return Math.ceil(this.total / this.display)
      },
      grouplist: function () { // 获取分页页码
        this.doRefresh()
        let len = this.page, temp = [], list = [], count = Math.floor(this.pagegroup / 2), center = this.current
        if (len <= this.pagegroup) {
          while (len--) {
            temp.push({text: this.page - len, val: this.page - len})
          }
          return temp
        }
        while (len--) {
          temp.push(this.page - len)
        }
        let idx = temp.indexOf(center);
        (idx < count) && (center = center + count - idx);
        (this.current > this.page - count) && (center = this.page - count)
        temp = temp.splice(center - count - 1, this.pagegroup)
        do {
          let t = temp.shift()
          list.push({
            text: t,
            val: t
          })
        } while (temp.length)
        if (this.page > this.pagegroup) {
          (this.current > count + 1) && list.unshift({text: '...', val: list[0].val - 1});
          (this.current < this.page - count) && list.push({text: '...', val: list[list.length - 1].val + 1})
        }
        return list
      }
    },
    mounted () {
      this.doRefresh()
    },
    methods: {
      doRefresh () {
        if (this.refresh) {
          this.current = 1
        }
      },
      setCurrent: function (idx) {
        // console.log(this.page)
        if (this.current !== idx && idx > 0 && idx < this.page + 1) {
          this.current = idx
          this.$emit('pageChange', this.current)
        }
      },
      handleSizeChange:function (size) {
        this.$emit('pageSizeChange', size)
      }
    }
  }
</script>

<style scoped>

</style>
