/*
*功能：
*  同一状态管理
*  this.$store.state.vuexLogin.userName //变量全局访问
*  this.$store.dispatch('login/chooseUser') //方法全局访问
*/
//全局存储信息
const state = {
  isLogin: false,
  userName: ''
}
//自定义触发mutations里函数的方法，context与store 实例具有相同方法和属性
const actions = {
  login (context, loginState) {
    context.commit('alterLogin', loginState)
  },
  chooseUser (context, newName) {
    context.commit('alterUser', newName)
  }
}
//实时监听数据的最新状态
const getters = {
  getLogin (state) {
    if (!state.isLogin) {
      state.isLogin = localStorage.getItem('islogin')
    }
    return state.isLogin
  },
  getName (state) {
    if (!state.userName) {
      state.userName = localStorage.getItem('username')
    }
    return state.userName
  }
}
//mutations里面可以放改变state的初始值的方法
const mutations = {
  alterLogin (state, loginState) {
    if (loginState) {
      localStorage.setItem('islogin', true)
    } else {
      localStorage.removeItem('islogin')
    }
    state.isLogin = loginState
  },
  alterUser (state, newName) {
    if (newName) {
      localStorage.setItem('username', newName)
    } else {
      localStorage.removeItem('username')
    }
    state.userName = newName
  }
}

export default{
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
