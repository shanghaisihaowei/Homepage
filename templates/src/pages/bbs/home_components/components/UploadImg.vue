<template>
  <div>
    <div
      style="
        width: 250px;
        height: 190px;
        border: 1px solid #d0d0d0;
        text-align: center;
        position: relative;
      "
    >
      <img style="margin: 55px 0 20px 0" src="statics/add_img.svg" />
      <div style="font-size: 16px; color: #116fec">{{ text }}</div>
      <input
        ref="input"
        style="
          position: absolute;
          width: 100%;
          height: 100%;
          top: 0;
          left: 0;
          opacity: 0;
        "
        :class="isSubmit ? '' : 'img_index'"
        @change="uploadImg"
        type="file"
      />
      <img
        style="width: 100%; height: 100%; position: absolute; top: 0; left: 0"
        v-if="img_src"
        :src="img_src"
      />
    </div>
  </div>
</template>
<script>
export default {
  props: {
    text: "",
    side: "",
    imgSrc: "",
    isSubmit: "",
  },
  data() {
    return {
      img_src: "",
    };
  },
  watch: {
    imgSrc: {
      handler(val) {
        if (val) {
          this.img_src = val;
        }
      },
    },
  },
  methods: {
    uploadImg(e) {
      if (e.target.files[0].size > 2097152) {
        this.$q.notify({
          message: this.$t("community.e_shop_view.img_oversize"),
          icon: "close",
          color: "negative",
        });
        this.$refs.input.value = "";
      } else {
        let reads = new FileReader();
        reads.readAsDataURL(e.target.files[0]);
        setTimeout(() => {
          this.img_src = reads.result;
        }, 200);
        this.$emit("getUploadImg", this.side, e.target.files[0]);
      }
    },
  },
};
</script>
<style scoped lang="sass">
.img_index
    z-index: 100
</style>