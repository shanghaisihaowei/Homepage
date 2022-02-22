<template>
  <div>
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
      <div @click.stop="
                this.$router.push({
                  path: `/community/mobile/GreaterWMSDetail/${item.id}`
                });setid(item.id)
              ">
      <q-card-section>
        <div class="my-font card_tol Wrap_two">
          <a
            style="cursor: pointer"
            class="my-font card_tol Wrap_two"
          >
            {{ item.title }}
          </a>
        </div>
      </q-card-section>

      <q-card-section style="margin-top: -28px" horizontal>
        <q-card-section v-show="item.cover != null">
          <q-img
            :src=item.cover
            style="width: 180px;
              height: 110px;border-radius: 4px;"/>
        </q-card-section>

        <q-card-section v-html="item.intro" class="article_text my-font"></q-card-section>
      </q-card-section>
      </div>

      <q-card-actions style="margin-top: -10px">
        <div
          class="my-font flex flex-center"
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
          class="my-font flex flex-center"
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
import {throttle, createMetaMixin} from 'quasar'
import jwtDecode from "jwt-decode";

export default defineComponent({
  data() {
    return {
      title: '',
      meta: {},
      allArtInfos: [],
      pathname: '/article/api/v1/Browse/?community_type=0',
      requestcount: 0,
      next_msg: '',
      icon: '',
      searchword: '',
      sortordOptions: [
        this.$t("community.newest"),
        this.$t("community.hottest"),
      ],
      sortordVal: this.$t("community.newest"),
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
    getList() {
      var _this = this
      if (_this.pathname !== null) {
        get(_this.pathname)
          .then((res) => {
            _this.pathname = res.result.next
            res.result.results.forEach(item => {
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
    getsearchList() {
      var _this = this
      _this.pathname = '/article/api/v1/Browse/?community_type=0'
      if (_this.pathname !== null) {
        get(_this.pathname + '&title__contains=' + _this.searchword)
          .then((res) => {
            _this.allArtInfos = []
            _this.pathname = res.result.next
            res.result.results.forEach(item => {
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
    setid(id) {
      var _this = this
      _this.$q.cookies.set('articleId', id)
    },
    // 跳转到修改信息页面
    tochangMsg() {
      var _this = this
      _this.$store.dispatch('bbsChange/isIndexMenu', false)
      _this.$router.push({name: 'changePsd'})
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
    if (_this.$q.cookies.has('token')) {
      let userinfoStr = jwtDecode(_this.$q.cookies.get("token"));
      _this.icon = window.g.BaseUrl + userinfoStr.icon
    } else {
    }
    _this.allArtInfos = []
    _this.getList = throttle(this.getList, 1000)
    _this.getList()
    this.$store.dispatch("bbsChange/logo", 'img:statics/logo_black.svg');
    this.$store.dispatch("bbsChange/titletype", 'GreaterWMS');
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
  width: 100%
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
