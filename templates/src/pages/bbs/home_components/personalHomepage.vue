<template>
  <div class="my_article_container">
    <div class="row my-font">
      <q-card class="col-12">
        <!--          顶部信息栏-->
        <q-card-section
          class="row"
          style="
            height: 180px;
            background-image: url('statics/homepagebg.png');
            background-repeat: no-repeat;
            background-size: cover;
          "
        >
          <!--                    头像-->
          <q-card-section class="col-2">
            <q-avatar size="120px">
              <img
                :src="per_icon"
                style="border-radius: 61px; background: white"
              />
            </q-avatar>
          </q-card-section>
          <!--                    信息-->
          <q-card-section class="col-7 column" style="margin-left: 20px">
            <div class="col-2"></div>
            <!--                      昵称-->
            <div class="col-3 my-font my_homenick">
              <span>
                {{ myhome.nickname }}
              </span>
              <span
                style="margin-left: 16px; cursor: pointer"
                @click="tochangMsg()"
              >
                <img src="statics/modify_white.svg" />
              </span>
            </div>
            <div class="col-2"></div>
            <!--                      个性签名-->
            <div class="col-3 my-font my_homeintro">
              {{ myhome.intro }}
            </div>
          </q-card-section>
          <!--                    发布文章-->
          <q-card-section class="col-2 column">
            <div class="col-3"></div>
            <div style="float: right" class="col-4">
              <q-btn
                icon="img:statics/homepage_push.svg"
                @click="$store.dispatch('bbsChange/releasediaChange', true)"
                style="
                  background: white;
                  color: #116fec;
                  min-width: 120px;
                  height: 38px;
                  float: right;
                "
              >
                <span
                  class="my-font"
                  style="margin-left: 10px; font-size: 16px"
                  >{{ $t("community.push_article") }}</span
                >
              </q-btn>
            </div>
          </q-card-section>
        </q-card-section>

        <q-separator inset />

        <q-card-section>
          <q-card-section class="q-pt-xs">
            <div class="text-h6 q-mt-sm q-mb-xs">
              {{ $t("community.my_article") }}
            </div>
          </q-card-section>

          <q-separator inset />
        </q-card-section>

        <q-card v-if="default_page" class="q-pa-md" style="padding-top: 100px">
          <div style="height: 400px" class="q-pa-md">
            <div class="flex flex-center">
              <q-img
                width="107px"
                height="117px"
                src="statics/community/default_page.svg"
              />
            </div>
            <div class="q-pa-md flex flex-center default_page">
              {{ $t("community.default_page") }}
            </div>
          </div>
        </q-card>
        <div v-if="!default_page">
          <q-card
            v-for="(item2, index) in myAllarticle"
            :key="index"
            square
            class="col-12 q-pa-md my-card shadow-0"
            style="padding-top: 0"
          >
            <div v-if="!num_index[index]">
              <q-card-section class="row" style="padding-top: 0">
                <span class="col-11 my-font card_tol Wrap_two">
                  {{ item2.title }}
                </span>
                <span class="col-1" style="margin-left: 10px">
                  <div
                    v-if="item2.check_person === '2'"
                    class="Moderated text-center"
                  >
                    {{ $t("community.not_reviewed") }}
                  </div>
                  <div
                    v-if="item2.check_person === '0'"
                    class="Review_failed text-center"
                  >
                    {{ $t("community.review_failed") }}
                  </div>
                </span>
              </q-card-section>

              <q-card-section style="margin-top: -20px" horizontal>
                <q-card-section class="Wrap_two article_text my-font">
                  {{ item2.intro }}
                </q-card-section>
              </q-card-section>

              <div class="q-pa-md" style="margin-top: -10px">
                <span
                  class="my-font"
                  style="font-size: 14px; font-weight: 400; color: #999999"
                >
                  <q-img
                    style="margin-top: -2px; margin-right: 10px"
                    width="12px"
                    height="14px"
                    src="statics/author.svg"
                  />
                  {{ item2.author_icon.author }}
                </span>
                <span
                  class="my-font-D"
                  style="
                    font-size: 14px;
                    font-weight: 400;
                    color: #999999;
                    margin-left: 1%;
                  "
                >
                  <span style="font-size: 14px !important">
                    {{ $t("community.push_time") }}
                  </span>
                  <span class="my-font" style="font-size: 14px !important">
                    {{ item2.updata_time }}
                  </span>
                </span>
                <div style="float: right">
                  <a
                    @click="
                      del_articles = true;
                      id_index = item2.id;
                    "
                    class="a_text my-font"
                    style="cursor: pointer; border-bottom: 1px black solid"
                  >
                    {{ $t("community.del") }}
                  </a>
                  <span class="my-font a_text"> &nbsp;/&nbsp; </span>
                  <a
                    @click="
                      pre_edit = true;
                      per_index = item2.id;
                      per_problem = item2.title;
                      markdown_text = item2.markdown_text;
                      this.num_index[index] = true;
                    "
                    class="a_text my-font"
                    style="cursor: pointer; border-bottom: 1px black solid"
                  >
                    {{ $t("community.edit") }}
                  </a>
                </div>
              </div>
              <div
                style="
                  width: 97%;
                  border-bottom: 1px #dcdcdc solid;
                  margin: 0 auto;
                "
              ></div>
            </div>

            <q-card-section v-if="num_index[index]" style="min-height: 550px">
              <!--          修改和关闭按钮-->
              <div
                class="my-font rel_dialog q-pa-md row"
                style="border-bottom: 1px #dcdcdc solid"
              >
                <div class="col-11 my-font edit_top">
                  {{ $t("community.edit_article") }}
                </div>
                <q-btn
                  class="col-1"
                  unelevated
                  icon="close"
                  @click="cancel_edit()"
                  style="width: 16px; height: 16px; margin-left: 12px"
                />
              </div>
              <!--          标题-->
              <div class="q-pa-md" style="width: 100%; height: 100px">
                <div class="edit_tit">
                  {{ $t("community.tip") }}
                </div>
                <input
                  class="rel_problem"
                  v-model="per_problem"
                  style="
                    width: 100%;
                    height: 42px;
                    border: 1px solid #e4e4e4;
                    margin-top: 10px;
                  "
                />
              </div>
              <!--          内容-->
              <div class="q-pa-md" style="width: 100%; min-height: 280px">
                <div style="font-size: 18px" class="rel_problem q-mb-sm">
                  {{ $t("community.content") }}
                </div>
                <markdown-aditor
                  @getMarkdownHtml="getMarkdownHtml('per_qeditor', $event)"
                  @getMarkdownText="getMarkdownText"
                  :needUploadImg="true"
                  :idIndex="1"
                  :markdownText="markdown_text"
                ></markdown-aditor>
              </div>
              <!--          确认修改-->
              <div style="width: 100%; text-align: right">
                <q-btn
                  unelevated
                  class="finish_btn q-mr-md"
                  style="width: 110px"
                  @click="
                    edit_article(per_index);
                    cancel_edit();
                  "
                >
                  <span class="my-font">
                    {{ $t("community.finish") }}
                  </span>
                </q-btn>
              </div>
            </q-card-section>
            <div
              v-if="num_index[index]"
              style="
                width: 96.1%;
                border-bottom: 1px #dcdcdc solid;
                margin: 0 auto;
              "
            ></div>
          </q-card>
        </div>
      </q-card>
      <div
        style="width: 100%"
        v-if="hasPagination"
        class="q-pa-md flex flex-center bg-white"
      >
        <q-pagination
          class="q_pagination"
          direction-links
          v-model="currentPage"
          :max="maxPages"
          :max-pages="6"
        />
      </div>
    </div>
    <!--      删除文章确认dialog-->
    <q-dialog v-model="del_articles" full-width>
      <q-card class="del_diaCard q-pa-md">
        <!--          提示-->
        <span class="my-font del_diaCard_tip">
          {{ $t("community.hint") }}
        </span>
        <!--          关闭按钮-->
        <span style="float: right">
          <q-btn padding="0" flat icon="close" @click="del_articles = false" />
        </span>
        <!--          确认删除？-->
        <div style="border-top: 1px #dcdcdc solid">
          <div class="my-font del_diaCard_msg1 text-center">
            {{ $t("community.confirm_del") }}
          </div>
        </div>
        <!--          确认与取消-->
        <div class="q-pa-xl">
          <div>
            <q-btn
              unelevated
              class="del_diaCard_btn1 my-font text-center"
              @click="delete_article(id_index)"
              >{{ $t("index.confirm") }}
            </q-btn>
            <q-btn
              unelevated
              class="del_diaCard_btn2"
              style="float: right"
              @click="del_articles = false"
              >{{ $t("index.cancel") }}
            </q-btn>
          </div>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { deleteauth, getauth, putauth } from "boot/axios";
import { Cookies } from "quasar";
import jwtDecode from "jwt-decode";
import MarkdownAditor from "./market/components/MarkdownAditor";

export default defineComponent({
  name: "per_homepage",
  components: {
    MarkdownAditor,
  },
  data() {
    return {
      per_icon: "",
      per_problem: "",
      per_qeditor: "",
      id_index: "",
      del_articles: false,
      myAllarticle: [],
      pre_edit: false,
      per_index: "",
      num_index: [],
      default_page: false,
      hasPagination: false,
      maxPages: 1,
      currentPage: 1,
      markdown_text: "",
    };
  },
  computed: {
    myhome() {
      return this.$store.state.bbsChange.user_info;
    },
  },
  watch: {
    currentPage(val) {
      this.redirectPage(val);
    },
  },
  methods: {
    // 获取个人的文章
    getPerarticle() {
      var _this = this;
      getauth("/article/api/v1/article/")
        .then((res) => {
          _this.setOrdersList(res);
          if (res.count === 0) {
            _this.default_page = true;
          } else {
            _this.myAllarticle = res.results;
            _this.maxPages = Math.ceil(res.count / 20);
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    // 删除文章
    delete_article(id) {
      var _this = this;
      deleteauth("/article/api/v1/article/" + id)
        .then((res) => {
          console.log(res);
          _this.$q.notify({
            message: _this.$t("community.del_suc"),
            icon: "check",
            color: "green",
          });
          location.reload();
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    //修改文章
    edit_article(id) {
      var _this = this;
      var msg = {};
      msg["title"] = _this.per_problem;
      msg["content"] = _this.per_qeditor;
      msg["markdown_text"] = _this.markdown_text;
      putauth("/article/api/v1/article/" + id + "/", msg)
        .then((res) => {
          if (res.code === 200) {
            _this.$q.notify({
              message: _this.$t("community.edit_suc"),
              icon: "check",
              color: "green",
            });
            location.reload();
          } else {
            _this.$q.notify({
              message: _this.$t("community.change_err"),
              icon: "close",
              color: "negative",
            });
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    // 取消或关闭编辑文章
    cancel_edit() {
      var _this = this;
      _this.num_index = !_this.num_index;
      _this.num_index = [];
    },
    // 跳转到修改信息页面
    tochangMsg() {
      var _this = this;
      _this.$store.dispatch("bbsChange/isIndexMenu", false);
      _this.$router.push({ name: "changePsd" });
    },
    setOrdersList(res) {
      this.myAllarticle = res.results;
      if (res.next || res.previous) {
        this.hasPagination = true;
      } else {
        this.hasPagination = false;
      }
    },
    redirectPage(page) {
      getauth(`/article/api/v1/article/?page=${page}`).then((res) => {
        this.setOrdersList(res);
        //回到顶部
        document.getElementsByClassName(
          "q-scrollarea__container"
        )[0].scrollTop = 0;
      });
    },
    //获取markdown输入的文字
    getMarkdownHtml(key, val) {
      this[key] = val;
    },
    getMarkdownText(val) {
      this.markdown_text = val;
      console.log(val);
    },
  },
  mounted() {
    if (this.$q.cookies.has("token")) {
      let userinfos = jwtDecode(this.$q.cookies.get("token"));
      this.per_icon = window.g.BaseUrl + userinfos.icon;
    } else {
    }
    this.getPerarticle();
    this.$store.dispatch("bbsChange/isIndexMenu", false);
    this.$store.dispatch("bbsChange/link", "personalHomepage");
  },
});
</script>

<style scoped lang="sass">
.default_page
    font-size: 15px
    color: #666666
.edit_top
    font-size: 20px
    font-weight: 400
    color: #333333

.edit_tit
    font-size: 18px
    font-weight: 400
    color: #333333

.finish_btn
    width: 110px
    height: 40px
    background-color: #116FEC
    font-size: 16px
    font-weight: 500
    color: white

.del_diaCard
    width: 460px !important
    height: 300px
    background: white
    border-radius: 4px

.del_diaCard_tip
    font-size: 20px
    font-weight: 400
    color: #333333

.del_diaCard_msg1
    font-size: 20px
    font-weight: 400
    color: #333333
    margin-top: 9%

.del_diaCard_btn1
    width: 120px
    height: 40px
    font-size: 16px
    font-weight: 400
    color: #333333
    border: 1px solid #979797
    border-radius: 4px

.del_diaCard_btn2
    width: 120px
    height: 40px
    font-size: 16px
    font-weight: 400
    background-color: #116FEC
    color: white

.a_text
    font-size: 14px
    font-weight: 400
    color: #999999

.article_text
    width: 95%
    font-size: 15px
    font-weight: 400
    color: #666666
    letter-spacing: 1px
    padding-bottom: 0

.my_homenick
    color: white
    font-size: 18px
    font-weight: 500

.my_homeintro
    color: white
    font-size: 14px
    font-weight: 400

.Wrap_two
    overflow: hidden
    text-overflow: ellipsis
    display: -webkit-box
    -webkit-box-orient: vertical
    -webkit-line-clamp: 3

.card_tol
    width: 90%
    font-size: 18px !important
    font-weight: 600
    color: #333333
    letter-spacing: 1px
.Moderated
    background: #ffffff
    border: 1px solid #f79d00
    border-radius: 2px
    font-size: 16px
    font-weight: 500
    color: #F79D00
    float: right
.Review_failed
    width: 170%
    background: #ffffff
    border: 1px solid #e53a3a
    border-radius: 2px
    font-size: 16px
    font-weight: 500
    color: #E53A3A
    float: right
</style>
