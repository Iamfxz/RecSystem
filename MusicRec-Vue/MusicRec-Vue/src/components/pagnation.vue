<template>
  <nav>
    <ul class="pagination">
      <li :class="{'disabled': current === 1}"><a href="javascript:" @click="setCurrent(current - 1)"> « </a></li>
      <li :class="{'disabled': current === 1}"><a href="javascript:" @click="setCurrent(1)"> 首页 </a></li>
      <li v-for="p in grouplist" :class="{'active': current === p.val}" :key="p.val">
        <a href="javascript:" @click="setCurrent(p.val)"> {{ p.text }} </a>
      </li>
      <li :class="{'disabled': current === page}"><a href="javascript:" @click="setCurrent(page)"> 尾页 </a></li>
      <li :class="{'disabled': current === page}"><a href="javascript:" @click="setCurrent(current + 1)"> »</a></li>
    </ul>
  </nav>
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
      coerce: function (v) {
        v = v > 0 ? v : 5
        return v % 2 === 1 ? v : v + 1
      }
    },
    refresh: { // 不是必须 搜索后默认第一页
      type: Boolean,
      default: false
    }
  },
  computed: {
    page: function () { // 总页数
      return Math.floor(this.total / this.display)
    },
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
      if (this.current !== idx && idx > 0 && idx < this.page + 1) {
        this.current = idx
        this.$emit('pagechange', this.current)
      }
    }
  }
}
</script>

<style scoped>
  .pagination {
    font-family: "sans",serif;
    overflow: hidden;
    display: table;
    border: 1px solid #eee;
    margin: 20px auto;
  }

  .pagination li {
    float: left;
    height: 30px;
    border-radius: 5px;
    margin: 3px;
    color: #000000;
    background: white;
  }

  .pagination li :hover {
    background: #696969;
  }

  .pagination li :hover a {
    color: #fff;
  }

  .pagination li a {
    display: block;
    width: 40px;
    height: 30px;
    text-align: center;
    line-height: 30px;
    font-size: 12px;
    border-radius: 5px;
    text-decoration: none;
    color: black;
  }

  .pagination .active {
    background: #696969;
  }

  .pagination .active a {
    color: #fff;
  }
</style>
