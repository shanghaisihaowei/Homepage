<template>
  <div class="plugList_view_container">
    <q-card
      flat
      square
      :class="[showBtn ? '' : 'top_border', 'row', 'relative-position']"
      v-for="item in pluginList"
      :key="item.id"
      @click="
        showBtn || item.check == '未审核' || item.check == '审核未通过'
          ? ''
          : goPluginDetail(item.id)
      "
      :style="{ cursor: showBtn ? 'default' : 'pointer' }"
    >
      <q-card-section class="col-1">
        <q-img
          class="head_portrait"
          width="60px"
          height="60px"
          :src="item.user.icon"
        />
      </q-card-section>
      <q-card-section class="col-9">
        <p class="text-h6 text-weight-bold">{{ item.name }}</p>
        <p
          class="text-body1"
          :class="showBtn ? 'plugin_des_detail' : 'plugin_des'"
        >
          {{ item.brief }}
        </p>
        <div class="flex q-mb-md">
          <q-btn
            v-for="(tab, index) in item.tab"
            :key="index"
            class="text-blue q-mr-sm"
            unelevated
            color="cyan-1"
            >{{ tab.tab_name }}</q-btn
          >
        </div>
        <p style="margin: 0; color: #999999">
          {{ $t("community.e_shop_view.createTime") }}
          {{ item.create_time }}
        </p>
      </q-card-section>
      <q-card-section class="col-2">
        <div
          v-if="item.check == '未审核' || item.check == '审核未通过'"
          :style="
            item.check == '未审核'
              ? {
                  fontSize: '16px',
                  color: '#f79d00',
                  border: '1px solid #f79d00',
                  width: 'fit-content',
                  float: 'right',
                }
              : {
                  fontSize: '16px',
                  color: '#E53A3A',
                  border: '1px solid #E53A3A',
                  width: 'fit-content',
                  float: 'right',
                }
          "
          class="q-px-sm"
        >
          {{
            item.check == "未审核"
              ? $t("community.myorder.no_auditing")
              : $t("community.myorder.audit_failed")
          }}
        </div>
        <div style="clear: both"></div>
        <div
          class="text-red my-font-D"
          style="font-size: 20px; margin-top: 43px; float: right"
        >
          <div style="color: #116fec" v-if="item.release_form == 0">
            {{ $t("community.e_shop_view.sort_free") }}
          </div>
          <div v-if="item.release_form != 0">
            {{ item.dollar ? "$" : "￥"
            }}{{ item.dollar ? item.dollar : item.rnb }}
          </div>
        </div>
      </q-card-section>
      <q-card-section
        class="flex"
        style="position: absolute; bottom: 0; right: 0; color: #666666"
      >
        <div class="flex" style="align-items: center">
          <img
            style="margin-right: 3px"
            v-if="isMyPlugins"
            src="statics/wallet.svg"
          />
          <span v-if="isMyPlugins" class="q-mr-md"
            >{{ $t("community.e_shop_view.current_earnings") }}：<span
              style="color: #d51717"
              >{{ item.earnings }}</span
            ></span
          >
          <img style="margin-right: 3px" src="statics/download.svg" />
          <span
            >{{ $t("community.e_shop_view.download_count") }}：{{
              item.number_downloads
            }}</span
          >
          <q-btn
            v-if="item.release_form"
            v-show="showBtn"
            :color="alreadyBought ? 'grey' : 'primary'"
            class="q-ml-md"
            :disabled="alreadyBought"
            @click="buyPlugin"
            >{{
              alreadyBought
                ? $t("community.e_shop_view.bought")
                : $t("community.e_shop_view.buy_now")
            }}</q-btn
          >
          <!-- 编辑和更新 -->
          <!-- <div class="q-ml-md" style="color: #999999" v-if="isMyPlugins">
            <span
              @click.stop="
                this.$router.push({
                  path: `/market/pluginRelease/${item.id}`,
                })
              "
              >{{ $t("community.e_shop_view.editor") }}</span
            >
            <span class="q-px-sm">/</span>
            <span
              @click.stop="
                this.$router.push({
                  path: `/market/pluginUpdate/${item.id}`,
                })
              "
              >{{ $t("community.e_shop_view.update") }}</span
            >
          </div> -->
        </div>
      </q-card-section>
    </q-card>
    <pay-dialog
      @closeDialog="closeDialog"
      :showPay="showPay"
      :pluginInfo="pluginInfo"
    ></pay-dialog>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import PayDialog from "./PayDialog";
import { getauth, postauth } from "boot/axios";
export default defineComponent({
  props: {
    pluginList: "",
    isFree: "",
    alreadyBought: "",
    isMyPlugins: "",
  },
  components: {
    PayDialog,
  },
  data() {
    return {
      showBtn: false,
      showPay: false,
      pluginInfo: "",
    };
  },
  methods: {
    showBtnHandler(val) {
      this.showBtn = val;
    },

    //跳转插件详情页
    goPluginDetail(id) {
      this.$router.push({
        path: `/market/pluginDetail/${id}`,
      });
    },
    //关闭dialog
    closeDialog(val) {
      this[val] = false;
    },
    //点击立即购买生成订单
    buyPlugin() {
      if (this.$q.cookies.get("token")) {
        postauth("order/api/v1/order/", {
          title: this.pluginList[0].name,
          total_count: "1",
          total_amount: this.pluginList[0].dollar
            ? this.pluginList[0].dollar
            : this.pluginList[0].rnb,
          software: this.pluginList[0].id,
          currency: this.pluginList[0].dollar ? 1 : 0,
        }).then((res) => {
          if (!res.code) {
            this.pluginInfo = res;
            this.showPay = true;
          }
        });
      } else {
        this.$store.dispatch("bbsChange/toLoginChange", true);
      }
    },
  },
});
</script>
<style scoped lang="sass">
.head_portrait
    border-radius: 50%
.plugin_des_detail
    letter-spacing: 1px
.plugin_des
    letter-spacing: 1px
    white-space: nowrap
    text-overflow: ellipsis
    overflow: hidden
</style>