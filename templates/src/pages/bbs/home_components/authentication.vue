<template>
  <div style="color: #333333; font-size: 16px">
    <q-card flat class="bottom_border">
      <q-card-section
        class="q-py-none bottom_border"
        style="
          font-size: 18px;
          height: 60px;
          line-height: 60px;
          font-weight: 500;
        "
      >
        {{ $t("community.authentication_view.authentication") }}
      </q-card-section>
      <q-card-section
        class="progress flex q-my-md"
        style="justify-content: center"
      >
        <div>
          <div class="progress_number_active progress_number">
            <div class="number">1</div>
          </div>
          <div>{{ $t("community.authentication_view.fill_info") }}</div>
        </div>
        <img style="margin-top: -22px" :src="lingSrc[0]" />
        <div>
          <div
            :class="
              status == 1 || status == 2
                ? 'progress_number_active progress_number'
                : 'progress_number'
            "
            :style="status == 3 ? { backgroundColor: '#C80808' } : {}"
          >
            <div class="number">2</div>
          </div>
          <div v-if="status != 3">
            {{ $t("community.authentication_view.auditing") }}
          </div>
          <div v-if="status == 3">
            {{ $t("community.authentication_view.audit_failed") }}
          </div>
        </div>
        <img style="margin-top: -22px" :src="lingSrc[1]" />
        <div>
          <div
            :class="
              status == 2
                ? 'progress_number_active progress_number'
                : 'progress_number'
            "
          >
            <div class="number">3</div>
          </div>
          <div>{{ $t("community.authentication_view.audit_success") }}</div>
        </div>
      </q-card-section>
      <q-card-section
        class="q-pb-none"
        style="font-size: 18px; font-weight: 500"
        >{{ $t("community.authentication_view.equity") }}：</q-card-section
      >
      <q-card-section>{{
        $t("community.authentication_view.equity_msg")
      }}</q-card-section>
      <q-card-section class="flex" style="align-items: center">
        <div class="form_info">
          {{ $t("community.authentication_view.real_name") }}：
        </div>
        <q-input
          :error="name_error"
          :error-message="name_error_tip"
          @blur="ruleHandler('name')"
          v-if="!submit_auth"
          v-model="formData.name"
          :placeholder="
            this.$t('community.authentication_view.name_placeholder')
          "
          outlined
          dense
          class="form_input"
          style="padding-bottom: 0 !important"
        ></q-input>
        <div v-if="submit_auth">{{ formData.name }}</div>
      </q-card-section>
      <q-card-section class="flex" style="align-items: center">
        <div class="form_info">
          {{ $t("community.authentication_view.id_number") }}：
        </div>
        <q-input
          :error="number_error"
          :error-message="number_error_tip"
          @blur="ruleHandler('number')"
          v-if="!submit_auth"
          v-model="formData.number"
          :placeholder="
            this.$t('community.authentication_view.number_placeholder')
          "
          outlined
          dense
          class="form_input"
          style="padding-bottom: 0 !important"
        ></q-input>
        <div v-if="submit_auth">{{ formData.number }}</div>
      </q-card-section>
      <q-card-section>
        <div class="flex" style="align-items: center">
          <div class="form_info">
            {{ $t("community.authentication_view.id_photo") }}：
          </div>
          <div>
            <div class="flex">
              <upload-img
                @getUploadImg="getUploadImg"
                class="q-mr-lg"
                :text="this.$t('community.authentication_view.front_photo')"
                :imgSrc="imgSrcFront"
                side="front"
                :isSubmit="submit_auth"
              ></upload-img>
              <upload-img
                @getUploadImg="getUploadImg"
                :text="this.$t('community.authentication_view.back_photo')"
                side="back"
                :imgSrc="imgSrcBack"
                :isSubmit="submit_auth"
              ></upload-img>
            </div>
          </div>
        </div>
        <div
          class="q-mt-md"
          style="font-size: 14px; color: #999999; margin-left: 120px"
        >
          {{ $t("community.authentication_view.photo_tip") }}：
        </div>
      </q-card-section>
      <q-card-section class="q-mt-xl text-center" style="padding-bottom: 150px">
        <q-btn
          style="
            font-size: 18px;
            background-color: #116fec;
            min-width: 220px;
            color: white;
          "
          dense
          @click="submit"
          :disable="disabled"
          v-show="!submit_auth"
        >
          {{ $t("community.authentication_view.submit") }}
        </q-btn>
        <q-btn
          style="
            font-size: 18px;
            background-color: #116fec;
            width: 220px;
            color: white;
          "
          dense
          @click="reset"
          v-show="status == 3"
        >
          {{ $t("community.authentication_view.resubmit") }}
        </q-btn>
      </q-card-section>
    </q-card>
  </div>
</template>
<script>
import { getauth, postauth } from "boot/axios";
import UploadImg from "./components/UploadImg.vue";
import jwtDecode from "jwt-decode";
export default {
  components: {
    UploadImg,
  },
  data() {
    return {
      formData: {
        name: "",
        number: "",
        file_front: "",
        file_back: "",
      },
      status: "",
      disabled: true,
      imgSrcFront: "",
      imgSrcBack: "",
      submit_auth: false,
      name_error: false,
      name_error_tip: this.$t("community.authentication_view.name_error"),
      number_error: false,
      number_error_tip: this.$t("community.authentication_view.number_error"),
    };
  },
  computed: {
    isFull() {
      return (
        this.formData.name &&
        this.formData.number &&
        this.formData.file_front &&
        this.formData.file_back &&
        !this.name_error &&
        !this.number_error
      );
    },
    lingSrc() {
      if (this.status == 0) {
        return ["statics/line.svg", "statics/greyLine.svg"];
      } else if (this.status == 1) {
        return ["statics/blueLine.svg", "statics/line.svg"];
      } else if (this.status == 2) {
        return ["statics/blueLine.svg", "statics/blueLine.svg"];
      } else {
        return ["statics/blueLine.svg", "statics/greyLine.svg"];
      }
    },
  },
  watch: {
    isFull(val) {
      if (val) {
        this.disabled = false;
      } else {
        this.disabled = true;
      }
    },
    formData: {
      handler(val) {
        this.formData.name = val.name.replace(/\s/g, "");
        this.formData.number = val.number.replace(/\s/g, "");
      },
      deep: true,
    },
  },
  methods: {
    ruleHandler(val) {
      if (val == "number") {
        if (
          /(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(this.formData.number) == false
        ) {
          this.number_error = true;
        } else {
          this.number_error = false;
        }
      } else {
        if (this.formData.name.search(/[0-9]/g) != -1 || !this.formData.name) {
          this.name_error = true;
        } else {
          this.name_error = false;
        }
      }
    },
    getUploadImg(side, file) {
      if (side == "front") {
        this.formData.file_front = file;
      } else {
        this.formData.file_back = file;
      }
    },
    submit() {
      let data = new FormData();
      data.append("email", jwtDecode(this.$q.cookies.get("token")).email);
      data.append("name", this.formData.name);
      data.append("id_number", this.formData.number);
      data.append("the_front_of_id_card", this.formData.file_front);
      data.append("reverse_side_of_id_card", this.formData.file_back);
      postauth("user/api/v1/auth/", data).then((res) => {
        window.location.reload();
      });
    },
    getAuthStatus() {
      getauth("user/api/v1/auth/").then((res) => {
        let data = res[res.length - 1];
        if (data) {
          this.formData.name = data.name;
          this.formData.number = data.id_number;
          this.imgSrcFront = data.the_front_of_id_card;
          this.imgSrcBack = data.reverse_side_of_id_card;
          this.status = data.verify_status;
          this.submit_auth = true;
        } else {
          this.submit_auth = false;
        }
      });
    },
    reset() {
      this.imgSrcFront = " ";
      this.imgSrcBack = " ";
      this.status = 0;
      this.submit_auth = false;
      this.formData = {
        name: "",
        number: "",
        file_front: "",
        file_back: "",
      };
    },
  },
  created() {
    this.getAuthStatus();
    this.$store.dispatch("bbsChange/isIndexMenu", false);
    this.$store.dispatch("bbsChange/link", "verified");
  },
};
</script>
<style scoped lang="sass">
.progress
    color: #999999
    .progress_number
        border-radius: 4px
        width: 25px
        height: 25px
        background-color: #D8D8D8
        transform: rotate(45deg)
        margin: 15px auto
        .number
            color: white
            height: 25px
            display: flex
            justify-content: center
            align-items: center
            transform: rotate(-45deg)
    .progress_number_active
        background-color: #116FEC
.form_info
    width: 120px
.form_input
    flex: 1
</style>
