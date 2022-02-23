<template>
  <div class="bg-white">
    <q-card square flat style="color: #999999" class="bottom_border q-py-md"
      ><q-btn class="text-body1" @click="this.$router.go(-1)" flat>
        &lt;{{ $t("community.e_shop_view.back") }}
      </q-btn></q-card
    >
    <plugins-list
      :isFree="isFree"
      :alreadyBought="alreadyBought"
      :pluginList="pluginList"
      ref="pluginsList"
    ></plugins-list>
    <div class="q-px-md">
      <q-card square flat class="q-py-md top_border text-h6">{{
        $t("community.e_shop_view.download")
      }}</q-card>
    </div>
    <a
      target="_blank"
      :href="downloadUrl"
      @click="checkDownloadStatus($event)"
      :style="{
        height: '70px',
        fontSize: '24px',
        backgroundImage: imageUrl,
        background: 'noRepeat',
        backgroundSize: '100%',
        cursor: 'pointer',
        textDecoration: 'none',
      }"
      class="text-white q-mx-md flex flex-center"
    >
      <div style="color: white" v-if="isFree">
        {{ $t("community.e_shop_view.click_download") }}
      </div>
      <div v-if="!isFree" style="color: white">
        {{
          alreadyBought
            ? $t("community.e_shop_view.download_btn_text")
            : $t("community.e_shop_view.unbought_btn_text")
        }}
      </div></a
    >
    <q-card square flat class="text-h6 q-px-md q-pt-lg">{{
      $t("community.e_shop_view.update_record")
    }}</q-card>
    <!-- 更新时间线 -->
    <timeline :timeline="timeline"></timeline>
    <!-- 插件介绍 -->
    <q-card square flat class="text-h6 q-px-md">{{
      $t("community.e_shop_view.plugin_introduce")
    }}</q-card>
    <div
      class="markdown q-px-md q-pt-md text-body1"
      v-html="pluginList[0].direction_for_use"
    ></div>
    <!-- 添加评论 -->
    <q-card square flat class="text-h6 q-px-md q-pt-lg">{{
      $t("community.e_shop_view.add_comment")
    }}</q-card>
    <comment-list :commentList="commentList" :userId="userId"></comment-list>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import PluginsList from "./components/PluginsList";
import Timeline from "./components/Timeline.vue";
import CommentList from "./components/CommentList.vue";
import { get, getauth } from "boot/axios";
export default defineComponent({
  components: {
    PluginsList,
    CommentList,
    Timeline,
  },
  data() {
    return {
      pluginId: "",
      userId: "",
      pluginList: [{ brief: "", user: { icon: "" } }],
      timeline: "",
      commentList: [],
      alreadyBought: false,
    };
  },
  computed: {
    imageUrl() {
      if (this.alreadyBought || this.isFree) {
        return "url('statics/purchased.svg')";
      } else {
        return "url('statics/unpurchased.svg')";
      }
    },

    isFree() {
      if (this.pluginList[0].dollar == 0 && this.pluginList[0].rnb == 0) {
        return true;
      } else {
        return false;
      }
    },
    downloadUrl() {
      return (
        `${window.g.BaseUrl}software/api/v1/downzip/` +
        this.pluginId +
        "/?token=" +
        this.$q.cookies.get("token")
      );
    },
  },
  methods: {
    //获取插件详情
    getPluginDetail() {
      get("software/api/v1/softwaregetret/" + this.pluginId + "/").then(
        (res) => {
          this.pluginList = [];
          this.pluginList.push(res);
          this.timeline = res.versions;
          this.commentList = res.comment;
          this.userId = res.user.id;
        }
      );
    },
    //查看用户是否已经购买插件
    changeBuyStatus() {
      if (this.$q.cookies.get("token")) {
        getauth("order/api/v1/order_status/?software=" + this.pluginId).then(
          (res) => {
            if (res.status) {
              this.alreadyBought = true;
            } else {
              this.alreadyBought = false;
            }
          }
        );
      }
    },
    //取消a标签的跳转
    checkDownloadStatus(e) {
      if (!this.alreadyBought && !this.isFree) {
        e.preventDefault();
      } else {
        if (this.isFree && !this.$q.cookies.get("token")) {
          e.preventDefault();
          this.$q.notify({
            message: this.$t("community.e_shop_view.unlogin_tip"),
            icon: "close",
            color: "negative",
          });
          this.$store.dispatch("bbsChange/toLoginChange", true);
        }
      }
    },
  },
  created() {
    this.pluginId = this.$route.params.id;
    this.changeBuyStatus();
    this.getPluginDetail();
    document.body.scrollTop = 0;
  },
  mounted() {
    this.$refs.pluginsList.showBtnHandler(true);
  },
});
</script>

