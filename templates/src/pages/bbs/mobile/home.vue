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
                    <q-item-section class="col-10 menu_left  text-left">
                      {{ $t("community.backfontpage") }}
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section class="col-10 menu_left  text-left">
                      {{ $t("index.osc") }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable :to="{ name : 'articleList' }" v-ripple class="row">
                    <div class="col-1">
                    </div>
                    <q-item-section class="col-10 menu_left  text-left">
                      GreaterWMS{{ $t("index.osc") }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable :to="{ name : 'articleListDV' }" v-ripple class="row">
                    <q-item-section class="col-1">
                    </q-item-section>
                    <q-item-section class="col-10 menu_left  text-left">
                      DVadmin{{ $t("index.osc") }}
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section class="col-10 menu_left  text-left">
                      {{ $t("index.navbar.market") }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable to="/community/mobile/pluginsList/GreaterWMS" v-ripple class="row">
                    <q-item-section class="col-1">
                    </q-item-section>
                    <q-item-section class="col-10 menu_left  text-left">
                      GreaterWMS{{ $t("community.plugin") }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable to="/community/mobile/pluginsList/DVAdmin" v-ripple class="row">
                    <q-item-section class="col-1">
                    </q-item-section>
                    <q-item-section class="col-10 menu_left  text-left">
                      DVAdmin{{ $t("community.plugin") }}
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
            </q-drawer>
          </div>
          <div class="col-1"></div>
          <div class="col-7">
            <q-avatar square>
              <img :src="mobileLogo" alt="">
            </q-avatar>
            <span>
           {{ titletype }} {{ $t("index.osc") }}
          </span>
          </div>
          <div class="col-2">
            <div style="float: right">
              <q-btn
                v-if="langlable !== '简体中文'"
                round
                flat
                label="CN"
                @click="langChange('zh-hans')"
                :to="{ name: 'community' }"
              />
              <q-btn
                v-if="langlable === '简体中文'"
                round
                flat
                label="EN"
                @click="langChange('en-US')"
                :to="{ name: 'community' }"
              />
            </div>
          </div>
        </q-toolbar>
      </q-header>
      <q-page-container>
        <q-page>
          <q-scroll-area :thumb-style="thumbStyle"
                         :bar-style="barStyle"
                         :visible="visible"
                         ref="scrollAreaHome"
                         @scroll="onScroll()"
                         :delay="1500"
                         :style="{ height: scroll_height, width: scroll_width}"
          >
          <router-view/>
          </q-scroll-area>
          <q-page-sticky
            v-if="pagelocation > 0.2"
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
      scroll_width: this.$q.screen.width + '' + 'px',
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
      var _this = this;
      _this.$store.dispatch(
        "pagelocation/pageLocationChange",
        _this.$refs.scrollAreaHome.getScrollPercentage().top
      );
    },
  },
  computed: {
    pagelocation() {
      return this.$store.state.pagelocation.pagelocation;
    },
    mobileLogo() {
      return this.$store.state.bbsChange.mobileLogo;
    },
    titletype() {
      return this.$store.state.bbsChange.titletype;
    },
  },
  mounted() {
    var _this = this
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
.bg_w {
  background-color: white;
  border-bottom: 1px #D8D8D8 solid;
}
.bg_b {
  background-color: #116FEC;
  border-bottom: 1px #D8D8D8 solid;
}
</style>
