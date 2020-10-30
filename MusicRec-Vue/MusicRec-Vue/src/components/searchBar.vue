<template>
  <el-autocomplete :placeholder="searchText()" v-model="search_name"
                   :fetch-suggestions="getSearch" :trigger-on-focus="false" @select="select_name"
                   style="float: right;width: 30%" suffix-icon="el-icon-search" v-if="show">
  </el-autocomplete>
</template>

<script>
  import {getSearchPlaylist, getSearchSongList, getSearchSingList, getSearchUserList} from "@/assets/js/api";

  export default {
    name: "searchBar",
    data() {
      return {
        search_name: '', //当前搜索框内的文字
        search_result: [], // 搜索结果的列表
        show: false //默认显示搜索框,因为cate初始为1
      }
    },
    props: {
      active: String
    },
    watch: {
      // 非搜索页面时，隐藏搜索框
      active: function (newValue) {
        this.show = parseInt(newValue) > 1 && parseInt(newValue) < 6;
      }
    },
    methods: {
      searchText: function(){
        if(this.active==='2'){
          return '请输入您要搜索的歌单'
        }else if(this.active==='3'){
          return '请输入您要搜索的歌曲'
        }else if(this.active==='4'){
          return '请输入您要搜索的歌手'
        }else if(this.active==='5'){
          return '请输入您要搜索的用户'
        }else {
          return '请输入您要搜索的内容'
        }
      },
      // 1.远程获取搜索结果及对应id
      getSearch: function (queryString, callback) {
        const option = {
          'search': this.search_name,
          'username': this.$store.state.vuexLogin.userName
        }
        //todo 根据不同cate调用搜索接口
        if(this.active === '2') {
          getSearchPlaylist(option).then((res) => {
            // console.log(res)
            this.search_result = res.data
            callback(res.data)
          }, (err) => {
            console.log(err)
            this.$message({
              message: '小主稍等，紧急恢复中...',
              type: "error"
            });
            this.search_result = []
          })
        }else if(this.active === '3'){
          getSearchSongList(option).then((res) => {
            // console.log(res)
            this.search_result = res.data
            callback(res.data)
          }, (err) => {
            console.log(err)
            this.$message({
              message: '小主稍等，紧急恢复中...',
              type: "error"
            });
            this.search_result = []
          })
        }else if(this.active === '4'){
          getSearchSingList(option).then((res) => {
            // console.log(res)
            this.search_result = res.data
            callback(res.data)
          }, (err) => {
            console.log(err)
            this.$message({
              message: '小主稍等，紧急恢复中...',
              type: "error"
            });
            this.search_result = []
          })
        }else if(this.active === '5'){
          getSearchUserList(option).then((res) => {
            // console.log(res)
            this.search_result = res.data
            callback(res.data)
          }, (err) => {
            console.log(err)
            this.$message({
              message: '小主稍等，紧急恢复中...',
              type: "error"
            });
            this.search_result = []
          })
        }
      },

      // 2.点击搜索结果后根据id调用相应显示函数
      select_name: function () {
        //遍历查找搜索id
        let search_id
        for (let i of this.search_result) {
          if (i.value === this.search_name)
            search_id = i.id
        }
        //搜索结果id发送到home.vue
        this.$emit('onSelectChange', search_id)

      }
    }
  }

</script>

<style scoped>

</style>
