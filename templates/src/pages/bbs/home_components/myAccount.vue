<template>
  <div
    style="
      color: #333333;
      font-size: 16px;
      height: calc(90vh);
      background-color: white;
    "
  >
    <q-card flat class="flex" style="align-items: center">
      <q-tabs
        v-model="account_type"
        align="left"
        narrow-indicator
        indicator-color="blue"
        inline-label
        style="font-size: 20px; font-weight: 500"
        class="q-py-md"
      >
        <q-tab name="rmb" no-caps
          ><span>{{ $t("community.myAccount_view.rmb_account") }}</span></q-tab
        >
        <q-tab name="dollar" no-caps
          ><span>{{
            $t("community.myAccount_view.dollar_account")
          }}</span></q-tab
        >
      </q-tabs>
      <q-space />
      <q-btn
        @click="addAccount"
        class="q-mr-md"
        flat
        style="background-color: #116fec; min-width: 120px; height: 38px"
        ><span style="font-size: 16px; color: white">{{
          $t("community.myAccount_view.add_account")
        }}</span></q-btn
      >
    </q-card>
    <q-card flat>
      <q-card-section
        class="flex row q-py-none"
        style="
          background-color: #f4f4f4;
          font-size: 18px;
          height: 60px;
          line-height: 60px;
          text-align: center;
        "
      >
        <div class="col-3 text-left">
          {{ $t("community.myAccount_view.account_number") }}
        </div>
        <div v-show="account_type == 'rmb'" class="col-2">
          {{ $t("community.myAccount_view.account_holder") }}
        </div>
        <div class="col-3">
          {{ $t("community.myAccount_view.account_type") }}
        </div>
      </q-card-section>
      <q-card-section
        class="flex row text-center"
        style="align-items: center"
        v-for="item in accountList"
        :key="item"
      >
        <div class="col-3 text-left">
          {{
            account_type == "rmb" ? item.alipay_account : item.account_number
          }}
        </div>
        <div v-show="account_type == 'rmb'" class="col-2">
          {{ item.account_holder }}
        </div>
        <div class="col-3 flex flex-center">
          <img
            class="q-mr-sm"
            :src="
              account_type == 'rmb' ? 'statics/zfb.svg' : 'statics/paypal.svg'
            "
          />
          {{ item.account_type }}
        </div>
        <div class="col-2">
          <q-btn
            @click="setDefaultAccount(item.id)"
            outline
            rounded
            v-show="!item.is_default"
            >{{ $t("community.myAccount_view.set_default") }}</q-btn
          >
          <span v-show="item.is_default" style="color: #c80808">{{
            $t("community.myAccount_view.default_account")
          }}</span>
        </div>
        <div class="col-2">
          <q-btn
            @click="
              this.confirmDelete = true;
              this.deleteId = item.id;
            "
            flat
            style="text-decoration: underline; width: 60px"
            >{{ $t("community.myAccount_view.delete") }}</q-btn
          >
        </div>
      </q-card-section>
    </q-card>
    <q-card flat class="q-mt-xl" v-show="showAddForm">
      <q-card-section
        style="
          font-size: 18px;
          font-weight: 500;
          border-top: 1px solid #e6e6e6;
          border-bottom: 1px solid #e6e6e6;
        "
      >
        {{ $t("community.myAccount_view.add_info") }}
      </q-card-section>
      <q-card-section class="flex q-mt-lg">
        <div style="min-width: 120px">
          <div style="height: 40px; line-height: 40px">
            {{ $t("community.myAccount_view.email") }}：
          </div>
          <div style="height: 40px; line-height: 40px" class="q-my-lg">
            {{ $t("community.myAccount_view.code") }}：
          </div>
          <div style="height: 40px; line-height: 40px">
            <span
              >{{
                account_type == "rmb"
                  ? $t("community.myAccount_view.alipay_account")
                  : $t("community.myAccount_view.paypal_account")
              }}：</span
            >
          </div>
        </div>
        <div style="flex: 1">
          <div
            class="q-px-md"
            style="
              background-color: #ececec;
              height: 40px;
              line-height: 40px;
              border-radius: 4px;
            "
          >
            {{ email }}
          </div>
          <div class="flex">
            <q-input
              dense
              outlined
              v-model="code"
              style="flex: 1"
              class="q-my-lg myAccount"
              :placeholder="
                this.$t('community.myAccount_view.code_placeholder')
              "
            >
            </q-input>
            <q-btn
              @click="getCode"
              :disable="getCodeDis"
              style="
                min-width: 190px;
                background-color: #116fec;
                color: white;
                height: 40px;
                border-top-left-radius: 0;
                border-bottom-left-radius: 0;
              "
              class="q-mt-lg"
              flat
              dense
              >{{ btnText }}</q-btn
            >
          </div>
          <q-input
            v-model="account"
            dense
            outlined
            :placeholder="
              account_type == 'rmb'
                ? this.$t('community.myAccount_view.alipay_placeholder')
                : this.$t('community.myAccount_view.paypal_placeholder')
            "
          >
          </q-input>
        </div>
      </q-card-section>
      <q-card-section class="text-center q-mt-xl">
        <q-btn
          :disable="disabled"
          @click="submit"
          style="color: white; background-color: #116fec; width: 220px"
          >{{ $t("community.authentication_view.submit") }}</q-btn
        >
      </q-card-section>
    </q-card>
    <q-dialog v-model="confirmDelete" persistent>
      <q-card
        style="width: 470px; height: 180px; font-size: 18px; position: relative"
      >
        <q-card-section class="q-ma-md">
          <span>{{ $t("community.myAccount_view.delete_tip") }}？</span>
        </q-card-section>

        <q-card-actions style="position: absolute; bottom: 0; right: 0">
          <q-btn
            flat
            style="font-size: 18px; font-weight: 500"
            :label="this.$t('index.confirm')"
            color="primary"
            v-close-popup
            @click="deleteAccount"
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
import { postauth, getauth, putauth, deleteauth } from "boot/axios";
import jwtDecode from "jwt-decode";

export default {
  data() {
    return {
      account_type: "rmb",
      accountList: [],
      showAddForm: false,
      code: "",
      account: "",
      email: "",
      btnText: "",
      getAccountUrl: "",
      confirmDelete: false,
      deleteId: "",
      getCodeDis: false,
    };
  },
  computed: {
    disabled() {
      if (this.code && this.account) {
        return false;
      } else {
        return true;
      }
    },
  },
  watch: {
    account_type: {
      handler(val) {
        if (val == "rmb") {
          this.getAccountUrl = "pay/api/v1/rnbccount/";
        } else {
          this.getAccountUrl = "pay/api/v1/usd_account/";
        }
        this.getAccounts();
        this.resetAddForm();
      },
      immediate: true,
    },
    getCodeDis: {
      handler(val) {
        if (val) {
          this.btnText = this.$t("community.myAccount_view.email_time");
        } else {
          this.btnText = this.$t("community.myAccount_view.get_code");
        }
      },
      immediate: true,
    },
  },
  methods: {
    addAccount() {
      this.showAddForm = true;
    },
    resetAddForm() {
      this.showAddForm = false;
      this.code = "";
      this.account = "";
      this.getCodeDis = false;
    },
    getAccounts() {
      getauth(this.getAccountUrl).then((res) => {
        this.accountList = res;
      });
    },
    getCode() {
      getauth("user/api/v1/account_codes/?email=" + this.email).then((res) => {
        this.$q.notify({
          message: this.$t("community.sended_email"),
          icon: "check",
          color: "green",
        });
        this.getCodeDis = true;
      });
    },
    setDefaultAccount(id) {
      putauth(`${this.getAccountUrl}${id}/`).then((res) => {
        this.accountList = res.result.data;
        this.$q.notify({
          message: res.result.msg,
          icon: "check",
          color: "green",
        });
      });
    },
    deleteAccount() {
      deleteauth(`${this.getAccountUrl}${this.deleteId}/`).then((res) => {
        this.accountList = res.result.data;
        this.$q.notify({
          message: res.result.msg,
          icon: "check",
          color: "green",
        });
      });
    },
    submit() {
      let data =
        this.account_type == "rmb"
          ? { alipay_account: this.account, code: this.code }
          : { account_number: this.account, code: this.code };
      postauth(this.getAccountUrl, data).then((res) => {
        if (res.code != 998) {
          if (res.result.msg) {
            this.$q.notify({
              message: res.result.msg,
              icon: "close",
              color: "negative",
            });
          } else {
            this.accountList = res.result.data;
            this.resetAddForm();
          }
        }
      });
    },
  },
  created() {
    this.email = jwtDecode(this.$q.cookies.get("token")).email;
    this.$store.dispatch("bbsChange/isIndexMenu", false);
    this.$store.dispatch("bbsChange/link", "my_account");
  },
};
</script>
<style scoped lang="sass">
.active
    background-color: #116FEC
    color: white
</style>
    