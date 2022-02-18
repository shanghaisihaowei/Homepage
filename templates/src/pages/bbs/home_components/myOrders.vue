<template>
  <div class="bg-white" style="clolr: #333333; min-height: calc(80vh)">
    <q-card flat>
      <q-tabs
        v-model="plugin_order"
        align="left"
        narrow-indicator
        indicator-color="blue"
        inline-label
        style="font-size: 20px; font-weight: 500"
        class="q-py-md"
      >
        <q-tab name="GreaterWMS" no-caps
          ><span
            >{{ $t("community.greaterwms")
            }}{{ $t("community.myorder.order") }}</span
          ></q-tab
        >
        <q-tab name="DVAdmin" no-caps
          ><span
            >{{ $t("community.dvadmin")
            }}{{ $t("community.myorder.order") }}</span
          ></q-tab
        >
      </q-tabs>
      <q-card-section class="background-grey row" style="font-size: 18px">
        <span class="col-6">{{ $t("community.myorder.order_detail") }}</span>
        <span class="col-2 text-center">{{
          $t("community.myorder.amount")
        }}</span>
        <span class="col-2 text-center">{{
          $t("community.myorder.status")
        }}</span>
        <span class="col-2 text-center">{{
          $t("community.myorder.operation")
        }}</span>
      </q-card-section>
      <div
        style="font-size: 16px; cursor: pointer"
        v-for="item in myOrdersList"
        :key="item.order_id"
        @click="this.$router.push(`/community/orderDetail/${item.order_id}`)"
      >
        <div class="background-grey q-pa-md q-mt-lg">
          <span>{{ item.order_id }}</span>
          <span class="q-ml-xl" style="color: #999999"
            >{{ $t("community.myorder.buy_time") }}：{{ item.pay_time }}</span
          >
        </div>
        <div class="bottom_border row q-px-md">
          <span class="plugins_list col-6" style="font-weight: 500">{{
            item.title
          }}</span>
          <span
            class="plugins_list col-2 text-center"
            style="border-left: 1px solid #dcdcdc"
            >{{ item.total_amount }}</span
          >
          <span
            class="plugins_list col-2 text-center"
            :style="{
              borderLeft: '1px solid #dcdcdc',
              color: 1 ? '' : '#D60909',
            }"
            >{{ item.status }}</span
          >
          <a
            v-if="item.status == '已支付'"
            :href="downloadUrl"
            @click.stop="this.pluginId = item.software"
            class="plugins_list col-2 text-center"
            style="border-left: 1px solid #dcdcdc; color: #116fec"
            >{{ $t("community.e_shop_view.download") }}</a
          >
          <span
            v-if="item.status != '已支付'"
            class="plugins_list col-2 text-center"
            style="border-left: 1px solid #dcdcdc; color: #999999"
            >{{ $t("community.myorder.pre_buy") }}</span
          >
        </div>
      </div>
      <q-card-section>
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
          v-if="!hasPagination && myOrdersList.length"
          class="flex flex-center q-mt-lg"
        >
          <q-btn flat>no more data</q-btn>
        </div>
        <div v-if="!myOrdersList.length" style="margin-top: 20%">
          <div class="flex flex-center">
            <img src="statics/community/default_page.svg" />
          </div>
          <div class="q-pa-md flex flex-center default_page">
            {{ $t("community.myAccount_view.my_orders") }}
          </div>
        </div>
      </q-card-section>
    </q-card>
    <pay-dialog ref="dialog"></pay-dialog>
  </div>
</template>
<script>
import { getauth } from "boot/axios";
import PayDialog from "./market/components/PayDialog.vue";
export default {
  components: {
    PayDialog,
  },
  data() {
    return {
      plugin_order: "GreaterWMS",
      myOrdersList: [],
      currentPage: 1,
      maxPages: 1,
      hasPagination: false,
      pluginId: "",
      order_type: "",
    };
  },
  computed: {
    downloadUrl() {
      return (
        `${window.g.BaseUrl}software/api/v1/downzip/` +
        this.pluginId +
        "/?token=" +
        this.$q.cookies.get("token")
      );
    },
  },
  watch: {
    currentPage(val) {
      this.redirectPage(val);
    },
    plugin_order: {
      handler(val) {
        this.order_type = val === "GreaterWMS" ? "0" : "1";
        this.getOrderList(this.order_type);
      },
      immediate: true,
    },
  },
  methods: {
    getOrderList(val) {
      getauth("order/api/v1/my_order/?affiliation=" + val).then((res) => {
        this.setOrdersList(res);
        if (res.count) {
          this.maxPages = Math.ceil(res.count / 20);
        }
      });
    },
    //设置插件列表和分页
    setOrdersList(res) {
      this.myOrdersList = res.results;
      if (res.next || res.previous) {
        this.hasPagination = true;
      } else {
        this.hasPagination = false;
      }
    },
    redirectPage(page) {
      getauth(
        `order/api/v1/my_order/?affiliation=${this.order_type}&page=${page}`
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
    this.$store.dispatch("bbsChange/link", "order");
    if (location.href.indexOf("out_trade_no") != -1) {
      this.$refs.dialog.closeDialogTime();
      location.href = location.href.split("?")[0];
    }
  },
};
</script>
<style scoped lang="sass">
.background-grey
    background-color: #f2f2f2
.plugins_list
    height: 100px
    line-height: 100px
a
    text-decoration: none
</style>
