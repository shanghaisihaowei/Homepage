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
      <q-card-section class="col-10">
        <div class="flex row" style="align-items: center">
          <div :class="{'plugin_des_detail col-12':showBtn,'plugin_des col-9':!showBtn,'plugin_des col-12':item.soft_label !== 2}" style="font-size: 16px; font-weight: 600">
            {{ item.name }}
          </div>
          <div
            class="q-ml-sm col-2"
            style="
              font-size: 12px;
              background-color: #116fec;
              color: white;
              padding: 0 7px;
              border-radius: 4px;
            "
            v-if="item.soft_label === 2"
          >
            {{ $t("community.e_shop_view.official") }}
          </div>
        </div>
        <div
          style="font-size: 14px; color: #666666"
          :class="showBtn ? 'q-my-md plugin_des_detail' : 'q-my-md plugin_des'"
        >
          {{ item.brief }}
        </div>
        <div style="margin-left: -10px;margin-top: -10px" class="flex q-mb-md">
          <q-btn
            v-for="(tab, index) in item.tab"
            :key="index"
            padding="xs"
            class="text-blue"
            unelevated
            color="cyan-1"
            style="max-width: 140px;margin-left: 10px;padding: 5px 10px;margin-top: 10px"
            ><span style="font-size: 13px;" class="plugin_des">{{ tab.tab_name }}</span></q-btn
          >
        </div>
        <div class="flex" style="align-items: center">
          <q-img
            class="head_portrait"
            width="22px"
            height="22px"
            :src="item.user.icon"
          />
          <div class="q-ml-sm" style="color: #999999">
            {{ $t("community.e_shop_view.createTime") }}
            {{ item.create_time }}
          </div>
        </div>
      </q-card-section>
      <q-card-section class="col-2" style="padding-left: 0">
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
        <div style="font-size: 18px; margin-top: 43px">
          <div
            style="color: #116fec; font-weight: 600"
            v-if="item.release_form == 0"
          >
            {{ $t("community.e_shop_view.sort_free") }}
          </div>
          <div
            style="font-size: 16px; color: #d51717; font-weight: 600"
            v-if="item.release_form != 0"
          >
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
            >{{ $t("community.e_shop_view.sort_download") }}：{{
              item.number_downloads
            }}</span
          >
          <q-btn
            flat
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
          <div class="q-ml-md" style="color: #999999" v-if="isMyPlugins">
            <span
              @click.stop="
                this.$router.push({
                  path: `/market/pluginRelease/${item.id}`,
                })
              "
              >{{ $t("community.e_shop_view.editor") }}</span
            >
            <span v-if="item.check === '审核已通过'" class="q-px-sm">/</span>
            <span
              v-if="item.check === '审核已通过'"
              @click.stop="
                this.$router.push({
                  path: `/market/pluginUpdate/${item.id}`,
                })
              "
              >{{ $t("community.e_shop_view.update") }}</span
            >
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import { postauth } from "boot/axios";
export default defineComponent({
  props: {
    pluginList: "",
    isFree: "",
    alreadyBought: "",
    isMyPlugins: "",
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
        path: `/community/mobile/pluginsDetail/${id}`,
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
