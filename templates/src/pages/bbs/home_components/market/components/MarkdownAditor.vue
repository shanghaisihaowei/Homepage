<template>
  <div class="relative-position markdown_container">
    <div v-if="needUploadImg" class="editor_tool flex">
      <q-btn color="grey-6" flat icon="add_photo_alternate">
        <input
          style="
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
          "
          class="q-mb-sm"
          ref="img"
          type="file"
          @change="uploadImg"
        />
      </q-btn>
      <q-btn
        @click="changeStyle('*')"
        color="grey-6"
        flat
        icon="format_italic"
      ></q-btn>
      <q-btn
        @click="changeStyle('**')"
        color="grey-6"
        flat
        icon="format_bold"
      ></q-btn>
    </div>
    <div
      v-show="showPholder"
      v-html="placeholder"
      @click="this.$refs.input.focus()"
      :style="{
        zIndex: '1',
        position: 'absolute',
        top: needUploadImg ? '55px' : '15px',
        left: '15px',
        cursor: 'text',
      }"
    ></div>
    <div :id="'input' + this.idIndex">
      <q-input
        ref="input"
        :class="['input_textarea', showPholder ? '' : 'bg-grey-1']"
        type="textarea"
        v-model="value"
        outlined
        @focus="hidePlaceholder()"
        @blur="showPlaceholder()"
      >
        <template v-slot:append>
          <div
            class="markdown"
            v-html="markedValue"
            :style="{
              borderLeft: showPholder ? '' : '1px solid grey',
              height: '100%',
              wordWrap: 'break-word',
              wordBreak: 'break-all',
              fontSize: '14px',
              padding: '10px',
            }"
          ></div>
        </template>
      </q-input>
    </div>
  </div>
</template>
<script>
import { marked } from "marked";
import { postauth } from "boot/axios.js";

export default {
  props: {
    placeholder: "",
    needUploadImg: "",
    idIndex: "",
    markdownText: "",
  },
  data() {
    return {
      value: "",
      showPholder: true,
      imgVal: "",
      domIndex: "",
    };
  },
  computed: {
    markedValue() {
      return marked(this.value);
    },
  },
  watch: {
    value(val) {
      if (val) {
        this.hidePlaceholder();
      } else {
        this.$emit("getMarkdownHtml", marked(this.value));
      }
    },
    markdownText: {
      handler(val) {
        if (val) {
          this.value = val;
          this.$emit("getMarkdownHtml", marked(this.value));
        }
      },
      immediate: true,
    },
  },
  methods: {
    changeStyle(val) {
      let dom = document.getElementById(`input${this.idIndex}`).children[0]
        .children[0].children[0].children[0].children[0];
      let start = dom.selectionStart;
      let end = dom.selectionEnd;
      this.value =
        this.value.slice(0, start) +
        val +
        this.value.slice(start, end) +
        val +
        this.value.slice(end);
    },
    hidePlaceholder() {
      this.showPholder = false;
    },
    showPlaceholder() {
      if (!this.value) {
        this.showPholder = true;
      }
      this.$emit("getMarkdownHtml", marked(this.value));
      this.$emit("getMarkdownText", this.value);
    },
    uploadImg(e) {
      let formData = new FormData();
      formData.append("upload", e.target.files[0]);
      postauth("article/api/v1/upload_file/", formData).then((res) => {
        this.value = `${this.value}![avatar](${window.g.BaseUrl}${res.result[0].url})`;
        this.$refs.img.value = "";
        //防止直传图片导致blur事件不触发
        this.$emit("getMarkdownHtml", marked(this.value));
        this.$emit("getMarkdownText", this.value);
      });
    },
  },
};
</script>
<style  lang="sass">
.editor_tool
    height: 40px
    width: 100%
    border-top: 1px solid #D4D4D4
    border-left: 1px solid #D4D4D4
    border-right: 1px solid #D4D4D4
    border-top-left-radius: 4px
    border-top-right-radius: 4px
</style>
