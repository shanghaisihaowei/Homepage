<template>
  <div>
    <!-- 支付成功弹窗 -->
    <q-dialog v-model="showPaySuccess" persistent>
      <q-card style="text-align: center; width: 600px; position: relative">
        <q-btn
          flat
          icon="close"
          class="q-pa-md"
          style="position: absolute; top: 0; right: 0"
          @click="reload"
        ></q-btn>
        <q-img
          class="q-mt-lg"
          width="350px"
          src="statics/paySuccess.png"
        ></q-img>
        <div class="text-h5 text-weight-Medium q-my-lg">
          {{ $t("community.e_shop_view.pay_success") }}
        </div>
        <div class="text-body1">
          {{ $t("community.e_shop_view.pay_success_text") }}
        </div>
        <q-btn
          @click="reload"
          class="q-my-lg"
          style="width: 150px"
          color="primary"
          >{{ $t("community.e_shop_view.ok") }}（{{ dialogCountdown }}）</q-btn
        >
      </q-card>
    </q-dialog>
    <!-- 支付弹窗 -->
    <q-dialog v-model="showPay" persistent>
      <q-card style="width: 600px; position: relative">
        <q-btn
          flat
          icon="close"
          class="q-pa-md"
          style="position: absolute; top: 0; right: 0; z-index: 1"
          @click="this.$parent.closeDialog('showPay')"
        ></q-btn>
        <q-card-section class="text-h6 bottom_border">{{
          $t("community.e_shop_view.buy_plugin")
        }}</q-card-section>
        <q-card-section class="text-body1 flex">
          <div>{{ $t("community.e_shop_view.plugin_name") }}：</div>
          <div class="q-ml-md" style="flex: 1">
            {{ pluginInfo.title }}
          </div>
        </q-card-section>
        <q-card-section class="text-body1 flex">
          <div>{{ $t("community.e_shop_view.plugin_des") }}：</div>
          <div class="q-ml-md" style="flex: 1">
            {{ pluginInfo.brief }}
          </div>
        </q-card-section>
        <q-card-section class="text-body1 flex" style="align-items: center">
          <div>{{ $t("community.e_shop_view.order_amount") }}：</div>
          <div class="q-ml-md text-h6 text-red my-font-D">
            {{ isDollar ? "$" : "￥" }}{{ pluginInfo.total_amount }}
          </div>
        </q-card-section>
        <q-card-section class="flex">
          <div class="pay_code">
            <!-- <div>
              <q-btn
                v-show="!isDollar"
                align="left"
                outline
                @click="showPayCode(0)"
                style="color: #09bb07"
                class="button_visited"
              >
                <img
                  style="width: 15px"
                  src="statics/weChat.svg"
                  class="q-mr-sm"
                />
                {{ $t("community.e_shop_view.pay_weChat") }}</q-btn
              >
            </div> -->
            <div>
              <q-btn
                v-show="!isDollar"
                align="left"
                outline
                class="button q-my-lg"
                @click="showPayCode(1)"
                style="color: #02a9f1"
              >
                <img
                  style="width: 15px"
                  src="statics/zfb.svg"
                  class="q-mr-sm"
                />{{ $t("community.e_shop_view.pay_zfb") }}</q-btn
              >
            </div>
            <div>
              <q-btn
                v-show="isDollar"
                align="left"
                outline
                @click="showPayCode(2)"
                class="button"
              >
                <img
                  style="width: 15px"
                  src="statics/paypal.svg"
                  class="q-mr-sm"
                />
                <img
                  style="height: 15px"
                  src="statics/paypalText.svg"
                  class="q-mr-sm"
                />
              </q-btn>
            </div>
          </div>
          <!-- <div class="q-ml-xl" style="flex: 1" v-show="payCode">
            <div
              style="
                width: 100%;
                background: #09bb07;
                text-align: center;
                border-radius: 4px;
              "
              class="q-pa-md"
            >
              <div class="q-pb-sm text-white">
                {{ $t("community.e_shop_view.pay_count_down") }}：{{
                  minutes
                }}
                : {{ seconds }}
              </div>
              <div style="position: relative">
                <div
                  v-if="seconds == 0 && minutes == 0"
                  style="
                    width: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    padding-top: 100%;
                    position: absolute;
                    color: white;
                    cursor: pointer;
                  "
                  @click="getWeChatPayCode()"
                >
                  <div
                    style="
                      position: absolute;
                      width: 100%;
                      text-algin: center;
                      font-size: 16px;
                      top: 42%;
                    "
                  >
                    {{ $t("community.e_shop_view.qrcode_overdue") }}
                  </div>
                </div>
                <img :src="payCode" style="width: 100%" />
              </div>
            </div>
            <div
              style="color: #113984; text-align: center"
              class="text-body1 q-mt-sm"
            >
              {{ $t("community.e_shop_view.pay_weChat_prompt") }}
            </div>
          </div> -->
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
<script>
import { defineComponent, ref, watch, onBeforeUnmount } from "vue";
import { getauth, postauth } from "boot/axios";
export default defineComponent({
  props: {
    showPay: Boolean,
    pluginInfo: "",
  },
  setup(props, context) {
    const { emit } = context;
    let payCode = ref();
    let isDollar = ref();
    let timer = ref();
    let showPaySuccess = ref(false);
    let minutes = ref();
    let seconds = ref();
    let timeInterval;
    let dialogInterval;
    let dialogCountdown = ref(5);
    //清空二维码和微信支付的选中格式
    watch(
      () => props.pluginInfo,
      (val) => {
        if (val) {
          if (val.currency == 1) {
            isDollar.value = true;
          } else {
            isDollar.value = false;
            payCode.value = "";
            // getWeChatPayCode();
          }
        }
      }
    );
    //展示响应选择方式的支付二维码
    function showPayCode(visited_index) {
      switch (visited_index) {
        case 0:
          getWeChatPayCode();
          break;
        case 1:
          getAlipayCode();
          break;
        case 2:
          PaypalPay();
          break;
      }
    }
    //获取微信支付二维码
    function getWeChatPayCode() {
      postauth("order/api/v1/wx_pay/", {
        order_id: props.pluginInfo.order_id,
      }).then((res) => {
        var QRCode = require("qrcode");
        QRCode.toDataURL(res.img_url, [
          {
            errorCorrectionLevel: "H",
            mode: "byte",
            version: "2",
            type: "image/jpeg",
          },
        ])
          .then((url) => {
            payCode.value = url;
          })
          .catch((err) => {
            console.error(err);
          });
        payCountdown();
        //获取微信二维码后轮询支付状态
        loopPayStatus("wx");
      });
    }
    //获取支付宝支付二维码
    function getAlipayCode() {
      getauth(
        "order/api/v1/zfb_pay/?order_id=" + props.pluginInfo.order_id
      ).then((res) => {
        emit("closeDialog", "showPay");
        window.open(res.result.alipay_url);
      });
    }
    //paypal支付
    function PaypalPay() {
      getauth(
        "order/api/v1/pay_pay/?order_id=" + props.pluginInfo.order_id
      ).then((res) => {
        window.open(res.url);
        //获取微信二维码后轮询支付状态
        payCountdown();
        loopPayStatus("paypal");
      });
    }
    //获取支付状态
    function getPayStatus(mode) {
      let url;
      if (mode === "wx") {
        url = "order/api/v1/wx_back/?out_trade_no=" + props.pluginInfo.order_id;
      } else {
        url = "order/api/v1/paystatus/?order_id=" + props.pluginInfo.order_id;
      }
      getauth(url).then((res) => {
        if (res.msg === "ok") {
          clearInterval(timer);
          emit("closeDialog", "showPay");
          closeDialogTime();
        }
      });
    }
    //轮询支付状态
    function loopPayStatus(mode) {
      //清空上次的轮询
      clearInterval(timer);
      timer = setInterval(() => {
        getPayStatus(mode);
      }, 5000);
    }
    //支付倒计时
    function payCountdown() {
      clearInterval(timeInterval);
      seconds.value = 59;
      minutes.value = 4;
      timeInterval = setInterval(() => {
        if (seconds.value == 0) {
          minutes.value = minutes.value - 1;
          seconds.value = 59;
        } else {
          seconds.value = seconds.value - 1;
        }
        if (minutes.value == 0 && seconds.value == 0) {
          clearInterval(timeInterval);
          clearInterval(timer);
        }
      }, 1000);
    }
    //支付成功的弹窗倒计时关闭
    function closeDialogTime() {
      showPaySuccess.value = true;
      dialogInterval = setInterval(() => {
        dialogCountdown.value = dialogCountdown.value - 1;
        if (dialogCountdown.value == 0) {
          clearInterval(dialogInterval);
          showPaySuccess.value = false;
        }
      }, 1000);
    }
    function reload() {
      showPaySuccess.value = false;
    }
    onBeforeUnmount(() => {
      clearInterval(timer);
      clearInterval(dialogInterval);
      clearInterval(timeInterval);
    });
    return {
      showPayCode,
      payCode,
      isDollar,
      showPaySuccess,
      minutes,
      seconds,
      dialogCountdown,
      reload,
      getWeChatPayCode,
      closeDialogTime,
    };
  },
});
</script>
<style scoped lang="sass">
.button
    width: 220px
    padding-left: 65px
.button_visited
    width: 220px
    padding-left: 65px
    border: 1px solid #116FEC
</style>
