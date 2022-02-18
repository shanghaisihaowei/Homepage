<template>
  <div class="plugins_view_container">
    <q-card flat square class="header_container flex">
      <q-card-section style="padding-top: 0; padding-bottom: 0"
        ><q-select
          class="header"
          borderless
          v-model="sortordVal"
          :options="sortordOptions"
      /></q-card-section>
      <q-card-section
        v-if="this.$q.cookies.get('token')"
        style="padding: 0 16px 0 0"
        class="flex flex-center"
        ><q-btn
          @click="this.$router.push('/market/pluginRelease/newPlugin')"
          color="primary"
          >{{ $t("community.e_shop_view.release_plugins") }}</q-btn
        ></q-card-section
      >
    </q-card>
    <plugins-list :pluginList="pluginList" ref="pluginsList"></plugins-list>
    <div v-if="hasPagination" class="q-pa-md flex bg-white flex-center">
      <q-pagination
        class="q_pagination"
        direction-links
        v-model="currentPage"
        :max="maxPages"
        :max-pages="6"
      />
    </div>
    <div class="flex flex-center q-mt-lg" v-if="!hasPagination">
      <q-btn flat>{{ $t("notice.nomoredata") }}</q-btn>
    </div>
  </div>
</template>

<script>
import PluginsList from "./components/PluginsList";
import { get } from "boot/axios";
import { createMetaMixin } from "quasar";

export default {
  components: {
    PluginsList,
  },
  data() {
    return {
      head_title: "",
      meta: "",
      pluginList: [],
      sortordVal: this.$t("community.e_shop_view.sort_download"),
      sortordOptions: [
        this.$t("community.e_shop_view.sort_download"),
        this.$t("community.e_shop_view.sort_free"),
        this.$t("community.e_shop_view.sort_pay"),
      ],
      currentPage: 1,
      hasPagination: false,
      maxPages: 1,
      affiliation: "",
    };
  },
  watch: {
    currentPage(val) {
      this.redirectPage(val);
    },
    sortordVal(val) {
      for (let [index, item] of this.sortordOptions.entries()) {
        if (item === val) {
          this.changeSortord(index);
          break;
        }
      }
    },
    $route: {
      handler(val) {
        this.affiliation = val.params.belong === "GreaterWMS" ? 0 : 1;
        if (val.params.belong === "GreaterWMS") {
          this.$store.dispatch("bbsChange/logo", "img:statics/logo_black.svg");
          this.$store.dispatch("bbsChange/titletype", "GreaterWMS");
        } else {
          this.$store.dispatch("bbsChange/logo", "img:statics/DV_logo.svg");
          this.$store.dispatch("bbsChange/titletype", "DVAdmin");
        }
        this.getPlginsList();
        this.$nextTick(() => {
          this.setHtmlTitle(val.params.belong);
        });
      },
      immediate: true,
      deep: true,
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
  methods: {
    //设置插件列表和分页
    setPluginsList(res) {
      this.pluginList = res.results;
      if (res.next || res.previous) {
        this.hasPagination = true;
      } else {
        this.hasPagination = false;
      }
    },
    //获取插件列表
    getPlginsList() {
      get("software/api/v1/softwareget/?affiliation=" + this.affiliation).then(
        (res) => {
          this.setPluginsList(res);
          if (res.count) {
            this.maxPages = Math.ceil(res.count / 20);
          }
        }
      );
    },
    //换页
    redirectPage(page) {
      get(
        "software/api/v1/softwareget/?affiliation=" +
          this.affiliation +
          "&page=" +
          page
      ).then((res) => {
        this.setPluginsList(res);
        //回到顶部
        document.getElementsByClassName(
          "q-scrollarea__container"
        )[0].scrollTop = 0;
      });
    },
    //更换排序方式
    changeSortord(index) {
      let requsetUrl;
      switch (index) {
        case 0:
          requsetUrl = "software/api/v1/softwareget/?ordering=-people_buy";
          break;
        case 1:
          requsetUrl = "software/api/v1/softwareget/?release_form=0";
          break;
        case 2:
          requsetUrl = "software/api/v1/softwareget/?release_form=1";
          break;
      }
      get(requsetUrl).then((res) => {
        this.setPluginsList(res);
        this.maxPages = Math.ceil(res.count / 20);
      });
    },
    //更改网页title
    setHtmlTitle(type) {
      if (this.$q.cookies.get("lang") === "zh-hans") {
        this.head_title =
          type === "GreaterWMS"
            ? "GreaterWMS - 插件市场"
            : "DVAdmin - 插件市场";
        this.meta = {
          description: {
            name: "description",
            content:
              type === "GreaterWMS"
                ? "GreaterWMS"
                : "DVAdmin" + " - Open Source Warehouse Management System",
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
              return ogTitle + type === "GreaterWMS"
                ? " - GreaterWMS"
                : " - DVAdmin";
            },
          },
        };
      } else {
        this.head_title =
          type === "GreaterWMS" ? "GreaterWMS - Market" : "DVAdmin - Market";
        this.meta = {
          description: {
            name: "description",
            content:
              type === "GreaterWMS"
                ? "GreaterWMS"
                : "DVAdmin" + " - Open Source Warehouse Management System",
          },
          keywords: {
            name: "keywords",
            content:
              type === "GreaterWMS"
                ? "GreaterWMS"
                : "DVAdmin" +
                  " - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms",
          },
          equiv: {
            "http-equiv": "Content-Type",
            content: "text/html; charset=UTF-8",
          },
          ogTitle: {
            property: "og:title",
            template(ogTitle) {
              return ogTitle + type === "GreaterWMS"
                ? " - GreaterWMS"
                : " - DVAdmin";
            },
          },
        };
      }
    },
  },
  mounted() {
    this.$refs.pluginsList.showBtnHandler(false);
  },
};
</script>

<style scoped lang="sass">
.header_container
    height: 70px
    align-items: center
    justify-content: space-between
    border-bottom: 1px solid #dcdcdc
    .header
        font-size: 18px
</style>
