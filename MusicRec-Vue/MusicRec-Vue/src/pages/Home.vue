<template>
  <div class="recommendContain">
    <div>
      <!-- 导航栏  -->
      <mheader :active="isActive" @onGetnews="getCateMusic"></mheader>
      <!--  搜索组件  -->
      <search-bar :active="isActive" @onSelectChange="selectChange"></search-bar>
    </div>
    <div v-if="isActive==='1'" class="mainContent">
      <div class="main_sign">
        <h3>歌单标签</h3>
        <ul class="lists">
          <li v-for="(item,index) in playlist.tags" :key="index" @click="getTagMusic(item+'+2')">{{item}}</li>
        </ul>
      </div>
      <div class="main_sign">
        <h3>歌曲标签</h3>
        <ul class="lists">
          <li v-for="(item,index) in song.tags" :key="index" @click="getTagMusic(item+'+3')">{{item}}</li>
        </ul>
      </div>
      <div class="main_sign">
        <h3>歌手标签</h3>
        <ul class="lists">
          <li v-for="(item,index) in sing.tags" :key="index" @click="getTagMusic(item+'+4')">{{item}}</li>
        </ul>
      </div>
    </div>
    <div v-if="isActive==='2'" class="mainContent">
      <div class="singCon singSongCon">
        <h3>歌单标签</h3>
        <ul class="signslists">
          <li :class="tag === 'all' ? 'oktag' : ''" @click="getTagMusic('all')">全部</li>
          <li :class="tag === item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">
            {{item}}
          </li>
          <li v-if="tags.length <=15" class="moretag" @click="getMoreTag()">更多 >></li>
        </ul>
        <div class="allsign">
          <ul class="relists">
            <li v-for="item in plays" :key="item.pl_id" class="relist singlists" @click="musicDesc(item.pl_id)">
              <el-image :key="item.pl_img_url" :src="item.pl_img_url"  alt="歌单封面">
                <div slot="placeholder" class="image-slot">
                  <span class="dot">加载中...</span>
                </div>
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
              <p class="recreater">{{item.pl_creator}}</p>
              <p class="rename">{{item.pl_name}}</p>
            </li>
          </ul>
        </div>
      </div>
      <div class="singCon singSong">
        <h3>歌单推荐</h3>
        <ul class="relists">
          <li v-for="item in replays" :key="item.pl_id" class="relist" @click="musicDesc(item.pl_id)">
            <el-image :src="item.pl_img_url" alt="歌单封面">
              <div slot="placeholder" class="image-slot">
                <span class="dot">加载中...</span>
              </div>
              <div slot="error" class="image-error">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
            <p class="recreater">{{item.pl_creator}}</p>
            <p class="rename">{{item.pl_name}}</p>
          </li>
          <el-button type="warning" round @click="getCateMusic({'cateid': '6','rectag': '1'})">更多 >></el-button>
        </ul>
      </div>
    </div>
    <div v-if="isActive==='3'" class="mainContent">
      <div class="singCon singSongCon">
        <h3>歌曲标签</h3>
        <ul class="signslists">
          <li :class="tag === 'all' ? 'oktag' : ''" @click="getTagMusic('all')">全部</li>
          <li :class="tag === item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">
            {{item}}
          </li>
          <li v-if="tags.length <=15" class="moretag" @click="getMoreTag()">更多 >></li>
        </ul>
        <div class="allsign">
          <el-table class="relists" :modal-append-to-body="true"
            :data="songs" :row-key="songs.song_id" @row-click="clickSong"
             stripe>
            <el-table-column fixed="left"  type="index" label="序号" width="50"></el-table-column>
            <el-table-column class="onename" prop="song_name" label="歌曲名字"></el-table-column>
            <el-table-column sortable fixed="right" class="onetime" prop="song_publish_time" label="出版时间"></el-table-column>
          </el-table>
<!--          <ul class="relists">-->
<!--            <li v-for="item in songs" :key="item.song_id" class="onelist" @click="musicDesc(item.song_id)">-->
<!--              <p class="onename">{{item.song_name}}</p>-->
<!--              <p class="onetime">{{item.song_publish_time}}</p>-->
<!--            </li>-->
<!--          </ul>-->
        </div>
      </div>
      <div class="singCon singSong">
        <h3>歌曲推荐</h3>
        <ul class="relists">
          <li v-for="item in replays" :key="item.song_id" class="onelist" @click="musicDesc(item.song_id)">
            <p class="onename">{{item.song_name}}</p>
            <p class="onetime">{{(item.song_publish_time|| '').slice(0,8)}}</p>
          </li>
          <el-button type="warning" round @click="getCateMusic({'cateid': '6','rectag': '2'})">更多 >></el-button>
        </ul>
      </div>
    </div>
    <div v-if="isActive==='4'" class="mainContent">
      <div class="singCon singSongCon">
        <h3>歌手标签</h3>
        <ul class="signslists">
          <li :class="tag === 'all' ? 'oktag' : ''" @click="getTagMusic('all')">全部</li>
          <li :class="tag === item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">
            {{item}}
          </li>
          <li v-if="tags.length <=15" class="moretag" @click="getMoreTag()">更多 >></li>
        </ul>
        <div class="allsign">
          <ul class="relists">
            <li v-for="item in sings" :key="item.sing_id" class="relist singlists" @click="musicDesc(item.sing_id)">
              <el-image :src="item.sing_url" alt="歌手封面">
                <div slot="placeholder" class="image-slot">
                  <span class="dot">加载中...</span>
                </div>
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
              <p class="recreater"></p>
              <p class="rename">{{item.sing_name}}</p>
            </li>
          </ul>
        </div>
      </div>
      <div class="singCon singSong">
        <h3>歌手推荐</h3>
        <ul class="relists">
          <li v-for="item in replays" :key="item.sing_id" class="relist" @click="musicDesc(item.sing_id)">
            <el-image :src="item.sing_url" alt="歌手封面">
              <div slot="placeholder" class="image-slot">
                <span class="dot">加载中...</span>
              </div>
              <div slot="error" class="image-error">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
            <p class="recreater"></p>
            <p class="rename">{{item.sing_name}}</p>
          </li>
          <el-button type="warning" round @click="getCateMusic({'cateid': '6','rectag': '3'})">更多 >></el-button>
        </ul>
      </div>
    </div>
    <div v-if="isActive==='5'" class="mainContent">
      <div class="singCon singSongCon">
        <h3>用户标签</h3>
        <ul class="signslists">
          <li :class="tag === 'all' ? 'oktag' : ''" @click="getTagMusic('all')">全部</li>
          <li :class="tag === item ? 'oktag' : ''" v-for="(item,index) in tags" :key="index" @click="getTagMusic(item)">
            {{item}}
          </li>
          <li v-if="tags.length <=15" class="moretag" @click="getMoreTag()">更多 >></li>
        </ul>
        <div class="allsign">
          <ul class="relists">
            <li v-for="item in users" :key="item.u_id" class="relist singlists" @click="musicDesc(item.u_id)">
              <el-image :src="item.u_img_url" alt="用户封面" style="width: 100px;height: 100px">
                <div slot="placeholder" class="image-slot">
                  <span class="dot">加载中...</span>
                </div>
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
              <p class="recreater"></p>
              <p class="rename">{{item.u_name}}</p>
            </li>
          </ul>
        </div>
      </div>
      <div class="singCon singSong">
        <h3>用户推荐</h3>
        <ul class="relists">
          <li v-for="item in replays" :key="item.u_id" class="relist" @click="musicDesc(item.u_id)">
            <el-image :src="item.u_img_url" alt="用户封面" style="width: 100px;height: 100px">
              <div slot="placeholder" class="image-slot">
                <span class="dot">加载中...</span>
              </div>
              <div slot="error" class="image-error">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
            <p class="recreater"></p>
            <p class="rename">{{item.u_name}}</p>
          </li>
        </ul>
      </div>
    </div>
    <div v-if="isActive==='6'" class="mainContent">
      <ul class="recnav">
        <li :class="rectag==='0'?'active':''" @click="getCateMusic({'cateid': '6', 'rectag': '0'})">总推荐榜</li>
        <li :class="rectag==='1'?'active':''" @click="getCateMusic({'cateid': '6','rectag': '1'})">歌单</li>
        <li :class="rectag==='2'?'active':''" @click="getCateMusic({'cateid': '6','rectag': '2'})">歌曲</li>
        <li :class="rectag==='3'?'active':''" @click="getCateMusic({'cateid': '6','rectag': '3'})">歌手</li>
      </ul>
      <div class="main_sign" v-if="rectag==='0'">
        <h3>推荐歌单榜<small style="font-size: 10px">(总推荐榜显示前20)</small></h3>
        <ul class="lists musiclis">
          <li v-for="(item,index) in tmpplay" :key="index" @click="musicDesc(item.pl_id+'+2')">
            <b>
              <img :src="item.pl_img_url" alt="歌单封面" style="padding: 20px"/>
            </b>
            <span class="singer">
              歌单名：{{item.pl_name}}
              <br>
              创建者：{{item.pl_creator}}
            </span>
          </li>
        </ul>
      </div>
      <div class="main_sign" v-if="rectag==='0'">
        <h3>推荐歌曲榜<small style="font-size: 10px">(总推荐榜显示前20)</small></h3>
        <ul class="lists musiclis">
          <li v-for="(item,index) in tmpsong" :key="index" @click="musicDesc(item.song_id+'+3')">
            <b>
              <span class="songname">
                歌名：{{item.song_name}}
                <br>
                出版时间：{{item.song_publish_time}}</span>
            </b>
          </li>
        </ul>
      </div>
      <div class="main_sign" v-if="rectag==='0'">
        <h3>推荐歌手榜<small style="font-size: 10px">(总推荐榜显示前20)</small></h3>
        <ul class="lists musiclis">
          <li v-for="(item,index) in tmpsing" :key="index" @click="musicDesc(item.sing_id+'+4')">
            <b>
              <img :src="item.sing_url" alt="歌单封面" style="padding: 20px"/>
            </b>
            <span class="singer">
              歌手:{{item.sing_name}}
              <br>
              歌曲数：{{item.sing_music_num}}
            </span>
          </li>
        </ul>
      </div>
      <div class="main_sign singlemainsign" v-if="rectag==='1'">
        <ul class="lists musiclis">
          <li>
            <b class="icon">
              图标
            </b>
            <span>歌单名称</span>
            <span>歌单创建者</span>
            <span>歌单推荐值</span>
            <span>歌单创建时间</span>
          </li>
          <li v-for="(item,index) in sortplaylist" :key="index" @click="musicDesc(item.pl_id+'+2')">
            <b>
              <img :src="item.pl_img_url" alt="推荐歌单封面"/>
            </b>
            <span>{{item.pl_name}}</span>
            <span>{{item.pl_creator}}</span>
            <span>{{item.score}}</span>
            <span>{{item.pl_create_time}}</span>
          </li>
        </ul>
      </div>
      <div class="main_sign singlemainsign" v-if="rectag ==='2'">
        <ul class="lists musiclis">
          <li>
            <span class="songname">歌曲名称</span>
            <span class="songname">歌曲演唱者</span>
            <span class="songname">歌曲推荐值</span>
            <span class="songname">歌曲创建时间</span>
          </li>
          <li v-for="(item,index) in sortsong" :key="index" @click="musicDesc(item.song_id+'+3')">
            <span class="songname">{{item.song_name}}</span>
            <span class="songtime">{{item.song_singer_name}}</span>
            <span class="songname">{{item.score}}</span>
            <span class="songtime">{{item.song_publish_time}}</span>
          </li>
        </ul>
      </div>
      <div class="main_sign singlemainsign" v-if="rectag ==='3'">
        <ul class="lists musiclis">
          <li>
            <b class="icon">头像</b>
            <span class="singer">歌手名称</span>
            <span class="singer">专辑数</span>
            <span class="singer">歌曲数</span>
            <span class="singer">MV数</span>
            <span class="singer">歌手推荐值</span>
          </li>
          <li v-for="(item,index) in sortsing" :key="index" @click="musicDesc(item.sing_id+'+4')">
            <b>
              <img :src="item.sing_url" alt="推荐歌手封面"/>
            </b>
            <span class="singer">{{item.sing_name}}</span>
            <span class="singer">{{item.sing_album_num}}</span>
            <span class="singer">{{item.sing_music_num}}</span>
            <span class="singer">{{item.sing_mv_num}}</span>
            <span class="singer">{{item.score}}</span>
          </li>
        </ul>
      </div>
    </div>
    <div v-if="isActive==='7'" class="mainContent">
      <ul class="liscan">
        <li>
          <span>时间</span>
          <span>操作</span>
        </li>
        <li v-for="(item,index) in datas" :key="index">
          <span>{{item.time}}</span>
          <span>{{item.desc}}<b v-if="item.name">【{{item.name}}】</b> </span>
        </li>
      </ul>
    </div>
    <div class="rightpag">
      <mpagnation v-if="total>display && 1<isActive && isActive<6"
                  :total="total" :display="display" :current-page='current' :refresh='refresh'
                  @pageChange="pageChange" @pageSizeChange="pageSizeChange" style="padding: 30px">
      </mpagnation>
    </div>
  </div>
</template>

<script>
  import {getMusicData, getRecommend} from '@/assets/js/api'
  import newheader from '@/components/newHeader.vue'
  import pagnation from '@/components/pagnation2'
  import SearchBar from "@/components/searchBar";

  export default {
    name: 'HelloWorld',
    data() {
      return {
        isActive: '1',
        newsData: {},
        tmptags: [],
        playlist: {},
        song: {},
        sing: {},
        // 歌单相关
        tags: [],
        plays: [{
          pl_img_url: 'https://img.icons8.com/carbon-copy/100/000000/picture.png',
          pl_id: '',
          pl_creator: '',
          pl_name: ''
        }],
        // 推荐内容，可能为歌曲，用户，歌单，歌手
        replays: [{
          sing_id: '',
          sing_url: '',
          sing_name: '',
          u_id: '',
          u_img_url: '',
          u_name: '',
          pl_id: '',
          pl_name: '',
          pl_creator: '',
          pl_img_url: '',
          song_id: '',
          song_name: '',
          song_publish_time: ''
        }],
        // 歌曲相关
        songs: [{
          song_id: '',
          song_name: '',
          song_publish_time: '',
          song_lysic: ''
        }],
        // 歌手相关
        sings: [{
          sing_id: '',
          sing_name: '',
          sing_url: 'https://img.icons8.com/carbon-copy/100/000000/picture.png',
          sing_album_num: '',
          sing_music_num: '',
          sing_mv_num: '',
          score: ''
        }],
        // 用户相关
        users: [],
        // 分页相关
        total: 0, // 总条数
        current: 1, // 当前激活页
        display: 30, // 每页显示多少条
        refresh: false, // 是否刷新（第一页激活）有搜索时需要
        tag: 'all',
        // 足迹
        datas: [],
        // 排行榜
        sortplaylist: [],
        sortsong: [],
        sortsing: [],
        tmpplay: [],
        tmpsing: [],
        tmpsong: [],
        // 排行榜分榜标示
        rectag: '0'
      }
    },
    components: {
      SearchBar,
      'mheader': newheader,
      'mpagnation': pagnation
    },
    methods: {
      clickSong: function(row){
        this.musicDesc(row.song_id)
      },
      getCateMusic: function (option) {
        // 页面id，对照表在数据库中
        let cateId = option.cateid;
        // console.log(cateId)
        let getdata = {};
        //默认tag=all
        if (!option.tag) {
          option.tag = 'all'
        } else {
          this.tag = option.tag;
        }
        //默认page=1
        if (!option.page) {
          option.page = 1
        }else {
          this.current = option.page
        }
        //pagesize和display绑定
        if (!option.pagesize) {
          option.pagesize = this.display
        }else {
          this.display = option.pagesize
        }
        //默认rectag=0
        if (!option.rectag) {
          this.rectag = '0'
        } else {
          this.rectag = option.rectag
        }
        //加载不同的页面
        if (cateId === '1') {
          this.loading('加载中...首次加载需要较多时间');
          if (option.sings) {
            getdata.sings = option.sings;
            getdata.songs = option.songs;
            getdata.baseclick = option.baseclick
          } else {
            getdata.sings = '';
            getdata.songs = '';
            getdata.baseclick = option.baseclick
          }
          if (option.baseclick === '0') {
            getdata.baseclick = 0
          } else {
            getdata.baseclick = 1
          }
          getdata.cateid = '1';
          this.isActive = cateId + '';
          getdata.username = this.$store.state.vuexLogin.userName;
          getMusicData(getdata).then((res) => {
            this.$layer.closeAll();
            const {code} = res;
            if (code) {
              this.playlist = res.data.playlist;
              this.sing = res.data.sing;
              this.song = res.data.song
            } else {
              this.$children[0].layout()
            }
          }, (err) => {
            this.$message({
              message: '小主稍等，紧急恢复中...' + err.data,
              type: "error"
            });
          })
        }
        else {
          this.loading('加载中...首次加载需要较多时间');
          if (cateId) {
            getdata.cateid = cateId;
            getdata.sings = '';
            getdata.songs = '';
            getdata.baseclick = 1;
            getdata.tag = option.tag;
            getdata.page = option.page;
            getdata.pagesize = option.pagesize;
            this.isActive = cateId + ''
          }
          getdata.username = this.$store.state.vuexLogin.userName;
          let recommendData = {
            'cateid': cateId,
            'username': getdata.username
          };
          if (recommendData.cateid === '2' || recommendData.cateid === '3' || recommendData.cateid === '4' || recommendData.cateid === '5') {
            getRecommend(recommendData).then((res) => {
              if (res.code === 1) {
                if (recommendData.cateid === '2') {
                  this.replays = res.data.recplaylist
                } else if (recommendData.cateid === '3') {
                  res.data.songs.forEach((item) => {
                    item.song_publish_time = this.timeFormat(item.song_publish_time)
                  });
                  this.replays = res.data.songs
                } else if (recommendData.cateid === '4') {
                  this.replays = res.data.sings
                } else if (recommendData.cateid === '5') {
                  this.replays = res.data.users
                }
              }
            })
          }
          let allRec = (cateId === '6' && this.rectag === '0' && this.sortplaylist.length > 0 && this.sortsing.length > 0 && this.sortsong.length > 0);
          let playRec = (cateId === '6' && this.rectag === '1' && this.sortplaylist.length > 0);
          let songRec = (cateId === '6' && this.rectag === '2' && this.sortsong.length > 0);
          let singRec = (cateId === '6' && this.rectag === '3' && this.sortsing.length > 0);
          if (!(allRec || playRec || singRec || songRec)) {
            getMusicData(getdata).then((res) => {
              this.$layer.closeAll();
              if (!res.code) {
                this.$children[0].layout()
              } else {
                if (res.data.tags) {
                  this.tags = res.data.tags.slice(0, 15);
                  this.tmptags = res.data.tags
                }
                if (getdata.cateid === '2') {
                  this.plays = res.data.playlist;
                  this.total = res.data.total
                } else if (getdata.cateid === '3') {
                  res.data.songs.forEach((item) => {
                    item.song_publish_time = this.timeFormat(item.song_publish_time)
                  });
                  this.songs = res.data.songs;
                  this.total = res.data.total
                } else if (getdata.cateid === '4') {
                  this.sings = res.data.sings;
                  this.total = res.data.total
                } else if (getdata.cateid === '5') {
                  this.users = res.data.sings;
                  this.total = res.data.total
                } else if (getdata.cateid === '6') {
                  this.total = 1;
                  res.data.song.forEach((item) => {
                    item.song_publish_time = this.timeFormat(item.song_publish_time)
                  });
                  res.data.playlist.forEach((item) => {
                    item.pl_create_time = this.timeFormat(item.pl_create_time)
                  });
                  this.tmpplay = res.data.playlist.slice(0, 20);
                  this.tmpsing = res.data.sing.slice(0, 20);
                  this.tmpsong = res.data.song.slice(0, 20);
                  if (this.rectag === '1') {
                    this.sortplaylist = res.data.playlist
                  } else if (this.rectag === '2') {
                    this.sortsong = res.data.song
                  } else if (this.rectag === '3') {
                    this.sortsing = res.data.sing
                  } else {
                    this.sortplaylist = res.data.playlist;
                    this.sortsing = res.data.sing;
                    this.sortsong = res.data.song
                  }
                } else if (getdata.cateid === '7') {
                  res.data.click.forEach((item) => {
                    item.time = this.timeFormat(item.time)
                  });
                  this.total = res.data.total;
                  this.datas = res.data.click
                }
              }
            }, (err) => {
              this.$message({
                message: '小主稍等，紧急恢复中...',
                type: "error"
              });
            })
          } else {
            this.$layer.closeAll();
            return 0
          }
        }
      },
      musicDesc: function (id) {
        if (id.indexOf('+') > -1) {
          let tmpId = id.split('+');
          id = tmpId[0];
          this.isActive = tmpId[1];
          console.log(tmpId[1])
        }
        this.$router.push({
          name: 'one',
          query: {id: id, cateid: this.isActive}
        })
      },
      // 分页
      pageChange: function (currentPage) {
        console.log(currentPage)
        this.tags = this.tags.slice(0, 15);
        this.refresh = false;
        this.current = currentPage;
        // 滚到顶部 注意不在window而在document.documentElement
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
        // 获取列表 可根据后端要求改变page的方式
        this.getCateMusic({'page': this.current, 'cateid': this.isActive, 'tag': this.tag, 'pagesize': this.display})
      },
      // 每页大小改变
      pageSizeChange: function (pageSize) {
        let changedPage = Math.ceil((this.current * this.display) / pageSize)
        this.display = pageSize
        if(this.current === 1){
          changedPage = 1
        }else{
          if(changedPage * pageSize > this.total){
            changedPage = Math.ceil(this.total/pageSize)
          }
        }
        this.pageChange(changedPage)
        // console.log(changedPage)
      },
      // tag获取
      getTagMusic: function (nowtag) {
        this.tags = this.tags.slice(0, 15);
        this.refresh = true;
        this.tag = nowtag;
        this.current = 1
        if (nowtag.indexOf('+') > -1) {
          let temTag = nowtag.split('+');
          this.tag = temTag[0];
          this.isActive = temTag[1]
        }
        this.getCateMusic({'cateid': this.isActive, 'tag': this.tag, 'pagesize':this.display})
      },
      // 获取更多tag
      getMoreTag: function () {
        this.tags = this.tmptags
      },
      // 调用搜索结果加载页面
      selectChange: function (search_id) {
        // console.log(res)
        this.musicDesc(search_id)
      }
    },
    mounted() {
      // this.getCateMusic({'cateid': '2'})
      let sings = this.$route.query.sings;
      let songs = this.$route.query.songs;
      let baseClick = this.$route.query.baseclick + '';
      if (this.$route.params.cateid) {
        this.getCateMusic({'cateid': this.$route.params.cateid})
      } else {
        this.getCateMusic({'cateid': '1', 'sings': sings, 'songs': songs, 'baseclick': baseClick})
      }
    }
  }
</script>
<style lang="less" scoped>
  @baseColor: #20a0ff;
  #ellies(@n) {
    overflow: hidden;
    text-overflow: ellipsis;
    -webkit-line-clamp: @n;
    -webkit-box-orient: vertical;
    white-space: nowrap;
  }

  .recommendContain {
    width: 100%;
    padding: 2% 8% 0;
    min-height: 100%;
    background: url("../assets/img/background2.jpg");
    position: absolute;
    box-sizing: border-box;

    .dot {
      size: 20px;
      margin: auto;
      padding: 10px;
    }

    .mainContent {
      width: 100%;
      display: flex;
      box-sizing: border-box;
      justify-content: space-around;

      .main_sign {
        width: 32%;
        box-sizing: border-box;
        padding: 10px;
        border: 1px solid #ddd;
        margin: 15px 6px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        min-height: 300px;

        .lists {
          margin-top: 10px;

          li {
            padding: 6px 8px;
            border-radius: 4px;
            color: #333;
            font-size: 16px;
            width: auto;
            display: inline-block;
            border: 1px solid #ddd;
            cursor: pointer;
            margin: 5px;
          }

          li:first-child {
            color: orange;
            border: 1px solid orange;
          }

          li:nth-child(2) {
            color: red;
            border: 1px solid red;
          }

          li:nth-child(3) {
            color: coral;
            border: 1px solid coral;
          }

          li:nth-child(4) {
            color: chocolate;
            border: 1px solid chocolate;
          }

          li:hover {
            color: @baseColor;
            border: 1px solid @baseColor;
          }
        }

        .musiclis {
          li {
            width: 100%;
            box-sizing: border-box;

            b {
              img {
                width: 50px;
                height: 50px;
                border-radius: 25px;
              }
            }

            span {
              display: inline-block;
              width: 30%;
              #ellies(1);
              vertical-align: middle;
              font-size: 12px;
            }

            span:last-child {
              font-size: 14px;
              width: 43%;
              float: right;
              line-height: 50px;
            }

            span.songname {
              font-size: 14px;
              width: 100%;
            }

            span.singer {
              width: 65%;
            }
          }
        }
      }

      .singlemainsign {
        width: 100%;

        .lists {
          li {
            display: flex;
            justify-content: space-around;
            align-items: center;

            .icon {
              width: 140px;
            }

            span {
              margin-left: 15px;
            }
          }

          li:first-child {
            color: #666;
            border: none;
          }

          li:first-child:hover {
            color: #666;
            border: none;
          }
        }
      }

      .singCon {
        box-sizing: border-box;
        padding: 10px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        min-height: 500px;
        margin-top: 15px;
        margin-bottom: 15px;

        .signslists {
          margin-top: 10px;

          li {
            display: inline-block;
            border: 1px solid #ddd;
            box-sizing: border-box;
            padding: 6px;
            border-radius: 4px;
            margin: 5px;
            text-align: center;
            cursor: pointer;
            font-size: 12px;

            &:hover {
              color: @baseColor;
              border: 1px solid @baseColor;
            }
          }

          .oktag {
            color: @baseColor;
            border: 1px solid @baseColor;
          }

          .moretag {
            color: orange;
            border: 1px solid orange;
          }
        }

        .relists {
          margin-top: 20px;
          display: flex;
          background: rgba(255,255,255,0.3);
          justify-content: space-around;
          flex-wrap: wrap;

          .more {
            padding: 5px;
            border: 1px solid orange;
            color: #fff;
            background: orange;
            text-align: center;
            width: 120px;
            border-radius: 3px;
            height: 30px;
            line-height: 30px;
            margin-top: 15px;
            cursor: pointer;
          }

          .relist {
            width: 30%;
            box-sizing: border-box;
            padding: 5px;
            color: #333;
            cursor: pointer;
            margin-bottom: 15px;

            &:hover {
              color: @baseColor;
            }

            .recreater {
              font-size: 12px;
              color: #666;
              line-height: 14px;
              margin-bottom: 5px;
              margin-top: 5px;
              #ellies(1)
            }

            .rename {
              font-size: 14px;
              line-height: 16px;
              #ellies(1)
            }

            img {
              width: 100%;
            }
          }

          .singlists {
            width: 20%;
          }

          .onelist {
            width: 100%;
            color: #666;
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
            cursor: pointer;

            &:hover {
              color: @baseColor;
            }
            .onename{
              width: 70%;
              #ellies(1);
              display: inline-block;
              box-sizing: border-box;
              padding: 0 10px;
            }
            .onetime {
              width: 30%;
              #ellies(1);
              display: inline-block;
              box-sizing: border-box;
              padding: 0 10px;
            }
          }
        }
      }

      .singSongCon {
        flex: 2;
        margin-right: 15px;
      }

      .singSong {
        flex: 1;
        margin-left: 15px;
        min-width: 30%;
      }

      .liscan {
        width: 100%;

        li {
          width: 100%;
          color: #666;
          font-size: 14px;
          display: block;
          margin: 20px;

          span {
            display: inline-block;
            width: 40%;
          }
        }

        li:first-child {
          color: #000;
        }
      }

      .recnav {
        width: 10%;
        min-width: 120px;
        padding-left: 20px;
        margin-top: 20px;
        box-sizing: border-box;

        li {
          width: 100%;
          height: 30px;
          box-sizing: border-box;
          line-height: 30px;
          padding-left: 20px;
          color: #666;
          cursor: pointer;
        }

        .active {
          background: #eee;
          box-shadow: 10px 0px 10px 1px @baseColor;
        }
      }
    }
  }
</style>
