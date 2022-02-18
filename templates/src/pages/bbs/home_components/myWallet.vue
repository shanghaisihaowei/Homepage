<template>
  <div>
    <!--  顶部资金分类-->
    <q-card class="top_card" flat>
      <q-tabs
        style="height: 78px"
        inline-label
        v-model="currency"
        align="left"
        narrow-indicator
        indicator-color="blue"
      >
        <q-tab name="rmb" class="details" no-caps>
          {{ $t("community.mywallet.rnb_wallet") }}
        </q-tab>
        <q-tab name="dollar" class="details" no-caps>
          {{ $t("community.mywallet.dollar_wallet") }}
        </q-tab>
        <q-space/>

        <!--        提现按钮-->
        <!--        人民币提现-->
        <q-btn
          v-if="currency === 'rmb'"
          @click="withdraw()"
          flat
          dense
          class="withdraw q-mr-md"
          no-caps
        >
          {{ $t("community.mywallet.withdraw") }}
        </q-btn>
        <!--        美元提现-->
        <q-btn
          v-if="currency !== 'rmb'"
          flat
          @click="withdraw_foreign()"
          dense
          class="withdraw q-mr-md"
          no-caps
        >
          {{ $t("community.mywallet.withdraw") }}
        </q-btn>
      </q-tabs>

      <q-separator/>

      <q-card-section class="row" horizontal style="height: 180px">
        <!--        总收入-->
        <q-card-section class="col-4">
          <span>
            <img
              class="icon_top"
              src="statics/person_center/total_revenue.svg"
            />
          </span>
          <span class="tit_top my-font">
            {{
              $t("community.mywallet.total_revenue")
            }}<span>{{ currency === "rmb" ? "(￥)" : "($)" }}：</span>
          </span>
          <div class="number_amount text-center my-font-D">
            {{ walletDetails.balance }}
          </div>
        </q-card-section>

        <q-separator vertical/>
        <!--        可提现-->
        <q-card-section class="col-4">
          <span>
            <img class="icon_top" src="statics/person_center/withdraw.svg"/>
          </span>
          <span class="tit_top my-font">
            {{
              $t("community.mywallet.withdrawnable")
            }}<span>{{ currency === "rmb" ? "(￥)" : "($)" }}：</span>
          </span>
          <!--          感叹号-->
          <span>
            <img
              class="icon_top"
              src="statics/person_center/tip.svg"
              style="margin-top: 5px"
            />
            <q-tooltip self="bottom right" :offset="[10, -30]">
              {{ $t("community.mywallet.tooltip2") }}
            </q-tooltip>
          </span>
          <!--          提现说明-->
          <span
            class="w_ins"
            @click="this.$router.push('/community/withdrawal_instructions')"
          >
            {{ $t("community.mywallet.w_ins") }}
          </span>
          <div class="number_amount text-center my-font-D">
            <span class="tixian" @click="withdraw()">
              {{ walletDetails.withdrawal_amount }}
            </span>
          </div>
        </q-card-section>

        <q-separator vertical/>
        <!--        月累计提现-->
        <q-card-section class="col-4">
          <span>
            <img class="icon_top" src="statics/person_center/income.svg"/>
          </span>
          <span class="tit_top my-font">
            {{
              $t("community.mywallet.mcw")
            }}<span>{{ currency === "rmb" ? "(￥)" : "($)" }}：</span>
          </span>
          <div class="number_amount text-center my-font-D">
            {{ withdraw_monthly }}
          </div>
        </q-card-section>
      </q-card-section>
    </q-card>

    <q-card class="sed_card top_border" flat>
      <q-tabs
        style="height: 78px"
        inline-label
        v-model="tab"
        align="left"
        narrow-indicator
        indicator-color="blue"
      >
        <q-tab
          icon="img:statics/person_center/withdraw_det.svg"
          name="one"
          no-caps
        >
          <span class="details q-ml-sm">
            {{ $t("community.mywallet.withdraw_detail") }}</span
          >
        </q-tab>
        <q-tab
          class="details"
          icon="img:statics/person_center/income_det.svg"
          name="two"
          no-caps
        >
          <span class="details q-ml-sm">
            {{ $t("community.mywallet.earnings_detail") }}</span
          >
        </q-tab>
        <q-space/>
        <!-- 功能暂未开发，暂时隐藏按钮 -->
        <q-btn
          @click="this.$router.push('/community/myAccount')"
          flat
          dense
          class="withdraw q-mr-md"
          no-caps
        >
          {{ $t("community.mywallet.withdraw_account") }}
        </q-btn>
      </q-tabs>

      <q-separator/>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel class="no-padding" name="one">
          <!--            表头-->
          <div class="row table_height flex-center">
            <span class="text-center col-3">
              {{ $t("community.mywallet.date") }}
            </span>
            <span class="text-center col-3 void">
              {{
                $t("community.mywallet.withdrawal_Amount")
              }}<span>{{ currency === "rmb" ? "(￥)" : "($)" }}</span>
            </span>
            <span class="text-center col-3 void">
              {{ $t("community.mywallet.Withdrawal_type") }}
            </span>
            <span class="text-center col-2 void">
              {{ $t("community.mywallet.state") }}
            </span>
          </div>
          <!--            数据-->
          <div
            class="row table_height flex-center"
            v-for="item in detailsList2"
            :key="item"
          >
            <span class="text-center col-3"> {{ item.create_time }} </span>
            <span class="text-center col-3 void">
              {{ item.balance }}
            </span>
            <span class="text-center col-3 void">
              {{ item.withdrawal_type }}
            </span>
            <span class="text-center col-2 void">
              {{ getWithdrawStatus(item.verify_status) }}
            </span>
          </div>
        </q-tab-panel>

        <q-tab-panel class="no-padding" name="two">
          <div class="row table_height flex-center">
            <span class="text-center col-2">
              {{ $t("community.mywallet.date") }}
            </span>
            <span class="text-center col-2 void">
              {{ $t("community.mywallet.user") }}
            </span>
            <span class="text-center col-2 void">
              {{
                $t("community.mywallet.earnings_amount")
              }}<span>{{ currency === "rmb" ? "(￥)" : "($)" }}</span>
            </span>
            <span class="text-center col-4 void">
              {{ $t("community.mywallet.detail") }}
            </span>
          </div>
          <!--            数据-->
          <div
            class="row table_height flex-center"
            v-for="item in detailsList"
            :key="item"
          >
            <span class="text-center col-2"> {{ item.create_time }} </span>
            <span class="text-center col-2 void">
              {{ item.user }}
            </span>
            <span class="text-center col-2 void">
              {{ item.total }}
            </span>
            <span class="text-center col-4 void"> {{ item.title }} </span>
          </div>
        </q-tab-panel>
      </q-tab-panels>
      <div v-if="hasPagination" class="q-pa-md flex bg-white flex-center">
        <q-pagination
          class="q_pagination"
          direction-links
          v-model="currentPage"
          :max="maxPages"
          :max-pages="6"
        />
      </div>
      <div v-if="!hasPagination" class="flex flex-center q-mt-lg">
        <q-btn flat>{{ $t('notice.nomoredata') }}</q-btn>
      </div>
    </q-card>
  </div>
</template>

<script>
import {defineComponent} from "vue";
import {getauth} from "boot/axios";

export default defineComponent({
  name: "myWallet",
  data() {
    return {
      tab: "one",
      currency: "rmb",
      currentPage: 1,
      hasPagination: false,
      maxPages: 1,
      detailsList: [],
      detailsList2: [],
      walletDetails: {},
      withdraw_monthly: "0.00",
      wallet_type: "",
      withdraw_type: "",
      getwithdrawUrl: '',
      isverify: false
    };
  },
  watch: {
    currentPage(val) {
      this.redirectPage(val);
    },
    currency: {
      handler: function (val) {
        if (val === "rmb") {
          this.wallet_type = "r_wallet";
          this.detail_type = "rmb_salary";
          this.withdraw_type = "r_cash";
          this.getwithdrawUrl = 'pay/api/v1/rnbccount/'
        } else {
          this.wallet_type = "d_wallet";
          this.detail_type = "dollar_salary";
          this.withdraw_type = "d_cash";
          this.getwithdrawUrl = 'pay/api/v1/usd_account/'
        }
        this.getWalletDetail();
        if (this.tab === "one") {
          this.getWithdrawDetail();
        } else {
          this.getDetailsList();
        }
      },
      immediate: true,
    },
    tab: {
      handler(val) {
        if (val === "one") {
          this.getWithdrawDetail();
        } else {
          this.getDetailsList();
        }
      },
      immediate: true,
    },
  },
  methods: {
    getWithdrawStatus(val) {
      switch (val) {
        case 0:
          return this.$t("community.authentication_view.audit_failed");
          break;
        case 1:
          return this.$t("community.authentication_view.auditing");
          break;
        case 2:
          return this.$t("community.mywallet.paid");
          break;
      }
    },
    //获取钱包详情
    getWalletDetail() {
      var _this = this;
      getauth(`pay/api/v1/${_this.wallet_type}/`).then((res) => {
        _this.walletDetails = {
          balance: res.result.data[0].balance,
          withdrawal_amount: res.result.data[0].withdrawal_amount,
        };
        _this.withdraw_monthly = res.result.Cumulative;
      });
    },
    //获取累计提现
    getcumulative() {
      var _this = this;
      getauth("")
        .then((res) => {
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    getWithdrawDetail() {
      getauth(`pay/api/v1/${this.withdraw_type}/`).then((res) => {
        this.detailsList2 = res;
      });
    },
    //设置详情列表和分页
    setDetailsList(res) {
      this.detailsList = res.results;
      if (res.next || res.previous) {
        this.hasPagination = true;
      } else {
        this.hasPagination = false;
      }
    },
    //获取详情列表
    getDetailsList() {
      getauth(`pay/api/v1/${this.detail_type}/`).then((res) => {
        if (res.count) {
          this.setDetailsList(res);
          this.maxPages = Math.ceil(res.count / 20);
        }
      });
    },
    //换页
    redirectPage(page) {
      getauth("?page=" + page).then((res) => {
        this.setDetailsList(res);
        //回到顶部
        document.getElementsByClassName(
          "q-scrollarea__container"
        )[0].scrollTop = 0;
      });
    },
    //提现
    withdraw() {
      var _this = this;
      //获取认证状态
      if (_this.$q.cookies.get('area') === 'China') {
        getauth('/user/api/v1/auth_status/').then(res2 => {
          _this.isverify = res2.result.status
          //当完成认证
          if (_this.isverify === true) {
            //判断有无绑定账号
            getauth(_this.getwithdrawUrl).then(res => {
              if (res.length === 0) {
                _this.$q.notify({
                  message: _this.$t('community.mywallet.not_account'),
                  icon: 'close',
                  color: 'negative'
                })
                _this.$router.push("/community/myAccount");
              } else {
                if (_this.walletDetails.withdrawal_amount < 800) {
                  this.$q.notify({
                    message: _this.$t('community.mywallet.insufficient800'),
                    icon: "close",
                    color: "negative",
                  });
                } else {
                  _this.$router.push("/community/withdraw");
                }
              }
            }).catch(err => {
              _this.$q.notify({
                message: err.detail,
                icon: 'close',
                color: 'negative'
              })
            })
          } else {
            _this.$q.notify({
              message: _this.$t('community.mywallet.not_certified'),
              icon: 'close',
              color: 'negative'
            })
          }
        }).catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
      } else {}
    },
    withdraw_foreign() {
      var _this = this;
      if (_this.$q.cookies.get('area') === 'China') {
        getauth('/user/api/v1/auth_status/').then(res2 => {
          _this.isverify = res2.result.status
          //当完成认证
          if (_this.isverify === true) {
            //判断有无绑定账号
            getauth(_this.getwithdrawUrl).then(res => {
              if (res.length === 0) {
                _this.$q.notify({
                  message: _this.$t('community.mywallet.not_account'),
                  icon: 'close',
                  color: 'negative'
                })
                _this.$router.push("/community/myAccount");
              } else {
                if (_this.walletDetails.withdrawal_amount < 100) {
                  this.$q.notify({
                    message: _this.$t('community.mywallet.insufficient100'),
                    icon: "close",
                    color: "negative",
                  });
                } else {
                  _this.$router.push("/community/withdraw_foreign");
                }
              }
            }).catch(err => {
              _this.$q.notify({
                message: err.detail,
                icon: 'close',
                color: 'negative'
              })
            })
          } else {
            _this.$q.notify({
              message: _this.$t('community.mywallet.not_certified'),
              icon: 'close',
              color: 'negative'
            })
          }
        }).catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
      } else {}
    },
  },
  mounted() {
    this.$store.dispatch("bbsChange/isIndexMenu", false);
    this.$store.dispatch("bbsChange/link", "wallet");
  },
});
</script>

<style lang="scss" scoped>
.details {
  font-size: 18px;
  font-weight: 500;
}

.void {
  margin-left: 10px;
}

.tixian {
  border-bottom: 3px #eca211 solid;
  padding-bottom: 10px;
  cursor: pointer;
}

.table_height {
  font-size: 16px;
  font-weight: 400;
  color: #333333;
  height: 56px;
  border-bottom: 1px #d8d8d8 solid;
}

.top_card {
  height: 260px;
}

.detail {
  font-size: 18px;
  font-weight: 500;
  color: #333333;
}

.withdraw {
  background-color: #116fec;
  color: white;
  min-width: 120px;
  font-size: 18px;
  font-weight: 500;
}

.icon_top {
  margin-bottom: -3px;
}

.tit_top {
  font-size: 18px;
  font-weight: 500;
  color: #333333;
  margin-left: 5px;
}

.number_amount {
  padding-top: 20px;
  height: 80px;
  font-size: 40px;
  font-weight: 600;
  color: #eca211;
}

.w_ins {
  float: right;
  font-size: 15px;
  color: #116fec;
  cursor: pointer;
  border-bottom: 1px #116fec solid;
}

// .sed_card {
//   margin-top: 30px;
// }
</style>
