<template>
  <div class="reHeader">
    <div class="headTop">
      <img class="topLogo" src="../assets/img/logo.png" alt="音乐推荐系统"/>
      <div class="userbtn">欢迎！{{getName}}&nbsp&nbsp&nbsp
        <el-button type="danger" round icon="el-icon-switch-button" @click="waitlayout">切换用户</el-button>
      </div>
    </div>

    <ul class="headNav">
      <li v-for="item in datas" :key="item.cate_id" @click="emitGetNews(item.cate_id)"
          :class="active === item.cate_id ? 'navActive':''">{{item.cate_name}}
      </li>
<!--      <li><a class="adminlink el-icon-s-tools" :href="serverlink" target="_blank">进去后台</a></li>-->
    </ul>
  </div>
</template>

<script>
  import {mapGetters, mapActions} from 'vuex'
  import {getCateData, layout} from '@/assets/js/api'
  import {serverUrl} from '@/assets/js/linkBase'

  export default {
    data() {
      return {
        datas: [{
          cate_id: '',
          cate_name: ''
        }],  //返回所有的cate
        serverlink: '', //服务器地址 + admin/
      }
    },
    props: {
      active: String
    },
    // 超引用（ES6）传入getter到计算属性computed,并映射到局部方法
    computed: {
      ...mapGetters('vuexLogin', {
        getLogin: 'getLogin',
        getName: 'getName'
      })
    },
    methods: {
      ...mapActions('vuexLogin', {
        login: 'login',
        chooseUser: 'chooseUser'
      }),

      emitGetNews: function (cateid) {
        // 切换页面时候设置默认请求参数
        let option = {
          'cateid': cateid,
          'tag': 'all',
          'pagesize': 30,
          'page': 1
        }

        this.$emit('onGetnews', option)
        // this.setSearchable(cateid)
      },

      waitlayout: function () {
        this.$layer.confirm('确定退出当前用户，切换其他用户？', {title: '尊敬的用户'}, () => {
          this.layout();
          this.$layer.closeAll()
        })
      },

      //重新登录
      layout: function () {
        layout().then((res) => {
          if (res.code) {
            localStorage.removeItem('loginTime');
            localStorage.removeItem('username');
            localStorage.removeItem('islogin');
            this.login(localStorage.getItem('islogin'));
            this.chooseUser(localStorage.getItem('username'));
            this.$router.push('/login')
          }
        }, (err) => {
          console.log(err)
        })
      },

      // 获取导航栏
      getCate: function () {
        this.loading('加载中...');
        getCateData().then((res) => {
          if (!res.code) {
            this.layout()
          } else {
            this.$layer.closeAll();
            this.datas = res.data
            //console.log(res.data)
          }
        }, (err) => {
          this.$message({
            message: '小主稍等，紧急恢复中...',
            type: "error"
          });
        })
      },
    },

    mounted() {
      this.serverlink = serverUrl + 'admin/';
      this.getCate()
    }
  }
</script>

<style lang="less" scoped>
  @baseColor: red;
  #ellies(@n) {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: @n;
    -webkit-box-orient: vertical;
  }

  .el-select .el-input {
    width: 130px;
  }

  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }

  .reHeader {
    .headTop {
      .userbtn {
        display: inline-block;
        float: right;
        line-height: 80px;
        margin-right: 5%;

        .layouticon {
          padding: 3px;
          border: 1px solid #eee;
          text-align: center;
          border-radius: 3px;
          background: #eee;
          margin-left: 10px;
          cursor: pointer;

          &:hover {
            background: #ddd;
          }
        }
      }
    }

    .headNav {
      float: left;
      width: 70%;
      display: flex;
      justify-content: flex-start;
      align-items: center;
      background: #ddd;
      height: 40px;

      li {
        display: inline-block;
        width: 120px;
        padding: 5px 15px;
        box-sizing: border-box;
        position: relative;
        text-align: center;
        cursor: pointer;
        color: #555;

        .adminlink {
          text-decoration: none;
          color: #555;

          &:hover {
            color: #000
          }
        }

        &:hover {
          color: #000
        }
      }

      .navActive::after {
        content: " ";
        display: block;
        position: absolute;
        bottom: -6px;
        width: 30%;
        left: 50%;
        border-bottom: 2px solid @baseColor;
        margin-left: -15%;
        color: #000;
      }
    }
  }
</style>
