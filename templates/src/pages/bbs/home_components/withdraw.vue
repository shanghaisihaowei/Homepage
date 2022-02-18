<template>
  <div class="row">
    <!--    上半部分-->
    <q-card class="col-12 shadow-0">
      <q-card-actions>
        <q-btn
          @click="this.$router.push( '/community/myWallet')"
          style="font-size: 14px;font-weight: 400;color: #999999"
          unelevated
          :label="goblack"/>
      </q-card-actions>

      <q-separator inset/>

      <q-card-section horizontal class="q-pa-md">
        <img src="statics/person_center/withdraw.svg">
        <span class="w_application">
        {{ $t('community.withdraw.withdrawal_application') }}
      </span>
      </q-card-section>

      <q-separator inset/>

      <q-card-section class="q-pa-md">
        <!--      提交金额-->
        <div class="row fir_amount">
          <div class="w_amount">
            {{ $t('community.withdraw.submit_amount') }}(￥):
          </div>
          <q-input
            input-style="font-size: 18px;font-weight: 500;color:#333333"
            type="number"
            dense
            autofocus
            v-model="amount_sub"
            onfocus="this.select()"
            :keyup="mykeyup(amount_sub)"
            :rules="[val => val && val >= 800 || this.amount_small + '800',val => val && this.withdrawal_amount * 1 >= val * 1 || this.beyond]"
            outlined
            style="width: 180px;margin-left: 20px;margin-top: 20px"/>
          <!--          <div v-if="amount_sub >= 800" class="flex flex-center tax" style="background: url('statics/community/tax.svg')">-->
          <!--            {{ $t('community.withdraw.tax') }} {{tax}}-->
          <!--          </div>-->
        </div>
        <!--      注意-->
        <div v-if="area === 'China'" class="w_notice">
          {{ $t('community.withdraw.notice1') }}
          <br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ $t('community.withdraw.notice2') }}
        </div>
        <div v-if="area !== 'China'" class="w_notice">
          {{ $t('community.withdraw.notice5') }}
        </div>
        <!--      结算金额-->
        <!--        <div style="margin-top: 33px">-->
        <!--          <span class="s_amount">-->
        <!--            {{ $t('community.withdraw.settlement_amount') }}-->
        <!--          </span>-->
        <!--          <span v-if="amount_sub >= 800" class="amount_value">-->
        <!--            {{ s_amount }}-->
        <!--          </span>-->
        <!--        </div>-->
      </q-card-section>
    </q-card>
    <!--    下半部分-->
    <q-card class="col-12 shadow-0" style="margin-top: 30px">
      <!--      提现账户信息-->
      <q-card-section horizontal class="q-pa-md row">
        <div class="col-10">
          <img src="statics/person_center/withdraw.svg">
          <span class="w_application">
        {{ $t('community.withdraw.wai') }}
      </span>
        </div>
        <!--        切换账户-->
        <q-btn-dropdown class="col-2 toggle_btn" unelevated :label=chose_amount>
          <q-list>
            <q-item v-for="item in amount" clickable v-close-popup @click="chose_accounts(item.alipay_account)">
              <q-item-section>
                <q-item-label>{{ item.alipay_account }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-card-section>

      <q-separator inset/>
      <!--      账户信息-->
      <q-card-section class="q-pa-md">
        <div class="acc_info">
          {{ $t('community.withdraw.account_type') }}
          &nbsp;&nbsp;&nbsp;
          {{ $t('community.withdraw.alipay') }}
        </div>
        <div class="acc_info">
          {{ $t('community.withdraw.account_number') }}
          &nbsp;&nbsp;&nbsp;
          <span class="amount_num">
            {{ amount_num }}
          </span>
        </div>
      </q-card-section>

      <q-card-actions class="q-pa-md flex-center pad_sub_btn">
        <q-btn
          class="sub_btn"
          flat
          @click="submit()"
        >
          {{ $t('index.submit') }}
        </q-btn>
      </q-card-actions>
    </q-card>
  </div>
  <q-dialog v-model="notice" full-width persistent>
    <q-card :class="{'dia_hans':this.$q.cookies.get('lang') === 'zh-hans','dia_en':this.$q.cookies.get('lang') !== 'zh-hans'}">
      <q-card-section class="text-center">
         <span class="w_intop">
        {{ $t('community.withdraw.w_ins') }}
      </span>
      </q-card-section>
      <q-separator inset/>
      <q-card-section class="flex flex-center">
        <img v-if="this.$q.cookies.get('lang') === 'zh-hans'" src="statics/community/w_in.svg">
        <img v-if="this.$q.cookies.get('lang') !== 'zh-hans'" src="statics/community/w_in_e.svg">
      </q-card-section>
      <q-separator inset/>
      <q-card-actions class="flex-center" style="padding-top: 20px">
        <q-btn
          class="w_intop_btn"
          flat
          @click="notice = false"
        >
          {{ $t('index.confirm') }}
        </q-btn>
      </q-card-actions>
      <q-card-section class="text-center" style="padding-top: 0">
        <span class="amount_num">
        {{ $t('community.withdraw.agree') }}
      </span>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<style lang="scss" scoped>
.dia_hans {
  width:610px!important;
}
.dia_en {
  width:720px!important;
}
.tax {
  width: 130px;
  height: 40px;
  font-size: 14px;
  font-weight: 400;
  color: #333333;
  margin-left: 20px;
}

.w_intop_btn {
  width: 300px;
  height: 50px;
  color: white;
  background-color: #116fec;
  font-size: 18px;
  font-weight: 400;
}

.w_intop {
  font-size: 20px;
  font-weight: 500;
  color: #333333;
}

.amount_num {
  font-size: 14px;
  font-weight: 400;
  color: #333333;
}

.pad_sub_btn {
  padding-top: 40px;
  padding-bottom: 100px;
}

.sub_btn {
  width: 220px;
  height: 50px;
  background: #116fec;
  border-radius: 4px;
  color: white;
  font-size: 18px;
  font-weight: 400;
}

.acc_info {
  font-size: 18px;
  font-weight: 400;
  color: #333333;
  margin: 30px 30px;
}

.toggle_btn {
  font-size: 18px;
  font-weight: 400;
  color: #116FEC;
}

.fir_amount {
}

.w_application {
  font-size: 18px;
  font-weight: 500;
  color: #333333;
  margin: 10px 10px;
}

.w_amount {
  font-size: 18px;
  font-weight: 400;
  color: #333333;
  margin-left: 30px;
  display: flex;
  align-items: center;
}

.w_notice {
  font-size: 14px;
  font-weight: 400;
  color: #D00D00;
  margin-top: 20px;
  margin-left: 30px;
  padding-bottom: 20px;
}

.s_amount {
  font-size: 18px;
  font-weight: 400;
  color: #333333;
  margin-left: 30px;
}

.amount_value {
  margin-left: 18px;
  font-size: 32px;
  font-weight: 400;
  color: #D00D00;
}
</style>

<script>
import {defineComponent} from "vue";
import {get, getauth, post, postauth} from "boot/axios";

export default defineComponent({
  name: "withdraw",
  data() {
    return {
      notice: false,
      area: '',
      amount: '',
      amount_num: '',
      s_amount: '',
      chose_amount: this.$t('community.withdraw.switch_accounts'),
      goblack: this.$t('community.black'),
      amount_sub: '',
      amount_small: this.$t('community.withdraw.amount_small'),
      tax: '0',
      withdrawal_amount: '',
      wallet_type: '',
      beyond: this.$t('community.withdraw.beyond'),
    }
  },
  methods: {
    //获取钱包详情
    getWalletDetail() {
      var _this = this
      getauth('pay/api/v1/r_wallet/').then((res) => {
        _this.withdrawal_amount = res.result.data[0].withdrawal_amount
        _this.amount_sub = res.result.data[0].withdrawal_amount
      });
    },
    // 查询账户列表
    account_list() {
      var _this = this
      if (_this.$q.cookies.get('token')) {
        getauth('/pay/api/v1/rnbccount/?').then(res => {
          _this.amount = res
          if (res.length > 0) {
            res.forEach((item, index) => {
              if (item.is_default) {
                _this.amount_num = item.alipay_account
              }
            })
          } else {
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
          message: 'err.detail',
          icon: 'close',
          color: 'negative'
        })
      }
    },
    //选择账户
    chose_accounts(e) {
      var _this = this
      _this.amount_num = e
    },
    // 计算结算金额
    // calculate_s_amount (amount) {
    //   // amount  提现金额
    //   // _this.s_amount 结算金额
    //   var _this = this
    //   // tax 税额
    //   var taxable  //应税所得额
    //   if (amount <= 4000) {
    //     taxable = amount - 800
    //     if (taxable <= 20000) {
    //       _this.tax = taxable * 0.2
    //       _this.s_amount = amount - _this.tax
    //     } else if (20000< taxable <= 50000) {
    //       _this.tax = taxable * 0.3 - 2000
    //       _this.s_amount = amount - _this.tax
    //     } else if (taxable > 50000) {
    //       _this.tax = taxable * 0.4 - 7000
    //       _this.s_amount = amount - _this.tax
    //     }
    //   } else if (amount > 4000) {
    //     taxable = amount * 0.8
    //     if (taxable <= 20000) {
    //       _this.tax = taxable * 0.2
    //       _this.s_amount = amount - _this.tax
    //     } else if (20000< taxable <= 50000) {
    //       _this.tax = taxable * 0.3 - 2000
    //       _this.s_amount = amount - _this.tax
    //     } else if (taxable > 50000) {
    //       _this.tax = taxable * 0.4 - 7000
    //       _this.s_amount = amount - _this.tax
    //     }
    //   }
    // },
    //提交
    submit() {
      var _this = this
      if (_this.withdrawal_amount * 1 >= _this.amount_sub * 1
        && _this.amount_sub * 1 >= 800
        && _this.amount_num !== ''
      ) {
        var msg = {}
        msg.balance = _this.amount_sub
        msg.alipay_account = _this.amount_num
        msg.withdrawal_type = '支付宝'
        postauth('pay/api/v1/r_cash/',msg).then(res => {
          //可以提交
          _this.$q.notify({
            message: _this.$t('community.withdraw.withdraw_suc'),
            icon: 'check',
            color: 'green'
          })
          _this.$router.push('/community/myWallet')
        }).catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
      } else {
        // 不可提交
        _this.$q.notify({
          message: _this.$t('community.withdraw.withdraw_err'),
          icon: 'close',
          color: 'negative'
        })
      }
    },
    mykeyup (e) {
      this.amount_sub = e.match(/\d+(\.\d{0,2})?/) ? e.match(/\d+(\.\d{0,2})?/)[0] : ''
      e.replace('-', '')
    }
  },
  mounted() {
    if (this.$q.cookies.has('area')) {
      this.area = this.$q.cookies.get('area')
      if (this.$q.cookies.get('area') === 'China') {
        this.notice  = true
      } else {
        this.notice  = false
      }
    }
    this.account_list()
    this.getWalletDetail()
    this.$store.dispatch("bbsChange/isIndexMenu", false);
    this.$store.dispatch("bbsChange/link", "wallet");
  }
})
</script>
