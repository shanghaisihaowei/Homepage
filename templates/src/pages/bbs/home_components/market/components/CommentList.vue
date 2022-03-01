<template>
  <div>
    <div v-show="!this.$q.platform.is.mobile" class="q-pb-lg q-pt-md q-px-md">
      <div class="flex relative-position q-pb-xl" v-if="isLogin">
        <q-img
          width="50px"
          height="50px"
          class="radius_circle"
          :src="headPortrait_url"
        ></q-img>
        <div class="q-pl-md" style="width: calc(100% - 50px)">
          <q-editor
            content-class="bg-grey-1"
            toolbar-toggle-color="primary"
            v-model="editorText1"
            min-height="200px"
          />
        </div>
        <div style="position: absolute; right: 0; bottom: 0">
          <q-btn
            flat
            style="background: #116efc; color: white"
            @click="releaseReviews(1, '', '', '')"
            >{{ $t("community.e_shop_view.release") }}</q-btn
          >
        </div>
      </div>
      <q-card
        square
        flat
        @click="$store.dispatch('bbsChange/toLoginChange', true)"
        v-if="!isLogin"
        style="height: 60px; font-size: 18px; color: #666666"
        class="flex flex-center bg-blue-1"
      >
        <img
          class="q-mr-sm"
          style="width: 18px; height: 18px"
          src="statics/info.svg"
        />
        {{ $t("community.e_shop_view.no_login_prompt") }}，<span
          style="text-decoration: underline; color: blue; cursor: pointer"
          >{{ $t("community.e_shop_view.tologin") }}</span
        ></q-card
      >
    </div>
    <q-card square flat class="text-body1 q-pa-md" :class="{'border_top': this.$q.platform.is.mobile}"
      >{{ commentNumber }}{{ $t("community.e_shop_view.reply_count") }}</q-card
    >
    <!-- 一级回复 -->
    <q-card
      square
      flat
      v-for="(item, index) in commentListCopy"
      :key="item.id"
      class="flex"
      style="border-top: 1px solid #dcdcdc"
    >
      <q-card-section style="width: 100%">
        <div style="line-height: 50px">
          <q-img
            class="radius_circle q-mr-md"
            width="50px"
            height="50px"
            :src="item.user__icon"
          ></q-img>
          <span style="color: #666666" class="text-body2">{{
            item.user__nickname
          }}</span>
          <!-- 作者回复 -->
          <span
            style="
              background-color: #116fec;
              font-size: 12px;
              color: white;
              padding: 2px 3px 2px 3px;
            "
            class="q-ml-sm"
            v-show="item.user__id == this.userId"
            >{{ $t("community.e_shop_view.author") }}</span
          >
          <span style="color: #999999; margin-left: 20px">{{
            item.create_time
          }}</span>
        </div>
        <div style="margin-left: 50px">
          <div class="q-ml-md">
            <div class="text-body1 q-mb-md" v-html="item.content"></div>
            <div class="flex reply_button" v-if="isLogin">
              <img
                style="width: 16px; height: 14px"
                src="statics/comment.svg"
              />
              <div
                class="q-ml-sm"
                @click="reply(index, '', item.user__id == this.userId)"
              >
                {{ $t("community.e_shop_view.reply") }}
              </div>
            </div>
            <!-- 回复的编辑框 -->
            <div
              class="flex relative-position q-pb-xl q-pt-md"
              style="width: 100%"
              v-show="showEditor[index]"
              @mouseup="this.clickEditor = true"
            >
              <div style="width: 100%">
                <q-editor
                  :ref="'editor' + index"
                  content-class="bg-grey-1"
                  toolbar-toggle-color="primary"
                  v-model="editorText2"
                  min-height="150px"
                />
              </div>
              <div style="position: absolute; right: 0; bottom: 0">
                <q-btn
                  color="primary"
                  @click="releaseReviews(2, item, index, '')"
                  >{{ $t("community.e_shop_view.release") }}</q-btn
                >
              </div>
            </div>
            <!-- 回复评论列表的展开 -->
            <div
              v-show="item.child[0] && !showChildComment[index]"
              class="reply_button q-mt-md"
              style="font-size: 12px; display: flex; align-items: center"
              @click="viewMoreComment(index, true)"
            >
              <span style="color: #d8d8d8; margin-right: 10px">——</span>
              {{ $t("community.e_shop_view.view_more") }}
              <img style="margin-left: 5px" src="statics/pull_down.svg" />
            </div>
            <!-- 二级回复 -->
            <div style="width: 100%" v-show="showChildComment[index]">
              <q-card
                square
                flat
                v-for="(secondItem, secondIndex) in item.child"
                :key="secondIndex"
                class="flex"
              >
                <div
                  style="width: 100%; align-items: center"
                  class="q-mt-lg flex"
                >
                  <q-img
                    class="radius_circle q-mr-md"
                    width="25px"
                    height="25px"
                    :src="secondItem.user__icon"
                  ></q-img>
                  <span style="color: #666666" class="text-body2">{{
                    secondItem.user__nickname
                  }}</span>
                  <!-- 作者回复 -->
                  <span
                    style="
                      background-color: #116fec;
                      font-size: 12px;
                      color: white;
                      padding: 0 3px 0 3px;
                    "
                    class="q-ml-sm"
                    v-show="secondItem.user__id == this.userId"
                    >{{ $t("community.e_shop_view.author") }}</span
                  >
                  <!-- 回复的二级评论用户 -->
                  <div
                    class="flex"
                    style="align-items: center; color: #666666"
                    v-show="secondItem.reply !== secondItem.root"
                  >
                    <img class="q-mx-sm" src="statics/reply_to.svg" />
                    <span>{{ secondItem.reply__user__nickname }}</span>
                  </div>
                  <!-- 作者被回复 -->
                  <span
                    style="
                      background-color: #116fec;
                      font-size: 12px;
                      color: white;
                      padding: 0 3px 0 3px;
                    "
                    class="q-ml-sm"
                    v-show="secondItem.is_author"
                    >{{ $t("community.e_shop_view.author") }}</span
                  >
                  <span style="color: #999999; margin-left: 20px">{{
                    secondItem.create_time
                  }}</span>
                </div>
                <div class="q-ml-md" style="padding-left: 25px">
                  <div
                    class="text-body1 q-my-md"
                    v-html="secondItem.content"
                  ></div>
                  <div class="flex reply_button" v-if="isLogin">
                    <img
                      style="width: 16px; height: 14px"
                      src="statics/comment.svg"
                    />
                    <div
                      class="q-ml-sm"
                      @click="
                        reply(
                          index,
                          secondIndex,
                          secondItem.user__id == this.userId
                        )
                      "
                    >
                      {{ $t("community.e_shop_view.reply") }}
                    </div>
                  </div>
                </div>
                <!-- 二级回复的编辑框 -->
                <div
                  class="flex relative-position q-pb-xl q-pt-md q-pl-md"
                  style="width: 100%; margin-left: 25px"
                  v-show="index == showSecondEditor[secondIndex]"
                  @mouseup="this.clickEditor = true"
                >
                  <div style="width: 100%">
                    <q-editor
                      :ref="'secondEditor' + index + secondIndex"
                      content-class="bg-grey-1"
                      toolbar-toggle-color="primary"
                      v-model="editorText2"
                      min-height="150px"
                    />
                  </div>
                  <div style="position: absolute; right: 0; bottom: 0">
                    <q-btn
                      color="primary"
                      @click="releaseReviews(2, item, index, secondItem)"
                      >{{ $t("community.e_shop_view.release") }}</q-btn
                    >
                  </div>
                </div>
              </q-card>
            </div>
            <!-- 回复评论列表的折叠 -->
            <div
              v-show="item.child[0] && showChildComment[index]"
              style="font-size: 12px; display: flex; align-items: center"
              class="reply_button q-mt-md"
              @click="viewMoreComment(index, false)"
            >
              <span style="color: #d8d8d8; margin-right: 10px">——</span
              >{{ $t("community.e_shop_view.pull_up") }}
              <img style="margin-left: 5px" src="statics/pull_up.svg" />
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>
<script>
import { postauth } from "boot/axios";
import { reactive } from "vue";
export default {
  props: {
    commentList: "",
    userId: "",
    type: "",
  },
  data() {
    return {
      editorText1: "",
      editorText2: "",
      pluginId: "",
      showEditor: [],
      showSecondEditor: [],
      showSecondComment: [],
      showChildComment: [],
      clickEditor: false,
      replyToAuthor: false,
    };
  },
  computed: {
    isLogin() {
      if (this.$q.cookies.get("token")) {
        return true;
      } else {
        return false;
      }
    },
    commentListCopy() {
      return reactive(JSON.parse(JSON.stringify(this.commentList)));
    },
    commentNumber() {
      return this.commentListCopy.length;
    },
    headPortrait_url() {
      return this.$store.state.bbsChange.user_info.icon;
    },
    requestUrl() {
      if (this.type == "article") {
        return "/comment/api/v1/commentadd/";
      } else {
        return "software/api/v1/comment/";
      }
    },
  },
  methods: {
    //发表评论
    releaseReviews(editorIndex, item, index, secondItem) {
      this.showSecondEditor = [];
      this.showEditor = [];
      if (this[`editorText${editorIndex}`]) {
        let params =
          this.type == "article"
            ? {
                content: this[`editorText${editorIndex}`],
                article: this.pluginId,
              }
            : {
                content: this[`editorText${editorIndex}`],
                softwares: this.pluginId,
              };
        if (item.id) {
          params.root = item.id;
          if (secondItem) {
            params.reply = secondItem.id;
            params.is_author = this.replyToAuthor;
          } else {
            params.reply = item.id;
          }
        }
        postauth(this.requestUrl, params).then((res) => {
          if (item.id) {
            this.commentListCopy[index].child.unshift(res.result);
          } else {
            this.commentListCopy.unshift(reactive(res.result));
            this.commentListCopy[0].child = [];
          }
          this[`editorText${editorIndex}`] = "";
        });
      }
    },
    //回复评论
    reply(index, secondIndex, replyToAuthor) {
      this.replyToAuthor = replyToAuthor;
      if (typeof secondIndex == "number") {
        this.showSecondEditor[secondIndex] = index;
        this.$nextTick(() => {
          this.$refs["secondEditor" + index + secondIndex].focus();
        });
      } else {
        this.showEditor[index] = true;
        this.$nextTick(() => {
          this.$refs["editor" + index].focus();
        });
      }
    },
    viewMoreComment(index, val) {
      this.showChildComment[index] = val;
    },
    //关闭编辑器
    closeEditor() {
      if (this.clickEditor) {
        this.clickEditor = false;
      } else {
        this.showSecondEditor = [];
        this.showEditor = [];
      }
    },
  },
  created() {
    this.pluginId = this.$route.params.id;
    document.body.addEventListener("mouseup", this.closeEditor);
  },
  beforeDestroy() {
    document.body.removeEventListener("mouseup", this.closeEditor);
  },
};
</script>
<style lang="sass" scoped>
.reply_button
    align-items: center
    cursor: pointer
    color: #666666
    width: fit-content
    &:hover
        color: $primary
.border_top
  border-top: 1px #E6E6E6 solid
</style>
