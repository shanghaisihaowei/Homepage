<template>
  <div>
    <!--                  首页个人信息展示-->
    <q-card v-if="isLogin" class="col-12 my-card shadow-0 q-pa-sm" style="height: 156px; margin-bottom: 30px">
      <q-card-section class="row" horizontal>
        <q-card-section class="col-2">
          <!--                      头像-->
          <q-img :src="user_info.icon" style="width: 108px; height: 108px;border-radius: 4px"/>
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
                  <span style="margin-left: 16px;cursor: pointer" @click="tochangMsg()">
                         <img src="statics/modify.svg"/>
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
                  class="my-font"
                  text-color="#ffffff"
                  align="left"
                  size="xs"
                  icon="img:statics/push.svg"
                  style="background-color: #116fec; width: 100px; height: 32px"
                  @click="this.$store.dispatch('bbsChange/releasediaChange', true)"
                >
                    <span
                      style="
                        font-size: 14px;
                        font-weight: 400;
                        margin-left: 20%;
                        color: white;
                      "
                    >
                      {{ $t('community.push_article') }}
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
    <!--                文章列表-->
    <q-infinite-scroll :offset="10">
      <q-card v-for="(item, index) in allArtInfos" :key="index" square class="col-12 my-card shadow-0"
              style="border-bottom: 1px #dcdcdc solid">
        <q-card-section>
          <div class="my-font card_tol Wrap_two">
            <a
              style="cursor: pointer"
              @click="this.$router.push('/bbs/articleDetail');setid(item.id)"
              class="my-font card_tol Wrap_two"
            >
              {{ item.title }}
            </a>
          </div>
        </q-card-section>

        <q-card-section style="margin-top: -20px" horizontal>
          <q-card-section v-show="item.cover != null">
            <q-img
              :src=item.cover
              style="width: 180px;
              height: 110px;border-radius: 4px;"/>
          </q-card-section>

          <q-card-section v-html="item.intro" class="article_text my-font"></q-card-section>
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
      <template v-slot:loading>
        <div class="row justify-center q-my-md">
          <q-spinner-dots color="primary" size="40px"/>
        </div>
      </template>
    </q-infinite-scroll>
  </div>
  <!--      发布弹窗dialog-->
  <q-dialog v-model="releasedialog" full-width>
    <q-card style="width: 580px !important; height: 500px">
      <!--          发布和关闭按钮-->
      <div
        class="my-font rel_dialog q-pa-md row"
        style="border-bottom: 1px #dcdcdc solid"
      >
        <div class="col-11">发布</div>
        <q-btn
          class="col-1"
          unelevated
          icon="close"
          @click="this.$store.dispatch('bbsChange/releasediaChange', false)"
          style="width: 16px; height: 16px; margin-left: 12px"
        />
      </div>
      <!--          标题-->
      <div class="q-pa-md" style="width: 100%; height: 100px">
        <div class="my-font">标题（问题）</div>
        <input
          class="rel_problem"
          v-model="post_art.title"
          style="
                width: 100%;
                height: 42px;
                border: 1px solid #e4e4e4;
                margin-top: 10px;
              "
          @keyup="getpushValue"
        />
      </div>
      <!--          内容-->
      <div class="column q-pa-md" style="width: 100%; height: 250px">
        <div class="col-1 my-font rel_problem">内容</div>
        <div class="col-1"></div>
        <div class="col-1">
          <q-editor
            style="
                  width: 546px;
                  height: 200px;
                  overflow-y: auto;
                  overflow-x: auto;
                "
            v-model="post_art.massage"
            :dense="$q.screen.lt.md"
            :toolbar="[
                  [
                    {
                      label: $q.lang.editor.align,
                      icon: $q.iconSet.editor.align,
                      fixedLabel: true,
                      list: 'only-icons',
                      options: ['left', 'center', 'right', 'justify'],
                    },
                  ],
                  ['bold', 'subscript', 'superscript'],
                  [
                    {
                      label: $q.lang.editor.fontSize,
                      icon: $q.iconSet.editor.fontSize,
                      fixedLabel: true,
                      fixedIcon: true,
                      list: 'no-icons',
                      options: [
                        'size-1',
                        'size-2',
                        'size-3',
                        'size-4',
                        'size-5',
                        'size-6',
                        'size-7',
                      ],
                    },
                  ],

                  ['quote', 'unordered'],
                  ['viewsource'],
                ]"
            :fonts="{
                  arial: 'Arial',
                  arial_black: 'Arial Black',
                  comic_sans: 'Comic Sans MS',
                  courier_new: 'Courier New',
                  impact: 'Impact',
                  lucida_grande: 'Lucida Grande',
                  times_new_roman: 'Times New Roman',
                  verdana: 'Verdana',
                }"
          ></q-editor>
        </div>
      </div>
      <!--          发布帖子-->
      <div class="q-pa-md" style="width: 100%">
        <q-btn
          v-show="!ispushOK"
          unelevated
          class="push_deNotebtn"
          style="float: right; width: 110px; height: 40px"
        >
              <span class="my-font push_note">{{
                  $t("community.push_note")
                }}</span>
        </q-btn>
        <q-btn
          v-show="ispushOK"
          unelevated
          class="push_notebtn"
          style="float: right; width: 110px; height: 40px"
          @click="sendArticles()"
        >
              <span class="my-font push_note">{{
                  $t("community.push_note")
                }}</span>
        </q-btn>
      </div>
    </q-card>
  </q-dialog>
</template>

<style lang="scss" scoped>
.rel_dialog{
  font-weight: 400;
  font-size: 20px;
  color: #333333
}
</style>
<script>
import {defineComponent} from 'vue';
import storage from "boot/localStorage";
import {getauth, post} from "boot/axios";
import {Cookies} from "quasar";

export default defineComponent({
  name: 'DVadmin',
  data() {
    return {
      allArtInfos: [],
      next_msg: '',
      releasedialog: false,
      post_art: {
        title: '',
        massage: ''
      },
      ispushOK: false,
      community_type: '1'
    }
  },
  computed: {
    isLogin() {
      return this.$store.state.bbsChange.isLogin;
    },
    user_info() {
      return this.$store.state.bbsChange.user_info;
    },
  },
  methods: {
    // 判断发布按钮变颜色
    getpushValue() {
      var _this = this;
      if (_this.post_art.title.length >= 1) {
        _this.ispushOK = true;
      } else {
        _this.ispushOK = false;
      }
    },
    setid(id) {
      storage.set('choseid', id)
    },
    // 跳转到修改信息页面
    tochangMsg() {
      var _this = this
      _this.$store.dispatch('bbsChange/isIndexMenu', false)
      _this.$router.push('changePsd')
    },
    // 发布文章
    sendArticles() {
      var _this = this;
      var msg = {
        title: _this.post_art.title,
        intro: _this.$store.state.bbsChange.user_info.intro,
        content: _this.post_art.massage,
        author: _this.$store.state.bbsChange.user_info.nickname,
        community_type: _this.community_type,
      };
      post("/article/api/v1/article/", msg)
        .then((res) => {
          var results = res.result;
          storage.set("latest_id", results.id);
          console.log(res);
          _this.$q.notify({
            message: _this.send_suc,
            icon: "check",
            color: "green",
          });
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
      this.$store.dispatch("bbsChange/releasediaChange", false);
      msg = {};
      console.log(1);
      _this.getallArticle();
      console.log(2);
      _this.$router.push("/bbs");
      console.log(3);
    },
    // 无限滚动
    // onLoad(index, done) {
    //   var  next_url
    //   // 获取换页的URL
    //   getauth("/article/api/v1/Browse/")
    //     .then((res) => {
    //       next_url = res.result.next
    //       console.log(next_url)
    //       if (next_url !== null) {
    //         console.log(next_url)
    //         getauth(next_url).then(res => {
    //           console.log(333,res)
    //           next_url = res.result.next
    //           this.next_msg = res.result.results
    //         }).catch(err => {
    //           this.$q.notify({
    //             message: err.detail,
    //             icon: 'close',
    //             color: 'negative'
    //           })
    //         })
    //       }
    //     }).catch(err => {
    //     this.$q.notify({
    //       message: err.detail,
    //       icon: 'close',
    //       color: 'negative'
    //     })
    //   })
    //   setTimeout(() => {
    //     let _this = this;
    //     if (this.allArtInfos) {
    //       console.log(this.allArtInfos)
    //       for (let i = 0; i <= _this.next_msg.length - 1; i++) {
    //         _this.allArtInfos.push(_this.next_msg[i])
    //       }
    //       done()
    //     }
    //   }, 2000)
    // }
  },
  mounted() {
    var _this = this;
    getauth("/article/api/v1/Browse/?community_type=1")
      .then((res) => {
        _this.allArtInfos = res.result.results
      })
      .catch((err) => {
        _this.$q.notify({
          message: err.detail,
          icon: "close",
          color: "negative",
        });
      });
  }
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
