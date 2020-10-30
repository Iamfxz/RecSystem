import fetch from '../../axios/fetch'
// 推荐标签等相关数据
export const getMusicData = (getdata) => fetch('/api/index/home/', getdata, 'get')
// 主页分类
export const getCateData = () => fetch('/api/index/getCates/', '', 'get')
// 推荐模块
export const getRecommend = (recommend) => fetch('/api/index/rec/', recommend, 'get')
// 详细歌单列表模块
export const getPlaylist = (one_name) => fetch('/api/playlist/one/', one_name, 'get')
// 歌单搜索模块
export const getSearchPlaylist = (name) => fetch('/api/playlist/search/', name, 'get')
// 详细歌曲列表模块
export const getSongList = (one_name) => fetch('/api/song/one/', one_name, 'get')
// 歌曲搜索模块
export const getSearchSongList = (name) => fetch('/api/song/search/', name, 'get')
// 详细歌手模块
export const getSingList = (one_name) => fetch('/api/sing/one/', one_name, 'get')
// 歌手搜索模块
export const getSearchSingList = (name) => fetch('/api/sing/search/', name, 'get')
// 详细用户列表模块
export const getUserList = (one_name) => fetch('/api/user/one/', one_name, 'get')
// 歌曲搜索模块
export const getSearchUserList = (name) => fetch('/api/user/search/', name, 'get')
// 获取用户以及标签
export const getLogin = () => fetch('/api/index/login/', '', 'get')
// 登录
export const login = (loginInfo) => fetch('/api/index/login/', loginInfo, 'post')
// 短信登录
export const smsLogin = (loginInfo) => fetch('/api/user/sms/', loginInfo, 'post')
// 短信登录
export const smsValid = (validInfo) => fetch('/api/user/valid/', validInfo, 'post')
// 退出切换用户
export const layout = () => fetch('/api/index/switchuser/', '', 'get')
