<template>
  <div>
    <q-input v-model="pagelocation" style="display: none" />
    <q-card v-if="imgSrc[0]" flat class="q-mb-lg">
      <a :title="imgTitle[0]" :href="imgHref[0]">
        <img :src="imgSrc[0]" style="width: 100%" />
      </a>
    </q-card>
    <!--                  首页个人信息展示-->
    <q-card
      v-if="isLogin"
      class="col-12 my-card shadow-0 q-pa-sm"
      style="height: 156px; margin-bottom: 30px"
    >
      <q-card-section class="row" horizontal>
        <q-card-section class="col-2">
          <!--                      头像-->
          <q-img
            :src="icon"
            style="width: 108px; height: 108px; border-radius: 4px"
          />
        </q-card-section>

        <q-card-section class="col-9 column">
          <div class="col-6 row">
            <div class="col-10 column">
              <div class="col-4"></div>
              <div class="col-4 row">
                <!--                            用户名；昵称-->
                <div class="col-8 my-font user_name Wrap_one">
                  <span>
                    {{ user_info.nickname }}
                  </span>
                  <span
                    style="margin-left: 16px; cursor: pointer"
                    @click="tochangMsg()"
                  >
                    <img src="statics/modify.svg" />
                  </span>
                </div>

                <div class="col-4"></div>
              </div>
              <div class="col-4"></div>
            </div>
            <div class="col-2 column">
              <div class="col-3"></div>
              <div class="col-6">
                <!--                            发布按钮-->
                <q-btn
                  flat
                  text-color="#ffffff"
                  icon="img:statics/push.svg"
                  style="
                    background-color: #116fec;
                    min-width: 120px;
                    height: 38px;
                  "
                  @click="$store.dispatch('bbsChange/releasediaChange', true)"
                >
                  <span
                    style="
                      font-size: 14px;
                      font-weight: 400;
                      margin-left: 20%;
                      color: white;
                    "
                  >
                    {{ $t("community.push_article") }}
                  </span>
                </q-btn>
              </div>
              <div class="col-3"></div>
            </div>
          </div>
          <div class="col-6 column article_text">
            <div class="col-4"></div>
            <div class="col-4 wrap_neo">
              {{ user_info.intro }}
            </div>
            <div class="col-4"></div>
          </div>
        </q-card-section>
      </q-card-section>
    </q-card>
    <!--    搜索框-->
    <q-card class="row q-pa-md my-card shadow-0">
      <div
        class="col-2"
        style="font-size: 18px; font-weight: 400; color: #333333"
      >
        <div style="padding-top: 0; padding-bottom: 0">
          <!--          <q-btn-dropdown-->
          <!--            unelevated-->
          <!--            style="float: right; margin-right: 20px"-->
          <!--            color="primary"-->
          <!--            :label="community_type"-->
          <!--          >-->
          <!--            <q-list>-->
          <!--              <q-item clickable v-close-popup @click="chose_gwms_type()">-->
          <!--                <q-item-section>-->
          <!--                  <q-item-label-->
          <!--                  >GreaterWMS{{ $t("index.navbar.community") }}-->
          <!--                  </q-item-label-->
          <!--                  >-->
          <!--                </q-item-section>-->
          <!--              </q-item>-->

          <!--              <q-item clickable v-close-popup @click="chose_dv_type()">-->
          <!--                <q-item-section>-->
          <!--                  <q-item-label-->
          <!--                  >DVadmin{{ $t("index.navbar.community") }}-->
          <!--                  </q-item-label-->
          <!--                  >-->
          <!--                </q-item-section>-->
          <!--              </q-item>-->
          <!--            </q-list>-->
          <!--          </q-btn-dropdown>-->
        </div>
        {{ $t("community.newest") }}
      </div>
      <div class="col-6"></div>
      <div class="col-4">
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
              style="height: 40px"
              color="primary"
              icon="search"
              unelevated
              @click="getsearchList()"
            />
          </template>
        </q-input>
      </div>
    </q-card>
    <!--                文章列表-->
    <q-card
      v-for="(item, index) in allArtInfos"
      :key="index"
      square
      class="col-12 my-card shadow-0"
      style="border-bottom: 1px #dcdcdc solid"
    >
      <q-card-section>
        <div class="my-font card_tol Wrap_two">
          <a
            style="cursor: pointer"
            @click.stop="
              this.$router.push({
                path: `/community/DVadminDetail/${item.id}`,
              })
            "
            class="my-font card_tol Wrap_two"
          >
            {{ item.title }}
          </a>
        </div>
      </q-card-section>

      <q-card-section style="margin-top: -20px" horizontal>
        <q-card-section v-show="item.cover != null">
          <q-img
            :src="item.cover"
            style="width: 180px; height: 110px; border-radius: 4px"
          />
        </q-card-section>

        <q-card-section
          v-html="item.intro"
          class="article_text my-font"
        ></q-card-section>
      </q-card-section>

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
            style="margin-top: -2px; margin-right: 10px"
            width="12px"
            height="14px"
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
          <span style="font-size: 12px !important">
            {{ $t("community.push_time") }}
            {{ item.updata_time }}
          </span>
        </div>
      </q-card-actions>
    </q-card>
    <div class="flex flex-center" v-show="pathname !== null">
      <q-spinner-dots color="primary" size="xl" />
    </div>
    <div class="text-center q-mt-lg" v-show="pathname === null">
      {{ $t("notice.nomoredata") }}
    </div>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import { get } from "boot/axios";
import { createMetaMixin, throttle } from "quasar";
import jwtDecode from "jwt-decode";

export default defineComponent({
  data() {
    return {
      title: "",
      meta: {},
      allArtInfos: [],
      pathname: "/article/api/v1/Browse/?community_type=1",
      requestcount: 0,
      next_msg: "",
      icon: "",
      searchword: "",
      imgSrc: [],
      imgHref: [],
      imgTitle: [],
    };
  },
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
      var _this = this;
      if (this.pagelocation < 0.99) {
        _this.requestcount = 0;
      } else {
        _this.requestcount = 1;
      }
      if (
        this.pagelocation >= 0.99 &&
        _this.pathname !== null &&
        _this.requestcount === 1
      ) {
        _this.getList();
      }
      return this.$store.state.pagelocation.pagelocation;
    },
  },
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.title,
        meta: this.meta,
      };
    }),
  ],
  methods: {
    getsearchList() {
      var _this = this;
      _this.pathname = "/article/api/v1/Browse/?community_type=1";
      if (_this.pathname !== null) {
        get(_this.pathname + "&title__contains=" + _this.searchword)
          .then((res) => {
            _this.allArtInfos = [];
            _this.pathname = res.result.next;
            res.result.results.forEach((item) => {
              _this.allArtInfos.push(item);
            });
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
    getList() {
      var _this = this;
      if (_this.pathname !== null) {
        get(_this.pathname)
          .then((res) => {
            _this.pathname = res.result.next;
            res.result.results.forEach((item) => {
              _this.allArtInfos.push(item);
            });
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
    // 跳转到修改信息页面
    tochangMsg() {
      var _this = this;
      _this.$store.dispatch("bbsChange/isIndexMenu", false);
      _this.$router.push({ name: "changePsd" });
    },
    getAdvertisingImg() {
      get("resp/api/v1/article_banner/?community=1").then((res) => {
        res.forEach((item, index) => {
          this.imgHref[index] = item.link;
          this.imgSrc[index] = item.image;
          this.imgTitle[index] = item.title;
        });
      });
    },
  },
  created() {
    var _this = this;
    _this.getAdvertisingImg();
    if (_this.$q.cookies.get("lang") === "zh-hans") {
      _this.title = "DVAdmin - 开源社区";
      _this.meta = {
        description: {
          name: "description",
          content: "DVAdmin - Open Source Warehouse Management System",
        },
        keywords: {
          name: "keywords",
          content:
            "聚商汇WMS,开源仓库管理系统,仓库管理系统,wms,仓库管理软件,仓库管理,GreaterWMS, greaterwms",
        },
        equiv: {
          "http-equiv": "Content-Type",
          content: "text/html; charset=UTF-8",
        },
        ogTitle: {
          property: "og:title",
          template(ogTitle) {
            return `${ogTitle} - DVAdmin`;
          },
        },
      };
    } else {
      _this.title = "DVAdmin - Community";
      _this.meta = {
        description: {
          name: "description",
          content: "DVAdmin - Open Source Warehouse Management System",
        },
        keywords: {
          name: "keywords",
          content:
            "GreaterWMS - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms",
        },
        equiv: {
          "http-equiv": "Content-Type",
          content: "text/html; charset=UTF-8",
        },
        ogTitle: {
          property: "og:title",
          template(ogTitle) {
            return `${ogTitle} - DVAdmin`;
          },
        },
      };
    }
  },
  mounted() {
    var _this = this;
    if (_this.$q.cookies.has("token")) {
      let userinfos = jwtDecode(_this.$q.cookies.get("token"));
      _this.icon = window.g.BaseUrl + userinfos.icon;
    } else {
    }
    _this.allArtInfos = [];
    _this.getList = throttle(this.getList, 1000);
    _this.getList();
    _this.$store.dispatch("bbsChange/logo", "img:statics/DV_logo.svg");
    _this.$store.dispatch("bbsChange/titletype", "DVAdmin");
  },
});
</script>
<style scoped lang="sass">
.article_text
    width: 100%
    font-size: 15px
    font-weight: 400
    color: #666666
    letter-spacing: 1px
    word-wrap: break-word

.card_tol
    width: 100%
    font-size: 18px !important
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
