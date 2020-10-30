/**
 *功能:全局功能函数
 */
exports.install = function (Vue, options) {
  // 时间格式化
  Vue.prototype.timeFormat = function (time) {
    if (!time) return false;
    if (time === '1970-01-01T00:00:00') return '暂无时间'
    let datetime = new Date(time);
    let y = datetime.getFullYear();
    let m = datetime.getMonth() + 1 < 10 ? '0' + parseInt(datetime.getMonth() + 1) : parseInt(datetime.getMonth() + 1);
    let d = datetime.getDate() < 10 ? '0' + datetime.getDate() : datetime.getDate();
    let h = datetime.getHours() < 10 ? '0' + datetime.getHours() : datetime.getHours();
    let mm = datetime.getMinutes() < 10 ? '0' + datetime.getMinutes() : datetime.getMinutes();
    let s = datetime.getSeconds() < 10 ? '0' + datetime.getSeconds() : datetime.getSeconds();
    return y + '年' + m + '月' + d + '日   ' + h + ':' + mm + ':' + s
  };
  // 获取URL中的参数,key=value,转化为字典result
  Vue.prototype.getUrlparams = function (url) {
    let urlArr = url.split('?');
    if (urlArr < 2) return false;
    let tmpArr = urlArr[1].split('&');
    let result = {};
    tmpArr.forEach(item => {
      let tmppar = item.split('=');
      result[tmppar[0]] = tmppar[1]
    });
    return result
  };
  // 处理歌词中的文本换行不匹配
  Vue.prototype.returnLine = function (str, reg, replacestr) {
    let re = new RegExp(reg, 'g');
    str = str.replace(re, replacestr);
    return str
  };
  // 数据加载缓冲
  Vue.prototype.loading = function (msg) {
    this.$layer.msg(msg, {
      title: '信息',
      time: 3600,
      shade: true,//是否显示遮罩
      shadeClose: false //点击遮罩是否关闭
    })
  };
  // 时间差计算
  // newtime - time <= efftime    -->正常
  Vue.prototype.deTime = function (time, newtime, efftime) {
    let t1 = new Date(time);
    let t2 = new Date(newtime);
    let detime = parseInt(t2 - t1) / 1000 / 3600;
    if (detime > efftime) {
      this.$children[0].$children[0].layout()
    }
  }
};
