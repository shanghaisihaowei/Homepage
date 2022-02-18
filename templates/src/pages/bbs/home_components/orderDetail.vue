<template>
  <div>
    <q-card square flat style="color: #999999" class="bottom_border q-py-sm"
      ><q-btn class="text-body1" @click="this.$router.go(-1)" flat>
        &lt;{{ $t("community.e_shop_view.back") }}
      </q-btn></q-card
    >
    <q-card flat square class="bg-white q-pa-md">
      <q-card-section
        style="background-color: #e7f0fd; font-size: 18px; border-radius: 4px"
      >
        <div>
          {{ $t("community.order_detail.order_status") }}：<span
            :style="{ color: 1 ? '' : '#d60909' }"
            >{{ pluginDetail.status }}</span
          >
        </div>
        <div class="q-mt-md flex">
          {{ $t("community.order_detail.pay_mode") }}：
          <!-- <img
            v-if="pluginDetail.currency == 0"
            src="statics/weChat.svg"
          /> -->
          <img
            v-if="pluginDetail.currency == 0"
            class="q-ml-sm"
            src="statics/zfb.svg"
          /><img v-if="pluginDetail.currency == 1" src="statics/paypal.svg" />
        </div>
      </q-card-section>
      <q-card-section
        class="q-my-md flex"
        style="
          background-color: #f0f0f0;
          font-size: 18px;
          border-radius: 4px;
          justify-content: space-between;
          align-items: center;
        "
      >
        {{ $t("community.order_detail.order_info") }}
        <q-btn flat
          ><a
            :href="downloadUrl"
            v-if="pluginDetail.status == '已支付'"
            style="font-size: 18px; color: #116fec; text-decoration: underline"
            >{{ $t("community.e_shop_view.download")
            }}{{ $t("community.plugin") }}</a
          ></q-btn
        >
      </q-card-section>
      <q-card-section style="font-size: 16px; color: #333333">
        <div class="q-mb-md flex">
          <div style="min-width: 100px">
            {{ $t("community.order_detail.order_id") }}：
          </div>
          {{ pluginDetail.order_id }}
        </div>
        <div class="q-mb-md">
          <div class="flex">
            <div style="min-width: 100px">
              {{ $t("community.order_detail.plugin_info") }}：
            </div>
            <div style="max-width: calc(100% - 100px)">
              {{ pluginDetail.title }}
            </div>
          </div>
          <div
            style="
              max-width: calc(100% - 100px);
              margin-left: 100px;
              color: #666666;
            "
          >
            {{ pluginDetail.brief }}
          </div>
        </div>
        <div class="q-mb-md flex">
          <div style="min-width: 100px">
            {{ $t("community.order_detail.order_time") }}：
          </div>
          {{ pluginDetail.create_time }}
        </div>
        <div class="q-mb-md flex">
          <div style="min-width: 100px">
            {{ $t("community.order_detail.pay_time") }}：
          </div>
          {{ pluginDetail.pay_time }}
        </div>
        <div class="q-mb-lg flex">
          <div style="min-width: 100px">
            {{ $t("community.order_detail.order_amount") }}：
          </div>
          {{ pluginDetail.total_amount }}
        </div>
        <div class="q-pt-lg top_border flex" style="width: 100%">
          <div style="min-width: 100px">
            {{ $t("community.order_detail.pay_amount") }}：
          </div>
          {{ pluginDetail.total_amount }}
        </div>
      </q-card-section>
      <q-card-section
        class="text-center"
        v-if="this.pluginDetail.status == '待支付'"
      >
        <q-btn
          style="
            width: 300px;
            background-color: #116fec;
            color: white;
            display: block;
            margin: 20px auto;
            height: 30px;
            line-height: 30px;
          "
          @click="toPay"
          >{{ $t("community.order_detail.pay_now") }}</q-btn
        >
        <q-btn
          @click="this.showConfirmDialog = true"
          class="q-mb-lg"
          flat
          style="color: #999999"
          >{{ $t("community.order_detail.cancel_pay") }}</q-btn
        >
      </q-card-section>
    </q-card>
    <pay-dialog
      :showPay="showPay"
      :pluginInfo="orderDetail"
      @closeDialog="closeDialog"
    ></pay-dialog>
    <q-dialog v-model="showConfirmDialog" persistent>
      <q-card
        style="width: 470px; height: 180px; font-size: 18px; position: relative"
      >
        <q-card-section class="q-ma-md">
          <span>{{ $t("community.order_detail.cancel_tip") }}？</span>
        </q-card-section>

        <q-card-actions style="position: absolute; bottom: 0; right: 0">
          <q-btn
            flat
            style="font-size: 18px; font-weight: 500"
            :label="this.$t('index.confirm')"
            color="primary"
            v-close-popup
            @click="cancelPay"
          />
          <q-btn
            flat
            style="font-size: 18px; font-weight: 500"
            :label="this.$t('index.cancel')"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>
<script>
import PayDialog from "./market/components/PayDialog.vue";
import { getauth, deleteauth } from "boot/axios";
export default {
  components: {
    PayDialog,
  },
  data() {
    return {
      pluginDetail: {},
      pluginId: "",
      showPay: false,
      order_id: "",
      orderDetail: "",
      showConfirmDialog: false,
    };
  },
  computed: {
    downloadUrl() {
      return (
        `${window.g.BaseUrl}software/api/v1/downzip/` +
        this.pluginDetail.software +
        "/?token=" +
        this.$q.cookies.get("token")
      );
    },
  },
  methods: {
    toPay() {
      this.showPay = true;
      this.orderDetail = this.pluginDetail;
    },
    //关闭dialog
    closeDialog(val) {
      this[val] = false;
    },
    cancelPay() {
      deleteauth("order/api/v1/my_order/" + this.order_id + "/").then((res) => {
        this.$router.push({
          path: "/community/myOrders",
        });
      });
    },
    getOrderDetail() {
      getauth("order/api/v1/my_order/" + this.order_id + "/").then((res) => {
        this.pluginDetail = res;
      });
    },
  },
  created() {
    this.order_id = this.$route.params.id;
    this.getOrderDetail();
  },
};
</script>
<style scoped lang="sass">
</style>