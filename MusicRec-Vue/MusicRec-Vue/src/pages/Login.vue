<template>
  <div class="login">
    <div v-if="!(showstep2 || showstep3)" class="loginstep">
      <div class=" posirelative select-out-div">
        <el-select class="userSelect" style="width: 100%; padding: 2px 0;" v-model="loginUser">
          <el-option v-for="(item,index) in users" :key="index" :value="item">{{item}}</el-option>
        </el-select>
        <span class="select-hide-span"><b class="select-show-b"></b></span>
      </div>
      <el-button class="nextBtn" @click="shownext(1)">下一步</el-button>
    </div>
    <div v-if="showstep2" class="loginstep2">
      <h3>选择喜爱的歌手</h3>
      <div class="alltag">
          <span class="tagbox" v-for="(tag,index) in sings" :key="index">
            <label for="singsbox"></label>
            <input type="checkbox" v-model="singsTags" name="singsbox" :value="index" id="singsbox"/>
            {{tag}}
          </span>
      </div>
      <div class="twobtn">
        <el-button class="skip" @click="shownext(3)">跳过</el-button>
        <el-button class="go" @click="shownext(2)">下一步</el-button>
      </div>
    </div>
    <div v-if="showstep3" class="loginstep2">
      <h3>选择喜爱的歌曲</h3>
      <div class="alltag">
          <span class="tagbox" v-for="(tag,index) in songs" :key="index">
            <label for="songsbox"></label>
            <input type="checkbox" v-model="songsTags" name="songsbox" :value="index" id="songsbox"/>
            {{tag}}
          </span>
      </div>
      <div class="twobtn">
        <el-button class="skip" @click="goLogin('skip')">跳过</el-button>
        <el-button class="go" @click="goLogin">进入系统</el-button>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapActions} from 'vuex'
  import {getLogin, login} from '@/assets/js/api'

  export default {
    name: 'z',
    data() {
      return {
        users: {},
        tags: [],
        showstep2: false,
        loginUser: '',
        singsTags: [],
        songsTags: [],
        sings: {},
        songs: {},
        showstep3: false
      }
    },
    methods: {
      ...mapActions('vuexLogin', {
        login: 'login',
        chooseUser: 'chooseUser'
      }),
      shownext: function (n) {
        if (n === 1) {
          if (!this.loginUser) {
            this.$layer.alert('请输入要登陆的用户', {title: '温馨提示', btn: '好嘞，了解'})
            return false
          } else {
            this.showstep2 = true
          }
        } else if (n === 2) {
          if (this.singsTags.length < 3 && this.singsTags.length >= 0) {
            this.$layer.alert('至少选择三个标签哦', {title: '温馨提示', btn: '好哒'})
            return false
          } else {
            this.showstep2 = false
            this.showstep3 = true
          }
        } else if (n === 3) {
          this.showstep2 = false
          this.showstep3 = true
        }
      },
      // 发送登录请求
      goLogin: function (opt) {
        // let encrypt = new JSEncrypt();
        // encrypt.setPublicKey('MIIBIjANBgkqhkiG9w0BA' +
        //   'QEFAAOCAQ8AMIIBCgKCAQEArtA8SL7cC24aOle5BhOXdqrmSl5' +
        //   '8Etqiv9umMuolbn8XVtbDQFWsAhP55RRZBZnlOGilzF49lPvi/tE' +
        //   'Udby5en6QeFJnF1UDmQ+9MikYeJ9/SYyhsJAluynLzTZal4+XdL/Q1' +
        //   'LVM9DtWacRNivBlBVI6V84gJznI8sSG7XYcZTGCN39t+fGq5qDbfRe3M' +
        //   'y+bfgVR0aw7Eh6tQCt9TMBhdyzV+QMaA5kAMEcioHyoqJGGbG4XJXOUY+k5' +
        //   'Nsz3+JZLKdsjXQ5A/XIVqnzSLeuhkUaKIcW2TMPjeewoMq6RJAxnugjnVO4o' +
        //   '27aFu6hUIu6YVCIoTvGj92zlZrwuV/rynQIDAQAB')
        // let encrypted = encrypt.encrypt('123456');
        // console.log(encrypted)
        let loginInfo = {
          username: this.loginUser,
          sings: '',
          songs: '',
          cate: 1,
          baseclick: 0
        };
        // console.log(this.boxTags)
        if (opt && opt === 'skip') {
          loginInfo.sings = ''
          loginInfo.songs = ''
        } else {
          if (this.songsTags.length < 3 && this.songsTags.length >= 0) {
            this.$layer.alert('至少选择三个标签哦', {title: '温馨提示', btn: '好哒'})
            return false
          } else {
            loginInfo.sings = this.singsTags.join(',')
            loginInfo.songs = this.songsTags.join(',')
            this.singsTags = []
            this.songsTags = []
          }
        }
        console.log(loginInfo)
        login(loginInfo).then((res) => {
          if (res.code) {
            localStorage.setItem('loginTime', Date())
            this.login(true)
            this.chooseUser(res.data.username)
            this.$router.push({
              path: '/',
              query: {username: res.data.username, sings: res.data.sings, songs: res.data.songs, baseclick: 0}
            })
          }
        }, (err) => {
          console.log(err)
        })
      }
    },
    mounted() {
      getLogin().then((res) => {
        if (res.code === 1) {
          this.users = res.data.users
          this.sings = res.data.sings
          this.songs = res.data.songs
        }
      }, (err) => {
        console.log(err)
      })
    }
  }
</script>

<style lang="less" scoped>
  #logins() {
    width: 40%;
    min-height: 300px;
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    border: 1px solid #eee;
    padding-bottom: 20px;
    margin-bottom: 20px;
  }

  @baseColor: #20a0ff;
  .login {
    width: 100%;
    min-height: 100%;
    position: absolute;
    background: url("../assets/img/background0.jpeg");
    background-size: contain;
    display: flex;
    justify-content: center;
    align-items: center;

    .loginstep {
      #logins();

      .posirelative {
        position: relative;
        width: 70%;
        overflow: hidden;
        margin-bottom: 30px;

        /*select.userSelect {*/
        /*  background-color: #ffffff;*/
        /*  background-image: none !important;*/
        /*  filter: none !important;*/
        /*  border: 1px solid #e5e5e5;*/
        /*  outline: none;*/
        /*  height: 35px !important;*/
        /*  line-height: 35px;*/
        /*}*/

        .select-hide-span {
          height: 35px;
          position: absolute;
          top: 0;
          border-right: 1px solid #e5e5e5;
          right: 0;
          width: 20px !important;
          z-index: 999;

          /*.select-show-b {*/
          /*  border-color: #888 transparent transparent transparent;*/
          /*  border-style: solid;*/
          /*  border-width: 5px 4px 0 4px;*/
          /*  margin-left: -4px;*/
          /*  margin-top: 15px;*/
          /*  position: absolute;*/
          /*}*/
        }
      }

      .nextBtn {
        &:hover {
          color: #fff;
          background: @baseColor;
        }
      }
    }

    .loginstep2 {
      #logins();
      justify-content: space-around;

      h3 {
        margin-top: 10px;
      }

      .twobtn {
        width: 100%;
        display: flex;
        justify-content: space-around;

        .skip, .go {
          width: 30%;

          &:hover {
            color: #fff;
            background: @baseColor;
          }
        }

        .skip:hover {
          background: #999;
        }
      }

      .alltag {
        padding: 10px;

        .tagbox {
          display: inline-flex;
          padding: 3px;
          border: 1px solid #999;
          border-radius: 3px;
          justify-content: center;
          align-items: center;
          margin: 8px;

          input {
            cursor: pointer;
          }
        }
      }
    }
  }

</style>
