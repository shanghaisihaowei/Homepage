<template>
  <div>
    <div class="text-h6">{{ $t("community.e_shop_view.upload_code") }}：</div>
    <div class="flex">
      <div class="upload_file q-my-md">
        <input
          ref="input"
          @change="uploadFile"
          class="input_upload"
          type="file"
        />
        <div style="font-size: 40px">+</div>
        <div>{{ $t("community.e_shop_view.upload_file") }}</div>
      </div>
      <div class="q-pa-md relative-position" style="flex: 1">
        <div style="position: absolute; bottom: 0" class="q-mb-md">
          {{ upload_fileName }}
        </div>
      </div>
    </div>
    <div style="color: #999999">
      <div>{{ $t("community.e_shop_view.notice") }}：</div>
      <div>
        {{ $t("community.e_shop_view.upload_prpmpt1") }}
      </div>
      <div>
        {{ $t("community.e_shop_view.upload_prpmpt2") }}
      </div>
      <div>
        {{ $t("community.e_shop_view.upload_prpmpt3") }}
      </div>
      <div>
        {{ $t("community.e_shop_view.upload_prpmpt4") }}
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    fileName: "",
  },
  data() {
    return {
      upload_fileName: "",
    };
  },
  watch: {
    fileName: {
      handler(val) {
        if (val) {
          this.upload_fileName = val;
        }
      },
      immediate: true,
    },
  },
  methods: {
    uploadFile(e) {
      if (e.target.files[0].size > 209715200) {
        this.$q.notify({
          message: this.$t("community.e_shop_view.file_oversize"),
          icon: "close",
          color: "negative",
        });
        this.$refs.input.value = "";
      } else {
        let fileName = e.target.files[0].name;
        let flieNameArray = fileName.split(".");
        if (flieNameArray[flieNameArray.length - 1] == "zip") {
          this.upload_fileName = fileName;
          this.$emit("getUploadFile", e.target.files[0]);
        } else {
          this.upload_fileName = "";
          this.$q.notify({
            message: this.$t("community.myAccount_view.zip_tip"),
            icon: "close",
            color: "negative",
          });
        }
      }
    },
  },
};
</script>
<style scoped lang="sass">
.upload_file
    width: 100px
    height: 100px
    border: 1px dashed
    color: #116FEC
    text-align: center
    padding: 5px 0 25px 0
    position: relative
    &:hover
        background: lightblue
    .input_upload
        position: absolute
        height: 100%
        width: 100%
        top: 0
        left: 0
        opacity: 0
        cursor: pointer
</style>