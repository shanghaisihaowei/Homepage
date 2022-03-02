<template>
  <div>
    <img @click="goTo(bannerUrl[0])" :src="bannerImgUrl[0]" alt="" style="max-width: 400px">
  </div>
  <div style="padding-bottom: 50px">
    <q-input v-model="pagelocation" style="display:none"/>
    <!--    搜索框-->
    <q-card class="row q-pa-md my-card shadow-0" style="padding-bottom: 0">
      <div class="col-12">
        <q-input
          dense
          outlined
          square
          placeholder="Search"
          class="bg-white"
          style="padding: 0"
          v-model="searchword"
          @keyup.enter="getsearchList()"
        >
          <template v-slot:after>
            <q-btn
              color="primary"
              icon="search"
              unelevated
              @click="getsearchList ()"/>
          </template>
        </q-input>
      </div>
    </q-card>
    <!--                文章列表-->
    <q-card v-for="(item, index) in allArtInfos" :key="index" square class="col-12 my-card shadow-0"
            style="border-bottom: 1px #dcdcdc solid;padding: 0">
      <div v-if="!item.top || item.isTop">
      <div @click.stop="
                this.$router.push({
                  path: `/community/mobile/DVadminDetail/${item.id}`
                })
              ">
      <q-card-section>
        <div class="card_tol Wrap_two">
          <span
            v-if="item.isTop"
            class="col-2"
            style=" font-size: 14px;
                  background-color: #116fec;
                  color: white;
                  padding: 1px 7px 0 7px;
                  border-radius: 4px;
                "
          >
              {{ $t("community.top") }}
            </span>
          <span
            style="cursor: pointer"
            class="card_tol Wrap_two"
          >
            {{ item.title }}
          </span>
        </div>
      </q-card-section>

      <q-card-section style="margin-top: -28px" horizontal>
        <q-card-section v-show="item.cover != null">
          <q-img
            :src=item.cover
            style="width: 180px;
              height: 110px;border-radius: 4px;"/>
        </q-card-section>

        <q-card-section v-html="item.intro" class="article_text"></q-card-section>
      </q-card-section>
      </div>
      <q-card-actions style="margin-top: -10px">
        <div
          class=" flex flex-center"
          style="
              font-size: 14px;
              font-weight: 400;
              color: #999999;
              margin-left: 1%;
            "
        >
          <q-img
            style="margin-top: -2px; margin-right: 10px" width="12px" height="14px"
            src="statics/author.svg"
          />
          <span>
              {{ item.author_icon.author }}
            </span>
        </div>
        <div
          class="flex flex-center"
          style="
              font-size: 14px;
              font-weight: 400;
              color: #999999;
              margin-left: 1%;
            "
        >
            <span style="font-size: 12px !important;">
              {{ $t('community.push_time') }}
               {{ item.updata_time }}
            </span>
        </div>
      </q-card-actions>
      </div>
    </q-card>
    <div class="flex flex-center" v-show="pathname !== null">
      <q-spinner-dots
        color="primary"
        size="xl"
      />
    </div>
    <div class="flex flex-center" v-show="pathname === null">
      <q-btn flat>{{ $t('notice.nomoredata') }}</q-btn>
    </div>
  </div>
</template>
<script>
import {defineComponent} from 'vue';
import {get, getauth} from "boot/axios";
import {throttle, createMetaMixin, openURL} from 'quasar'
import jwtDecode from "jwt-decode";

export default defineComponent({
  data() {
    return {
      title: '',
      meta: {},
      allArtInfos: [],
      pathname: '/article/api/v1/Browse/?community_type=1',
      requestcount: 0,
      next_msg: '',
      icon: '',
      searchword: '',
      sortordOptions: [
        this.$t("community.newest"),
        this.$t("community.hottest"),
      ],
      sortordVal: this.$t("community.newest"),
      bannerImgUrl: [],
      bannerUrl: []
    }
  },
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.title,
        meta: this.meta,
      };
    }),
  ],
  computed: {
    isLogin() {
      return this.$store.state.bbsChange.isLogin;
    },
    user_info() {
      return this.$store.state.bbsChange.user_info;
    },
    getmore() {
      return this.$store.state.getmore.getmore;
    },
    pagelocation() {
      var _this = this
      if (this.pagelocation < 0.99) {
        _this.requestcount = 0
      } else {
        _this.requestcount = 1
      }
      if (this.pagelocation >= 0.99 && _this.pathname !== null && _this.requestcount === 1) {
        _this.getList()
      }
      return this.$store.state.pagelocation.pagelocation
    }
  },
  methods: {
    goTo(e) {
      openURL(e)
    },
    getList() {
      var _this = this
      if (_this.pathname !== null) {
        get(_this.pathname)
          .then((res) => {
            _this.pathname = res.result.next
            res.result.results.forEach(item => {
              _this.allArtInfos.push(item)
            })
            _this.getTopArticle()
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: "close",
              color: "negative",
            });
          });
      }
    },
    getsearchList() {
      var _this = this
      _this.pathname = '/article/api/v1/Browse/?community_type=1'
      if (_this.pathname !== null) {
        get(_this.pathname + '&title__contains=' + _this.searchword)
          .then((res) => {
            _this.allArtInfos = []
            _this.pathname = res.result.next
            res.result.results.forEach(item => {
              if (item.top) {
                item.isTop = true
              }
              _this.allArtInfos.push(item)
            })
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: "close",
              color: "negative",
            });
          });
      }
    },
    getTopArticle() {
      get("article/api/v1/topwms/").then((res) => {
        res.result.forEach((item) => {
          item.isTop = true;
          this.allArtInfos.unshift(item);
        });
      });
    },
    // 跳转到修改信息页面
    tochangMsg() {
      var _this = this
      _this.$store.dispatch('bbsChange/isIndexMenu', false)
      _this.$router.push({name: 'changePsd'})
    },
    // 获取广告位信息
    getbanner() {
      var _this = this
      get('resp/api/v1/mobile_banner/?community=1').then(res => {
        res.forEach((item,index) =>{
          _this.bannerImgUrl[index] = item.image
          _this.bannerUrl[index] = item.link
        })
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    }
  },
  created() {
    var _this = this
    if (_this.$q.cookies.get('lang') === 'zh-hans') {
      _this.title = 'GreaterWMS - 开源社区'
      _this.meta = {
        description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
        keywords: {name: 'keywords', content: '聚商汇WMS,开源仓库管理系统,仓库管理系统,wms,仓库管理软件,仓库管理,GreaterWMS, greaterwms'},
        equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
        ogTitle: {
          property: 'og:title',
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`
          }
        }
      }
    } else {
      _this.title = 'GreaterWMS - Community'
      _this.meta = {
        description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
        keywords: {
          name: 'keywords',
          content: 'GreaterWMS - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms'
        },
        equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
        ogTitle: {
          property: 'og:title',
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`
          }
        }
      }
    }
  },
  mounted() {
    var _this = this;
    _this.getbanner()
    _this.getList = throttle(this.getList, 1000)
    _this.getList()
    this.$store.dispatch("bbsChange/mobileLogo", 'statics/DV_logo_w.svg');
    this.$store.dispatch("bbsChange/titletype", 'DVAdmin');
  }
});
</script>
<style scoped lang="sass">
.article_text
  width: 100%
  font-size: 13px
  font-weight: 400
  color: #666666
  letter-spacing: 1px
  word-wrap: break-word

.card_tol
  font-size: 15px !important
  font-weight: 600
  color: #333333
  letter-spacing: 1px
  word-wrap: break-word

.Wrap_two
  overflow: hidden
  text-overflow: ellipsis
  display: -webkit-box
  -webkit-box-orient: vertical
  -webkit-line-clamp: 2

.wrap_neo
  overflow: hidden
  text-overflow: ellipsis
  display: -webkit-box
  -webkit-box-orient: vertical
  -webkit-line-clamp: 1
  line-height: 18px
</style>
