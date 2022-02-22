<template>
    <q-layout view="hhh LpR fFf" class="bg-grey-1">
      <q-header class="bg-white head_shadow" reveal>
        <q-toolbar class="GPLAY__toolbar mobile_toolbar row">
          <div class="col-2">
            <q-btn flat @click="drawerLeft = !drawerLeft" round dense icon="menu"/>
            <q-drawer
              v-model="drawerLeft"
              show-if-above
              :width="200"
              :breakpoint="700"
              elevated
              content-class="bg-primary text-white"
            >
              <div style="color: #333333">
                <q-list separator>
                  <!--            首页-->
                  <q-item class="row">
                    <q-item-section class="col-9">
                    </q-item-section>
                    <q-item-section class="col-3">
                      <q-btn
                        round
                        size="xs"
                        flat
                        icon="img:statics/phone/close.svg"
                        @click="drawerLeft = false"
                      />
                    </q-item-section>
                  </q-item>
                  <q-item clickable :to="{ name : 'phone' }" v-ripple>
                    <q-item-section class="col-10 menu_left my-font text-left">
                      {{ $t("community.backfontpage") }}
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section class="col-10 menu_left my-font text-left">
                      {{ $t("index.osc") }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable :to="{ name : 'articleList' }" v-ripple class="row">
                    <div class="col-1">
                    </div>
                    <q-item-section class="col-10 menu_left my-font text-left">
                      GreaterWMS{{ $t("index.osc") }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable :to="{ name : 'articleListDV' }" v-ripple class="row">
                    <q-item-section class="col-1">
                    </q-item-section>
                    <q-item-section class="col-10 menu_left my-font text-left">
                      DVadmin{{ $t("index.osc") }}
                    </q-item-section>
                  </q-item>
                  <q-item/>
                </q-list>
              </div>
            </q-drawer>
          </div>
          <div class="col-1"></div>
          <div class="col-7">
            <q-avatar square>
              <img src="statics/logo.svg" alt="">
            </q-avatar>
            <span>
            GreaterWMS {{ $t("index.osc") }}
          </span>
          </div>
          <div class="col-2">
            <div style="float: right">
              <q-btn flat @click="drawerRight = !drawerRight" round dense icon="translate"/>
              <q-drawer
                side="right"
                v-model="drawerRight"
                show-if-above
                :width="200"
                :breakpoint="700"
                elevated
                content-class="bg-primary text-white"
              >
                <div style="color: #333333">
                  <q-list>
                    <!--            语言-->
                    <q-item class="row" style="border-bottom: #D5D5D5 solid 1px">
                      <q-item-section class="col-1">
                        <q-img
                          width="14px"
                          src="statics/phone/language.svg"
                        />
                      </q-item-section>
                      <q-item-section class="col-8">
                      </q-item-section>
                      <q-item-section class="col-3">
                        <q-btn
                          round
                          size="xs"
                          flat
                          icon="img:statics/phone/close.svg"
                          @click="drawerRight = false"
                        />
                      </q-item-section>
                    </q-item>
                    <!--                中文简体-->
                    <q-item clickable v-ripple @click="langChange('zh-hans')" class="border_bottom menu_right">
                      <q-item-section class="menu_left my-font text-left">
                        中文简体
                      </q-item-section>
                    </q-item>
                    <!--                    English-->
                    <q-item clickable @click="langChange('en-US')" v-ripple class="border_bottom menu_right">
                      <q-item-section class="menu_left my-font text-left">
                        English
                      </q-item-section>
                    </q-item>
                  </q-list>
                </div>
              </q-drawer>
            </div>
          </div>
        </q-toolbar>
      </q-header>
      <q-page-container>
        <q-page>
          <q-scroll-area :thumb-style="thumbStyle"
                         :bar-style="barStyle"
                         :visible="visible"
                         ref="scrollAreaIndex"
                         @scroll="onScroll()"
                         :delay="1500"
                         :style="{ height: scroll_height, width: width }"
          >
          <router-view/>
          </q-scroll-area>
          <q-page-sticky
            position="bottom-right"
            :offset="[25, 100]"
          >
            <q-btn
              padding="md"
              icon="img:statics/return.svg"
              style="opacity: 0.18; background: #000000"
              @click="ScrollToTop()"
            >
            </q-btn>
          </q-page-sticky>
        </q-page>
      </q-page-container>
    </q-layout>
</template>

<script>
import {defineComponent, ref} from "vue";

export default defineComponent({
  name: "home",
  data() {
    return {
      lang: this.$i18n.locale,
      langlable: "",
      drawerLeft: false,
      drawerRight: false,
      thumbStyle: {
        right: '4px',
        borderRadius: '5px',
        backgroundColor: '#116FEC',
        width: '8px',
        opacity: 0.5
      },
      barStyle: {
        right: '2px',
        borderRadius: '9px',
        backgroundColor: '#EEEEEE',
        width: '12px',
        opacity: 0.2
      },
      visible: false,
      width: this.$q.screen.width + '' + 'px',
      scroll_height: this.$q.screen.height + '' + 'px',
    }
  },
  methods: {
    // 更换语言
    langChange(e) {
      var _this = this;
      _this.lang = e;
      window.setTimeout(() => {
        location.reload();
      }, 1);
    },
    onScroll() {
      var _this = this
      this.$store.dispatch("pagelocation/pageLocationChange", _this.$refs.scrollAreaIndex.getScrollPercentage().top);
    },
  },
  computed: {
  },
  mounted() {
    var _this = this
    if (_this.$q.platform.is.mobile) {
      this.$router.push({name: 'community_mobile'})
    } else {
      this.$router.push({name: 'community'})
    }
    if (_this.$q.cookies.has('lang')) {
      if (_this.$q.cookies.get('lang') === 'ja') {
        _this.$q.cookies.set('lang', 'en-US')
        location.reload()
      } else if (_this.$q.cookies.get('lang') === 'zh-hant') {
        _this.$q.cookies.set('lang', 'zh-hans')
        location.reload()
      } else {
      }
    } else {
    }
  },
  created() {
    var _this = this
    if (_this.lang === "zh-hans") {
      _this.langlable = "简体中文";
    } else if (_this.lang === "zh-hant") {
      _this.langlable = "繁體中文";
    } else if (_this.lang === "ja") {
      _this.langlable = "日本語";
    } else if (_this.lang === "en-US") {
      _this.langlable = "English";
    } else {
      _this.langlable = "English";
    }
  },
  watch: {
    lang(lang) {
      var _this = this;
      if (_this.$q.cookies.has("lang")) {
        _this.$q.cookies.remove("lang");
      }
      _this.$q.cookies.set("lang", lang);
      _this.$i18n.locale = lang;
    },
  },
  setup() {
    const position = ref(0);
    const scrollAreaHome = ref(null);
    return {
      position,
      scrollAreaHome,
      ScrollToTop() {
        scrollAreaHome.value.setScrollPosition("vertical", position.value, 100);
      },
    };
  },
})
</script>

<style lang="scss" scoped>
.mobile_toolbar {
  background-color: #116FEC
}
</style>
