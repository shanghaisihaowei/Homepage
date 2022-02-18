<template>
  <div>
    <q-card flat class="flex" style="align-items: center">
      <q-tabs
        v-model="plugin_type"
        align="left"
        narrow-indicator
        indicator-color="blue"
        inline-label
        style="font-size: 20px; font-weight: 500"
        class="q-py-md"
      >
        <q-tab name="GreaterWMS" no-caps
          ><span>{{ $t("community.greaterwms") }}</span></q-tab
        >
        <q-tab name="DVAdmin" no-caps
          ><span>{{ $t("community.dvadmin") }}</span></q-tab
        >
      </q-tabs>
      <q-space />
      <q-btn
        @click="this.$router.push('/market/pluginRelease/newPlugin')"
        class="q-mr-md"
        style="background-color: #116fec; min-width: 120px; height: 40px"
        ><span style="font-size: 20px; color: white">{{
          $t("community.e_shop_view.release_plugins")
        }}</span></q-btn
      >
    </q-card>
    <plugins-list
      :pluginList="plugin_list"
      :isMyPlugins="isMyPlugins"
    ></plugins-list>
    <div v-if="hasPagination" class="q-pa-md flex bg-white flex-center">
      <q-pagination
        class="q_pagination"
        direction-links
        v-model="currentPage"
        :max="maxPages"
        :max-pages="6"
      />
    </div>
    <div
      v-if="!hasPagination && plugin_list.length"
      class="flex flex-center q-mt-lg"
    >
      <q-btn flat>{{ $t("notice.nomoredata") }}</q-btn>
    </div>
    <div
      v-if="!plugin_list.length"
      style="
        height: calc(72vh);
        background-color: white;
        padding-top: 20%;
        border-top: 1px solid #e6e6e6;
      "
    >
      <div class="flex flex-center">
        <img src="statics/community/default_page.svg" />
      </div>
      <div class="q-pa-md flex flex-center default_page">
        {{ $t("community.myAccount_view.my_plugins") }}
      </div>
    </div>
  </div>
</template>
<script>
import PluginsList from "./market/components/PluginsList.vue";
import { getauth } from "boot/axios";
export default {
  components: {
    PluginsList,
  },
  data() {
    return {
      currentPage: 1,
      maxPages: 1,
      hasPagination: false,
      plugin_type: "GreaterWMS",
      plugin_list: [],
      isMyPlugins: true,
      affiliation: "",
    };
  },
  watch: {
    currentPage(val) {
      this.redirectPage(val);
    },
    plugin_type: {
      handler(val) {
        this.affiliation = val === "GreaterWMS" ? "0" : "1";
        this.getMyReleasedPlugins(this.affiliation);
      },
      immediate: true,
    },
  },
  methods: {
    getMyReleasedPlugins(val) {
      getauth(`software/api/v1/my_soft/?affiliation=${val}`).then((res) => {
        this.setOrdersList(res);
        if (res.count) {
          this.maxPages = Math.ceil(res.count / 20);
        }
      });
    },
    setOrdersList(res) {
      this.plugin_list = res.results;
      if (res.next || res.previous) {
        this.hasPagination = true;
      } else {
        this.hasPagination = false;
      }
    },
    redirectPage(page) {
      getauth(
        `software/api/v1/my_soft/?affiliation=${this.affiliation}&page=${page}`
      ).then((res) => {
        this.setOrdersList(res);
        //回到顶部
        document.getElementsByClassName(
          "q-scrollarea__container"
        )[0].scrollTop = 0;
      });
    },
  },
  mounted() {
    this.$store.dispatch("bbsChange/isIndexMenu", false);
    this.$store.dispatch("bbsChange/link", "plugin");
  },
};
</script>
