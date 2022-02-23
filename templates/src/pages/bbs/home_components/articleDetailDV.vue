<template>
  <div class="row my-font">
    <q-card class="col-12 shadow-0">
      <!--                  返回按钮-->
      <q-card-actions>
        <q-btn
          @click="this.$router.push({ name: 'community' })"
          style="font-size: 14px; font-weight: 400; color: #999999"
          unelevated
          :label="goblack"
        />
      </q-card-actions>

      <q-separator inset />

      <q-card-section horizontal>
        <!--        头像及作者-->
        <q-card-section class="q-pa-md">
          <q-avatar size="60px">
            <img :src="avatar_img" />
          </q-avatar>
        </q-card-section>
        <q-card-section class="q-pa-md flex flex-center">
          <span class="author my-font">
            {{ author }}
          </span>
        </q-card-section>
        <q-card-section class="q-pa-md flex flex-center art_time my-font-D">
          <span v-if="is_uptime === true">
            {{ $t("community.push_time") }}
          </span>
          <span v-if="is_uptime === false">
            {{ $t("community.revise_time") }}
          </span>
          <span>
            {{ time }}
          </span>
        </q-card-section>
      </q-card-section>
      <!--      文章标题-->
      <q-card-section>
        <div class="tit my-font">
          {{ title }}
        </div>
      </q-card-section>
      <!--        文章集体内容-->
      <q-card-section>
        <div v-html="content" class="art_msg my-font"></div>
      </q-card-section>
      <!--       图片-->
      <q-card-section>
        {{ imgs }}
      </q-card-section>
      <q-separator />
    </q-card>
    <!--    评论区-->
    <q-card class="col-12 shadow-0" style="margin-top: 30px">
      <comment-list
        class="col-12"
        :commentList="first_LR"
        :userId="userid"
        type="article"
      ></comment-list>
    </q-card>
  </div>
</template>

<style lang="scss" scoped>
.check_more {
  margin-left: 52px;
  margin-top: 10px;
}

.check_morebtn {
  cursor: pointer;
  color: #999999;
}

.sen_cun {
  margin-top: 10px;
  margin-left: 48px;
}

.reply_div {
  margin-top: 10px;
  padding: 0 50px;
}

.reply_a {
  font-size: 14px;
  font-weight: 400;
  color: #666666;
  margin-left: 6px;
  cursor: pointer;
}

.fir_reply_msg {
  font-size: 16px;
  font-weight: 400;
  color: #333333;
  line-height: 24px;
  padding: 0 50px;
}

.fir_reply_time {
  font-size: 14px;
  font-weight: 400;
  color: #999999;
}

.fir_reply_author {
  font-size: 14px;
  font-weight: 400;
  color: #666666;
}

.reply_btn {
  float: right;
  width: 100px;
  height: 34px;
  background: #116fec;
  color: white;
  font-size: 14px;
  font-weight: 400;
}

.avatar_pad {
  padding-right: 0;
}

.editor_pad {
  padding-left: 0;
  margin-left: -3%;
}

.commentary_card {
  margin-top: 30px;
}

.art_msg {
  letter-spacing: 1px;
  font-size: 15px;
  font-weight: 400;
  text-align: left;
  color: #333333;
  line-height: 23px;
}

.art_time {
  margin-top: 5px;
  font-size: 16px;
  font-weight: 400;
  color: #999999;
}

.author {
  font-size: 20px;
  font-weight: 400;
  color: #333333;
}

.tit {
  font-size: 20px;
  font-weight: 600;
  color: #333333;
  line-height: 30px;
}
</style>

<script>
import { defineComponent } from "vue";
import jwtDecode from "jwt-decode";
import { get, postauth } from "boot/axios";
import { createMetaMixin } from "quasar";
import commentList from "./market/components/CommentList";
export default defineComponent({
  components: {
    commentList,
  },
  data() {
    return {
      userid: "",
      avatar_now: "",
      goblack: this.$t("community.black"),
      title: "",
      avatar_img: "",
      author: "",
      time: "",
      content: "",
      imgs: "",
      qeditor_commentary: "",
      comment_count: "",
      first_LR: [],
      sen_qeditor: "",
      write_reply: this.$t("community.write_reply"),
      isWrite: [],
      has_child: [],
      comment_more: [],
      isexhibit: true,
      is_uptime: true,
      isLogin: false,
    };
  },
  computed: {
    articleId() {
      return this.$store.state.bbsChange.articleId;
    },
  },
  methods: {
    getavayarinfo() {
      var _this = this;
      let userinfoStr = jwtDecode(_this.$q.cookies.get("token"));
      _this.avatar_now = userinfoStr.icon;
    },
    // 获取文章详情
    getdetailedinfo() {
      var _this = this;
      get(
        "article/api/v1/Browse/" +
          _this.$q.cookies.get("articleId") +
          "/" +
          "?community_type=1"
      )
        .then((res) => {
          var res_msg = res.result;
          _this.title = res_msg.title;
          _this.head_title = res_msg.title;
          _this.author = res_msg.author_icon.author;
          _this.content = res_msg.content;
          _this.imgs = res_msg.cover;
          _this.comment_count = res_msg.comment_count;
          _this.avatar_img = res_msg.author_icon.icon;
          _this.first_LR = res_msg.comment;
          _this.userid = res_msg.author_icon.id;
          if (res_msg.changed_time === res_msg.create_time) {
            _this.time = res_msg.updata_time;
            _this.is_uptime = true;
          } else {
            _this.time = res_msg.create_time;
            _this.is_uptime = false;
          }
          _this.meta = {
            description: {
              name: "description",
              content: "DVAdmin - Open Source Warehouse Management System",
            },
            keywords: { name: "keywords", content: res_msg.content },
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
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    // 发表评论（一级）
    post_comment() {
      var _this = this;
      var msg = {};
      msg["content"] = _this.qeditor_commentary;
      msg["depth"] = 1;
      msg["article"] = _this.$q.cookies.get("articleId");
      postauth("/comment/api/v1/commentadd/", msg)
        .then((res) => {
          if (res.code === 200) {
            _this.$q.notify({
              message: _this.$t("community.reply_suc"),
              icon: "check",
              color: "green",
            });
            location.reload();
          } else {
            _this.$q.notify({
              message: _this.$t("community.reply_err"),
              icon: "close",
              color: "negative",
            });
          }
          // var res_msg = res.result
          // _this.first_LR.icon = res_msg.user__icon
          // _this.first_LR.author = res_msg.user__nickname
          // _this.first_LR.time = res_msg.updata_time
          // _this.first_LR.msg = res_msg.content
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    //点击回复
    click_isWrite(i) {
      var _this = this;
      _this.isWrite[i] = !_this.isWrite[i];
    },
    //发表评论（二级）
    post_comment_sen(id, name) {
      var _this = this;
      var msg = {};
      msg["depth"] = 2;
      msg["reply"] = id;
      msg["root"] = id;
      msg["article"] = _this.$q.cookies.get("articleId");
      msg["content"] = _this.sen_qeditor;
      postauth("/comment/api/v1/commentadd/", msg)
        .then((res) => {
          if (res.code === 200) {
            _this.$q.notify({
              message: "成功",
              icon: "check",
              color: "green",
            });
          }
          _this.isWrite = [];
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    // 查看更多回复
    getcommentmore(id, index) {
      var _this = this;
      get("/comment/api/v1/commentget/?root=" + id)
        .then((res) => {
          _this.comment_more[index] = res.result;
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
      _this.isMore = [];
    },
  },
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.head_title,
        meta: this.meta,
      };
    }),
  ],
  created() {
    var _this = this;
    if (_this.$q.cookies.get("lang") === "zh-hans") {
      _this.head_title = "DVAdmin - 开源社区";
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
      _this.head_title = "GreaterWMS - Community";
      _this.meta = {
        description: {
          name: "description",
          content: "GreaterWMS - Open Source Warehouse Management System",
        },
        keywords: {
          name: "keywords",
          content:
            "DVAdmin - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms",
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
      _this.getavayarinfo();
      _this.isLogin = true;
    } else {
      _this.isLogin = false;
    }
    this.getdetailedinfo();
  },
});
</script>
