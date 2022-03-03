<template>
  <div class="release_container">
    <q-card square flat style="color: #999999" class="bottom_border q-py-md"
      ><q-btn
        padding="5px 9px"
        class="text-body1 q-ml-sm"
        @click="this.$router.go(-1)"
        flat
      >
        &lt;{{ $t("community.e_shop_view.back") }}
      </q-btn></q-card
    >
    <q-card square flat>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.affiliation") }}：
        </div>
        <q-select
          style="width: 100%"
          dense
          :disable="this.pluginId != 'newPlugin'"
          outlined
          v-model="pluginBelonging"
          :options="belongingOptions"
        >
          <template v-if="!pluginBelonging" v-slot:prepend>
            <div class="text-body2" style="color: #999999">
              {{ $t("community.e_shop_view.select") }}：
            </div>
          </template>
        </q-select>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.plugin_name") }}：
        </div>
        <q-input
          style="padding-bottom: 0"
          maxlength="40"
          :error-message="errorMessage_name"
          :error="error_name"
          dense
          outlined
          v-model="pluginName"
          @focus="hidePlaceholder('showNamePholder')"
          @blur="showPlaceholder('pluginName', 'showNamePholder')"
        >
          <div v-show="showNamePholder" class="input_placeholder">
            {{ $t("community.e_shop_view.placeholder_name") }}
          </div>
        </q-input>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.plugin_tag") }}:
        </div>
        <q-input
          dense
          outlined
          v-model="pluginTag"
          @focus="hidePlaceholder('showTagPholder')"
          @blur="showPlaceholder('pluginTag', 'showTagPholder')"
        >
          <div v-show="showTagPholder" class="input_placeholder">
            {{ $t("community.e_shop_view.placeholder_tag") }}
          </div>
        </q-input>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.plugin_des") }}:
        </div>
        <q-input
          dense
          outlined
          maxlength="100"
          :error-message="errorMessage_des"
          :error="error_des"
          v-model="pluginDes"
          @focus="hidePlaceholder('showDesPholder')"
          @blur="showPlaceholder('pluginDes', 'showDesPholder')"
        >
          <div v-show="showDesPholder" class="input_placeholder">
            {{ $t("community.e_shop_view.placeholder_des") }}
          </div>
        </q-input>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.plugin_versions") }}：<span
            style="color: #999999"
            >{{ $t("community.e_shop_view.example") }}</span
          >
        </div>
        <div class="flex">
          <q-input
            style="flex: 1"
            v-model="pluginVersions"
            outlined
            dense
            @focus="this.showVersionsPholder = false"
            @blur="if (!this.pluginVersions) this.showVersionsPholder = true;"
          >
            <template v-slot:prepend>
              <div
                class="bg-grey-3 text-body1"
                style="
                  width: 70px;
                  height: 40px;
                  line-height: 40px;
                  text-align: center;
                  color: #999999;
                  margin-left: -12px;
                "
              >
                V:
              </div>
            </template>
            <div
              v-show="showVersionsPholder"
              style="
                line-height: 40px;
                height: 40px;
                position: absolute;
                left: 0px;
                cursor: text;
                color: #999999;
              "
            >
              {{ $t("community.e_shop_view.placeholder_versions") }}
            </div>
          </q-input>
          <q-select
            style="width: 200px"
            class="q-ml-md"
            dense
            outlined
            v-model="versionsType"
            :options="versionsOptions"
          >
            <template v-slot:prepend>
              <div class="text-body2" style="color: #999999">
                {{ $t("community.e_shop_view.versions_type") }}：
              </div>
            </template>
          </q-select>
        </div>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.update_explain") }} ：
        </div>
        <markdown-aditor
          :placeholder="placeholder_update"
          @getMarkdownHtml="getMarkdownHtml('updateNotes', $event)"
          @getMarkdownText="getMarkdownText('updateMarkdown', $event)"
          :needUploadImg="false"
          :markdownText="updateMarkdown"
          :idIndex="0"
        ></markdown-aditor>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.plugin_introduce") }}：
        </div>
        <markdown-aditor
          :placeholder="placeholder_use"
          @getMarkdownHtml="getMarkdownHtml('useNotes', $event)"
          @getMarkdownText="getMarkdownText('useMarkdown', $event)"
          :markdownText="useMarkdown"
          :needUploadImg="true"
          :idIndex="1"
        ></markdown-aditor>
      </q-card-section>
      <q-card-section>
        <upload-file
          @getUploadFile="getUploadFile"
          :fileName="this.pluginId === 'newPlugin' ? '' : this.fileName"
        ></upload-file>
      </q-card-section>
      <q-card-section>
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.release_method") }}：
        </div>
        <div style="margin-left: -8.5px" class="q-mt-sm">
          <q-radio
            size="sm"
            v-model="radio_button"
            val="free"
            :label="this.$t('community.e_shop_view.sort_free')"
          ></q-radio>
          <q-radio
            class="q-mx-lg"
            size="sm"
            v-model="radio_button"
            val="pay"
            :label="this.$t('community.e_shop_view.sort_pay')"
          ></q-radio>
        </div>
      </q-card-section>
      <q-card-section v-show="radio_button == 'pay'">
        <div class="text-h6 q-mb-sm">
          {{ $t("community.e_shop_view.software_cost") }}：
        </div>
        <div class="q-mt-md flex">
          <q-select
            outlined
            dense
            v-model="paymentMethod"
            :options="paymentOptions"
            class="payment_method"
          >
            <template v-slot:prepend>
              <div class="text-body2 text-black q-mr-sm">
                {{ $t("community.e_shop_view.money_type") }} ：
              </div>
            </template>
          </q-select>
          <q-input
            v-model="money"
            type="number"
            outlined
            dense
            :error="error_amount"
            :error-message="amountError"
            @blur="moneyBlur"
            style="margin-left: 15px; flex: 1"
          >
            <template v-slot:prepend>
              <div class="text-body2 text-black">
                {{ $t("community.e_shop_view.label_fill_amount") }} ：
              </div>
            </template>
          </q-input>
        </div>
        <div style="color: #d95555" class="q-my-md">
          {{ $t("community.e_shop_view.deduction_prompt") }}
        </div>
      </q-card-section>
      <q-card-section class="text-center" style="padding-bottom: 50px">
        <q-btn
          :class="
            disable_release ? 'release_btn_disabled' : 'release_btn_undisabled'
          "
          unelevated
          :disable="disable_release"
          @click="release"
          >{{ $t("community.e_shop_view.release") }}</q-btn
        >
      </q-card-section>
    </q-card>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import { getauth, uploadpost, uploadput } from "boot/axios.js";
import UploadFile from "./components/UploadFile.vue";
import MarkdownAditor from "./components/MarkdownAditor.vue";

export default defineComponent({
  components: {
    UploadFile,
    MarkdownAditor,
  },
  data() {
    return {
      pluginName: "",
      pluginTag: "",
      pluginDes: "",
      pluginVersions: "",
      updateNotes: "",
      useNotes: "",
      radio_button: "free",
      paymentMethod: "",
      money: 0,
      isFilled: false,
      paymentOptions: ["￥", "$"],
      showUpdatePholder: true,
      showUsePholder: true,
      showNamePholder: true,
      showTagPholder: true,
      showVersionsPholder: true,
      showDesPholder: true,
      versionsType: "",
      versionsOptions: [
        this.$t("community.e_shop_view.official_version"),
        this.$t("community.e_shop_view.beta_version"),
      ],
      pluginBelonging: "",
      belongingOptions: [
        this.$t("community.greaterwms"),
        this.$t("community.dvadmin"),
      ],
      placeholder_update: `<div style='color:#999999'>${this.$t(
        "community.e_shop_view.placeholder_update"
      )}</div>`,
      placeholder_use: `<div style='color:#999999'>${this.$t(
        "community.e_shop_view.placeholder_use"
      )}</div>`,
      error_name: false,
      errorMessage_name: this.$t("community.e_shop_view.maxlength_40_name"),
      error_des: false,
      errorMessage_des: this.$t("community.e_shop_view.maxlength_100_des"),
      file: "",
      fileName: "",
      pluginId: "",
      error_amount: false,
      amountError: this.$t("community.myAccount_view.money_tip"),
      updateMarkdown: "",
      useMarkdown: "",
      submit: "",
      submitUrl: "",
    };
  },
  computed: {
    pluginMsg() {
      return {
        affiliation: this.pluginBelonging,
        tab_name: this.pluginTag,
        name: this.pluginName,
        brief: this.pluginDes,
        version: this.pluginVersions,
        versionsType: this.versionsType,
        plugin_instructions: this.updateNotes,
        direction_for_use: this.useNotes,
        source_code_file: this.file,
        release_form: this.radio_button == "free" ? "0" : "1",
        total_amount: this.money,
        currency: this.paymentMethod,
      };
    },
    disable_release() {
      for (let item in this.pluginMsg) {
        if (!this.pluginMsg[item]) {
          if (item == "total_amount" || item == "currency") {
            if (this.radio_button === "free") {
              this.isFilled = true;
            } else {
              this.isFilled = false;
              break;
            }
          } else if (
            item == "source_code_file" &&
            this.pluginId !== "newPlugin"
          ) {
            this.isFilled = true;
          } else {
            this.isFilled = false;
            break;
          }
        } else {
          this.isFilled = true;
        }
      }
      if (this.isFilled && !this.error_name && !this.error_des) {
        return false;
      } else {
        return true;
      }
    },
  },
  watch: {
    pluginName(val) {
      if (val.length == 40) {
        this.error_name = true;
      } else {
        this.error_name = false;
      }
      if (val) {
        this.hidePlaceholder("showNamePholder");
      }
    },
    pluginDes(val) {
      if (val.length == 100) {
        this.error_des = true;
      } else {
        this.error_des = false;
      }
      if (val) {
        this.hidePlaceholder("showDesPholder");
      }
    },
    pluginVersions(val) {
      if (val) {
        this.hidePlaceholder("showVersionsPholder");
      }
      this.pluginVersions = val.replace(/[^\d^\.]+/g, "");
    },
    pluginTag(val) {
      if (val) {
        this.hidePlaceholder("showTagPholder");
      }
    },
  },
  methods: {
    moneyBlur() {
      if (this.money < 0.01) {
        this.error_amount = true;
        this.money = 0;
      } else {
        this.error_amount = false;
      }
    },
    hidePlaceholder(placeholder) {
      this[placeholder] = false;
    },
    showPlaceholder(val, placeholder) {
      if (!this[val]) {
        this[placeholder] = true;
      } else {
        this.pluginTag = this.pluginTag.replace(/，/g, ",");
      }
    },
    //发布插件
    release() {
      if (this.radio_button == "pay" && this.money < 0.01) {
        this.error_amount = true;
        this.money = 0;
      } else {
        this.error_amount = false;
        let formData = this.setUploadFormData();
        let tip = this.$t("community.myAccount_view.release_success");
        this.$router.push("/community/myReleasedPlugins");
        this.submit(this.submitUrl, formData)
          .then((res) => {
            if (res.data.code !== 998) {
              this.$nextTick(() => {
                this.$q.notify({
                  message: tip,
                  icon: "check",
                  color: "green",
                });
              });
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    //获取上传的文件
    getUploadFile(file) {
      this.file = file;
    },
    //获取markdown输入的文字
    getMarkdownHtml(key, val) {
      this[key] = val;
    },
    getMarkdownText(key, val) {
      this[key] = val;
    },
    //设置上传的formData对象
    setUploadFormData() {
      let formData = new FormData();
      formData.append(
        "affiliation",
        this.pluginBelonging == this.$t("community.dvadmin") ? 1 : 0
      );
      formData.append("tab_name", this.pluginTag);
      formData.append("brief", this.pluginDes);
      formData.append("name", this.pluginName);
      formData.append("version", `V${this.pluginVersions}`);
      formData.append("version_type", this.versionsType);
      formData.append("plugin_instructions", this.updateNotes);
      formData.append("direction_for_use", this.useNotes);
      formData.append("source_code_file", this.file);
      formData.append("release_form", this.radio_button == "free" ? "0" : "1");
      let currency;
      this.paymentMethod == "$" ? (currency = "1") : (currency = "0");
      if (currency == 0) {
        formData.append("rnb", this.money);
      } else {
        formData.append("dollar", this.money);
      }
      formData.append("currency", currency);
      formData.append("direction_markdown_text", this.useMarkdown);
      formData.append("plugin_markdown_text", this.updateMarkdown);
      return formData;
    },
    //编辑插件时获取插件信息
    getMyPluginInfo() {
      getauth(`software/api/v1/my_soft/${this.pluginId}/`).then((res) => {
        this.fileName = res.source_code_file;
        this.pluginBelonging =
          res.affiliation == 0
            ? this.$t("community.greaterwms")
            : this.$t("community.dvadmin");
        this.pluginName = res.name;
        this.pluginDes = res.brief;
        this.pluginVersions = res.versions[0].version;
        this.versionsType = res.versions[0].version_type;
        this.updateMarkdown = res.versions[0].plugin_markdown_text;
        this.useMarkdown = res.direction_markdown_text;
        this.radio_button = res.release_form == 0 ? "free" : "pay";
        if (res.release_form == 1) {
          this.paymentMethod = res.currency == 0 ? "￥" : "$";
          if (res.dollar) {
            this.money = res.dollar;
          } else {
            this.money = res.rnb;
          }
        }
        res.tab.forEach((element, index) => {
          let separator;
          if (index === res.tab.length - 1) {
            separator = "";
          } else {
            separator = ",";
          }
          this.pluginTag = this.pluginTag + element.tab_name + separator;
        });
      });
    },
  },
  created() {
    document.body.scrollTop = 0;
    this.pluginId = this.$route.params.id;
    if (this.pluginId != "newPlugin") {
      this.getMyPluginInfo();
      this.submit = uploadput;
      this.submitUrl = `software/api/v1/my_soft/${this.pluginId}/`;
    } else {
      this.submit = uploadpost;
      this.submitUrl = "software/api/v1/add/";
    }
  },
});
</script>
<style scoped lang="sass">
.input_placeholder
    line-height: 40px
    height: 40px
    position: absolute
    left: 0px
    cursor: text
    color: #999999
.release_btn_undisabled
    width: 400px
    background: $primary
    color: white
.release_btn_disabled
    width: 400px
    background: #e6e6e6
    color: #999999
</style>

