<template>
  <div>
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
          {{ $t("community.e_shop_view.plugin_name") }}：
        </div>
        <q-input v-model="pluginName" disable outlined dense></q-input>
      </q-card-section>
      <q-card-section>
        <div class="text-h6">
          {{ $t("community.e_shop_view.update_record") }}：
        </div>
        <timeline :timeline="timelineList"></timeline
      ></q-card-section>
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
                V
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
          {{ $t("community.e_shop_view.update_explain") }}:
        </div>
        <markdown-aditor
          :placeholder="placeholder_update"
          @getMarkdownHtml="getMarkdownHtml"
          @getMarkdownText="getMarkdownText"
          :needUploadImg="false"
          :idIndex="0"
        ></markdown-aditor>
      </q-card-section>
      <q-card-section>
        <upload-file @getUploadFile="getUploadFile"></upload-file>
      </q-card-section>
      <q-card-section class="text-center q-mt-lg" style="padding-bottom: 50px">
        <q-btn
          :class="
            disable_update ? 'update_btn_disabled' : 'update_btn_undisabled'
          "
          unelevated
          :disable="disable_update"
          @click="submitUpdate"
          >{{ $t("community.e_shop_view.update") }}</q-btn
        >
      </q-card-section>
    </q-card>
  </div>
</template>
<script>
import Timeline from "./components/Timeline";
import UploadFile from "./components/UploadFile";
import MarkdownAditor from "./components/MarkdownAditor.vue";
import { get, putauth } from "boot/axios";

export default {
  components: {
    Timeline,
    UploadFile,
    MarkdownAditor,
  },
  data() {
    return {
      pluginName: "",
      pluginId: "",
      pluginVersions: "",
      updateNotes: "",
      showPlaceholder: true,
      showVersionsPholder: true,
      timelineList: "",
      file: "",
      versionsType: "",
      markdownText: "",
      versionsOptions: [
        this.$t("community.e_shop_view.official_version"),
        this.$t("community.e_shop_view.beta_version"),
      ],
      placeholder_update: `<div style='color:#999999'>${this.$t(
        "community.e_shop_view.placeholder_update"
      )}</div>`,
    };
  },
  computed: {
    disable_update() {
      if (
        this.file &&
        this.pluginVersions &&
        this.versionsType &&
        this.updateNotes
      ) {
        return false;
      } else {
        return true;
      }
    },
  },
  methods: {
    //查询插件名称
    getPluginDetail() {
      get("software/api/v1/softwaregetret/" + this.pluginId + "/").then(
        (res) => {
          if (res.code !== 998) {
            this.pluginName = res.name;
            this.timelineList = res.versions;
          }
        }
      );
    },
    getMarkdownHtml(val) {
      this.updateNotes = val;
    },
    getMarkdownText(val) {
      this.markdownText = val;
    },
    getUploadFile(file) {
      this.file = file;
    },
    setUpdateFormData() {
      let formData = new FormData();
      formData.append("source_code_file", this.file);
      formData.append("version", `V${this.pluginVersions}`);
      formData.append("plugin_instructions", this.updateNotes);
      formData.append("version_type", this.versionsType);
      formData.append("plugin_markdown_text", this.markdownText);
      return formData;
    },
    submitUpdate() {
      putauth(
        `software/api/v1/add/${this.pluginId}/`,
        this.setUpdateFormData()
      ).then((res) => {
        this.$router.push({
          path: "/community/myReleasedPlugins",
        });
      });
    },
  },
  created() {
    this.pluginId = this.$route.params.id;
    document.body.scrollTop = 0;
    this.getPluginDetail();
  },
};
</script>
<style scoped lang="sass">
.update_btn_undisabled
    width: 400px
    background: $primary
    color: white
.update_btn_disabled
    width: 400px
    background: #e6e6e6
    color: #999999
</style>
