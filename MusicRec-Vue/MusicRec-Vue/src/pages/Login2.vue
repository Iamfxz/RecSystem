<template>
  <div class="page">
    <div class="login-box">
      <p class="title">
        <img src="https://img.icons8.com/ios/20/000000/login-rounded-down.png" alt="登录图标"/>
        欢迎登录
      </p>
      <el-tabs v-model="activeName">
        <el-tab-pane label="密码登录" name="first">
          <el-form
            :model="ruleForm"
            status-icon
            :rules="rules"
            ref="ruleForm"
            label-width="0">
            <el-form-item prop="account">
              <el-select filterable clearable allow-create type="text"
                         style="width: 100%" prefix-icon="el-icon-user-solid"
                         v-model="ruleForm.account" placeholder="请输入账号">
                <div class="el-icon-user-solid"  style="padding: 5px" slot = "prefix"></div>
                <el-option v-for="(item,index) in users" :key="index" :value="item">{{item}}</el-option>
              </el-select>
            </el-form-item>
            <el-form-item prop="pass" v-if="visible">
              <el-input
                type="password"
                prefix-icon="el-icon-lock"
                v-model="ruleForm.pass"
                auto-complete="off"
                placeholder="请输入密码">
                <i slot="suffix"
                  title="显示密码"
                  @click="changePass('show')"
                  style="cursor:pointer;"
                  class="iconfont iconyanjing_kai"></i>
              </el-input>
            </el-form-item>
            <el-form-item prop="pass" v-else>
              <el-input type="text" v-model="ruleForm.pass" auto-complete="off" placeholder="请输入密码">
                <i slot="suffix"
                  title="隐藏密码"
                  @click="changePass('hide')"
                  style="cursor:pointer;"
                  class="iconfont iconyanjing_bi"></i>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                :loading="logining"
                :disabled="true"
                v-if="!isLog"
                @click="submitForm('ruleForm')"
                style="width:100%;">登录</el-button>
              <el-button
                type="primary"
                :loading="logining"
                v-else-if="isLog"
                @click="submitForm('ruleForm')"
                style="width:100%;">登录</el-button>
              <!-- <p class="login" @click="gotoLogin">已有账号？立即登录</p> -->
            </el-form-item>
<!--            <el-form-item class="login">-->
<!--              <label class="showPasswordToggle">-->
<!--                <el-checkbox v-model="checked" id="showPasswordCheck">已阅读并同意《服务协议》</el-checkbox>-->
<!--              </label>-->
<!--              <div class="gotoRight">-->
<!--                <span @click="gotoLoginForget" class="hoverBlue">忘记密码</span>-->
<!--                <el-divider direction="vertical"></el-divider>-->
<!--                <span @click="gotoLoginReg" class="hoverBlue">免费注册</span>-->
<!--              </div>-->
<!--            </el-form-item>-->
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="短信登录" name="second">
          <el-form
            :model="ruleForm2"
            status-icon
            :rules="rules"
            ref="ruleForm2"
            label-width="0"
            class="demo-ruleForm">
            <el-form-item prop="tel">
              <el-input prefix-icon="el-icon-mobile-phone" v-model="ruleForm2.tel" auto-complete="off" placeholder="请输入手机号"></el-input>
            </el-form-item>
            <el-form-item prop="smscode" class="code">
              <el-input prefix-icon="el-icon-chat-dot-square" v-model="ruleForm2.smscode" placeholder="短信验证码"></el-input>
              <el-button :disabled="true" @click="sendCode" v-if="disabled=== 0">{{buttonText}}</el-button>
              <el-button
                type="primary"
                :disabled="isDisabled"
                class="btn-color"
                @click="sendCode"
                v-else-if="disabled=== 1">{{buttonText}}</el-button>
            </el-form-item>
            <el-form-item>
              <el-button
                :loading="logining"
                :disabled="true"
                v-if="!isLogin"
                @click="submitSMS('ruleForm')"
                style="width:100%;">登录</el-button>
              <el-button
                type="primary"
                :loading="logining"
                v-else-if="isLogin"
                @click="submitSMS('ruleForm')"
                style="width:100%;"
              >登录</el-button>
            </el-form-item>
<!--            <el-form-item class="login">-->
<!--              <label class="showPasswordToggle">-->
<!--                <el-checkbox v-model="checked" id="showPasswordCheck">已阅读并同意《服务协议》</el-checkbox>-->
<!--              </label>-->
<!--              <div class="gotoRight">-->
<!--                <span @click="gotoLoginForget">忘记密码</span>-->
<!--                <el-divider direction="vertical"></el-divider>-->
<!--                <span @click="gotoLoginReg">免费注册</span>-->
<!--              </div>-->
<!--            </el-form-item>-->
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
  import {mapActions} from "vuex";
  import {getLogin, login, smsLogin, smsValid} from "@/assets/js/api";

  export default {
    name: "Login2",
    data: function () {
      // <!--验证账号-->
      let account = (rule, value, callback) => {
        if (value === "") {
          callback();
        } else {
          callback();
        }
      };
      // <!--验证密码-->
      let validatePass = (rule, value, callback) => {
        if (value === "") {
          callback();
        } else {
          callback();
        }
      };
      // <!--验证手机号是否合法-->
      let checkTel = (rule, value, callback) => {
        if (value === "") {
          callback();
        } else if (!this.checkMobile(value)) {
          callback(new Error("请输入正确的11位手机号码"));
        } else {
          callback();
        }
      };
      //  <!--验证码是否为空-->
      let checkSmscode = (rule, value, callback) => {
        if (value === "") {
          // callback(new Error("请输入手机验证码"));
          callback();
        } else {
          callback();
        }
      };
      return {
        users: {},
        sings: {},
        songs: {},
        ruleForm: {
          account: "",
          pass: ""
        },
        ruleForm2: {
          tel: "",
          smscode: ""
        },
        rules: {
          account: [
            {required: false, message: "请输入账号", trigger: "blur"},
            {
              pattern: /./,
              message: "账号为用户昵称",
              trigger: "blur"
            },
            {validator: account, trigger: "blur"}
          ],
          pass: [
            {required: false, message: "请输入密码", trigger: "blur"},
            {
              pattern: /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$/,
              message: "密码长度为6-20位，含有数字和字母",
              trigger: "blur"
            },
            {validator: validatePass, trigger: "blur"}
          ],
          tel: [
            {required: false, message: "请输入手机号", trigger: "blur"},
            {
              pattern: /^[1][3-9][0-9]{9}$/,
              message: "请输入正确的11位手机号码",
              trigger: "blur"
            },
            {validator: checkTel, trigger: "blur"}
          ],
          smscode: [
            {required: false, message: "请输入短信验证码", trigger: "blur"},
            {
              pattern: /^[0-9]{4}$/,
              message: "请输入正确的四位数字验证码",
              trigger: "blur"
            },
            {validator: checkSmscode, trigger: "blur"}
          ]
        },
        activeName: "first",
        buttonText: "获取短信验证码",
        isDisabled: false, // 是否禁止点击发送验证码按钮
        flag: true,
        visible: true,
        checked: true,
        disabled: 0,
        isLog: false,
        isLogin: false,
        logining: false
      };
    },
    watch: {
      //账号验证btn按钮显示高亮
      ruleForm: {
        handler: function() {
          this.isLog = this.ruleForm.account !== "" && this.ruleForm.pass !== "";
        },
        deep: true
      },
      //账手机验证btn按钮显示高亮
      "ruleForm2.tel"() {
        if (this.ruleForm2.tel !== "") {
          this.disabled = 1;
        } else {
          this.disabled = 0;
        }
      },
      ruleForm2: {
        handler: function(val, oldval) {
          this.isLogin = val.tel !== "" && val.smscode !== "";
        },
        deep: true //对象内部的属性监听，也叫深度监听
      }
    },
    methods: {
      // 载入vuex中的方法
      ...mapActions('vuexLogin', {
        login: 'login',
        chooseUser: 'chooseUser'
      }),
      //密码判断渲染，true:暗文显示，false:明文显示
      changePass(value) {
        this.visible = !(value === "show");
      },
      // <!--发送验证码-->
      sendCode() {
        let tel = this.ruleForm2.tel;
        if (this.checkMobile(tel)) {
          let loginInfo = {'phone':tel}
          console.log(loginInfo)
          smsLogin(loginInfo).then((res) => {
            this.$layer.closeAll()
            if(res.code === 200){
              this.$message({
                message: '您的验证码已发送',
                type: "success"
              });
            }else{
              this.$message({
                message: res.data,
                type: "error"
              });
            }
          })
          let time = 60;
          this.buttonText = "已发送";
          this.isDisabled = true;
          if (this.flag) {
            this.flag = false;
            let timer = setInterval(() => {
              time--;
              this.buttonText = time + " s";
              if (time === 0) {
                clearInterval(timer);
                this.buttonText = "重新获取";
                this.isDisabled = false;
                this.flag = true;
              }
            }, 1000);
          }
        }
      },
      // 提交sms code 登录
      submitSMS(formNme){
        // console.log(formNme)
        let validInfo={
          'phone':this.ruleForm2.tel,
          'sms':this.ruleForm2.smscode
        }
        console.log(validInfo)
        smsValid(validInfo).then((res) =>{
          if(res.code === 200){
            setTimeout(() => {
              this.$message({
                message: "登录成功！",
                type: "success"
              });
              this.logining = false; //登陆操作完毕
            }, 400);
            localStorage.setItem('loginTime', Date())
            //Vuex设置
            this.login(true)
            this.chooseUser(res.data.username)
            //router设置
            this.$router.push({
              path: '/',
              query: {username: res.data.username, baseclick: 0}
            })
          }else {
            setTimeout(() => {
              this.$message({
                message: res.data,
                type: "error"
              });
            }, 400);
          }
        })
      },
      // <!--提交密码登录-->
      submitForm(formName) {
        let encrypt = new JSEncrypt();
        encrypt.setPublicKey('MIIBIjANBgkqhkiG9w0BA' +
          'QEFAAOCAQ8AMIIBCgKCAQEArtA8SL7cC24aOle5BhOXdqrmSl5' +
          '8Etqiv9umMuolbn8XVtbDQFWsAhP55RRZBZnlOGilzF49lPvi/tE' +
          'Udby5en6QeFJnF1UDmQ+9MikYeJ9/SYyhsJAluynLzTZal4+XdL/Q1' +
          'LVM9DtWacRNivBlBVI6V84gJznI8sSG7XYcZTGCN39t+fGq5qDbfRe3M' +
          'y+bfgVR0aw7Eh6tQCt9TMBhdyzV+QMaA5kAMEcioHyoqJGGbG4XJXOUY+k5' +
          'Nsz3+JZLKdsjXQ5A/XIVqnzSLeuhkUaKIcW2TMPjeewoMq6RJAxnugjnVO4o' +
          '27aFu6hUIu6YVCIoTvGj92zlZrwuV/rynQIDAQAB')
        let password_encrypted = encrypt.encrypt(this.ruleForm.pass)
        // console.log(formName)
        let loginInfo = {
          username: this.ruleForm.account,
          password: password_encrypted,
          sings: '',
          songs: '',
          cate: 1,
          baseclick: 0
        };
        console.log(loginInfo)
        this.$refs[formName].validate(valid => {
          // 格式验证成功
          if (valid) {
            this.logining = true; //登陆中
            login(loginInfo).then((res) => {
              //登录成功
              if (res.code === 200) {
                setTimeout(() => {
                  this.$message({
                    message: "登录成功！",
                    type: "success"
                  });
                  this.logining = false; //登陆操作完毕
                }, 400);
                localStorage.setItem('loginTime', Date())
                //Vuex设置
                this.login(true)
                this.chooseUser(res.data.username)
                //router设置
                this.$router.push({
                  path: '/',
                  query: {username: res.data.username, sings: res.data.sings, songs: res.data.songs, baseclick: 0}
                })
              }else if(res.code === 202){
                setTimeout(() => {
                  this.$message({
                    message: "账号不存在！",
                    type: "error"
                  });
                  this.logining = false; //登陆操作完毕
                }, 400);
              }else if(res.code === 203){
                setTimeout(() => {
                  this.$message({
                    message: "密码错误！",
                    type: "error"
                  });
                  this.logining = false; //登陆操作完毕
                }, 400);
              }
            }, (err) => {
              console.log(err)
            })
          } else {
            console.log("error submit!!");
            return false;
          }
        });
      },
      // <!--免费注册页-->
      gotoLoginReg() {
        this.$router.push({
          path: "/"
        });
      },
      // <!--忘记密码页-->
      gotoLoginForget() {
        this.$router.push({
          path: "/LoginForget"
        });
      },
      // 验证手机号
      checkMobile(str) {
        let reg = /^[1][3,4,5,6,7,8,9][0-9]{9}$/;
        return reg.test(str);
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
  };
</script>

<style lang="scss" scoped>
  $white-bg-color: rgba(255,255,255,0.5);
  $btn-color: #409eff;

  .page {
    background: url("../assets/img/background0.jpeg");
    background-size: contain;
    position: absolute;
    width: 100%;
    height: 100%;
    font-size: 16px;
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 400;
    -webkit-font-smoothing: antialiased;
    .login-box {
      position: absolute;
      top: 45%;
      left: 50%;
      -webkit-transform: translate(-50%, -50%);
      transform: translate(-50%, -50%);
      display: block;
      width: 100%;
      max-width: 400px;
      background-color: $white-bg-color;
      margin: 0;
      padding: 15px 35px;
      box-sizing: border-box;
      // border: solid 1px #ddd;
      border-radius: 0.5em;
      font-family: "Source Sans Pro", sans-serif;
      .title {
        font-size: 20px;
        line-height: 50px;
        font-weight: bold;
        margin: 10px;
        text-align: center;
      }
      /deep/ .el-tabs__header {
        margin: 0 0 30px 0;
      }
      // /deep/ .el-tabs__item {
      //   font-size: 20px;
      //   text-align: center;
      // }
      /deep/ .el-tabs__nav-wrap::after {
        height: 0;
      }
      /deep/ #tab-first::after {
        content: "";
        position: absolute;
        right: 0;
        bottom: 0;
        width: 1px;
        height: 20px;
        background-color: #dcdfe6;
        margin: 8px 0;
        vertical-align: middle;
      }
      .code /deep/ .el-form-item__content {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      .code button {
        margin-left: 20px;
        width: 140px;
        text-align: center;
      }
      .el-form-item:last-child {
        margin-bottom: 6px;
      }
      .el-button--primary:focus {
        background: $btn-color;
        border-color: $btn-color;
        color: $white-bg-color;
      }
      /deep/ .el-input__suffix-inner {
        margin-right: 6px;
      }
    }
    .login {
      margin-top: -15px;
      font-size: 12px;
      cursor: pointer;
      text-align: left;
      .gotoRight {
        float: right;
        color: #999999;
        .hoverBlue{
          &:hover {
            color: $btn-color;
          }
        }
      }
    }
  }
</style>
