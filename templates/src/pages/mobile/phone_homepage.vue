<template>
<div>
<!--  第一个模块-->
  <div class=" my-font">
    <div style="position: relative;display: flex; justify-content: center;">
      <q-img src="statics/phone/bg1.svg"/>
      <div
        style="position:absolute;top:25%;font-size: 20px;font-weight: 500;color: white;letter-spacing: 10px;text-align: center;">
        {{ $t('index.title') }}
        <br>
        {{ $t('index.title2') }}
        <br>
        <!--                    简体中文-->
        <q-btn v-if="langlable === '简体中文'"
               style="background-color:#FFCE05;width: 130px;height: 30px;margin-top: 10%"
               icon="img:statics/phone/gitee-fill-round.svg" @click="goTo('https://gitee.com/Singosgu/GreaterWMS')">
                      <span class="my-font" style="color: #333333;font-size: 15px;font-weight: 500;margin-left: 15%">
                        {{ code_warehous }}
                      </span>
        </q-btn>
        <!--                    繁体中文-->
        <q-btn v-else-if="langlable === '繁體中文'"
               style="background-color:#FFCE05;width: 130px;height: 30px;margin-top: 10%"
               icon="img:statics/phone/gitee-fill-round.svg" @click="goTo('https://gitee.com/Singosgu/GreaterWMS')">
                      <span class="my-font" style="color: #333333;font-size: 15px;font-weight: 500;margin-left: 15%">
                        {{ code_warehous }}
                      </span>
        </q-btn>
        <!--                    日语-->
        <q-btn v-else-if="langlable === '日本語'"
               style="background-color:#FFCE05;width: 200px;height: 40px;margin-top: 5%"
               icon="img:statics/phone/gitee-fill-round.svg" @click="goTo('https://github.com/Singosgu/GreaterWMS.git')">
                      <span class="my-font" style="color: #333333;font-size: 15px;font-weight: 500;margin-left: 5%">
                        {{ code_warehous }}
                      </span>
        </q-btn>
        <!--                    英语-->
        <q-btn v-else-if="langlable === 'English'"
               style="background-color:#FFCE05;width:170px;height: 40px;margin-top: 8%"
               icon="img:statics/phone/gitee-fill-round.svg" @click="goTo('https://github.com/Singosgu/GreaterWMS.git')">
                      <span class="my-font" style="color: #333333;font-size: 15px;font-weight: 500;margin-left: 5%">
                        {{ code_warehous }}
                      </span>
        </q-btn>
      </div>
      <q-img src="/statics/phone/computer.svg" style="position: absolute;top:62%;width: 95%"/>
              <iframe v-show="lang === 'zh-hans'"
                src="//player.bilibili.com/player.html?aid=374944573&bvid=BV1LZ4y1c7T1&cid=319133580&page=1"
                allowfullscreen
                height="34.5%"
                title="bilibili"
                style="position: absolute;top:65%;width: 67%;border-radius: 5px 5px 0 0"
        ></iframe>
        <iframe v-show="lang !== 'zh-hans'"
                height="34.5%"
                src="https://www.youtube-nocookie.com/embed/BozodbF5AzI"
                title="YouTube video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                style="position: absolute;top:65%;width: 67%;border-radius: 5px 5px 0 0"
        >
        </iframe>
    </div>
  </div>
  <!--               第二个模块-->
  <div style="text-align: center;margin-top: 15%">
              <span class="my-font" style="font-size: 18px;font-weight: 500;text-align: center;color: #333333">{{
                  $t('index.features')
                }}</span>
    <q-separator inset
                 style="color: #FFCE05;width: 20px;background-color:#FFCE05;margin-left: 47.8%;margin-top: 1%"/>
<!--    第一行-->
    <div class="row q-pa-md">
      <div class="col-6">
        <div style="height: 27px">
          <q-img
            width="30px"
            src="statics/phone/features1.svg"
          />
        </div>
<!--        标题-->
        <div class="my-font features_tit">
          {{ $t('avtar.tip1') }}
        </div>
<!--        内容-->
        <div class="my-font features_msg" style="width: 90%;margin-left: 8%">
          {{$t('avtar.tip_note1') }}
        </div>
      </div>
      <div class="col-6">
        <div style="height: 27px">
          <q-img
            width="25px"
            src="statics/phone/features2.svg"
          />
        </div>
        <!--        标题-->
        <div class="my-font features_tit">
          {{ $t('avtar.tip2') }}
        </div>
        <!--        内容-->
        <div class="my-font features_msg" style="width: 90%;margin-left: 8%">
          {{$t('avtar.tip_note2') }}
        </div>
      </div>
    </div>
<!--    第二行-->
    <div class="row q-pa-md">
      <div class="col-6">
        <div style="height: 27px">
          <q-img
            width="30px"
            src="statics/phone/features3.svg"
          />
        </div>
        <!--        标题-->
        <div class="my-font features_tit">
          {{ $t('avtar.tip3') }}
        </div>
        <!--        内容-->
        <div class="my-font features_msg" style="width: 90%;margin-left: 8%">
          {{$t('avtar.tip_note3') }}
        </div>
      </div>
      <div class="col-6">
        <div style="height: 27px">
          <q-img
            width="30px"
            src="statics/phone/features4.svg"
          />
        </div>
        <!--        标题-->
        <div class="my-font features_tit">
          {{ $t('avtar.tip4') }}
        </div>
        <!--        内容-->
        <div class="my-font features_msg" style="width: 90%;margin-left: 8%">
          {{$t('avtar.tip_note4') }}
        </div>
      </div>
    </div>
  </div>
<!--  第三个模块-->
  <div class="q-pa-md"
       style="background: url('statics/bg3.svg');background-repeat: no-repeat;background-size: 100%;background-color: #F6F6F8;margin-top: 100px;padding-bottom: 3%"
  >
    <q-img
      width="211px"
      src="statics/phone/computer2.svg"
      style="margin-top: -65px;margin-left: 20%"
    />
    <div class="text-center solve">
      {{ $t('avatar2.tit') }}
    </div>
    <q-separator
      inset
      color="orange-11"
      style="width: 20px;margin: 0 auto"
    />
    <div class="q-pa-md" style="margin-top: 15px">
<!--      01-->
      <div>
        <span class="solve_number my-font-D">
        01
      </span>
        <span class="my-font solve_tit">
        {{ $t('avatar2.tip1') }}
      </span>
        <div class="my-font solve_msg">
          {{ $t('avatar2.tip1_note') }}
        </div>
      </div>
      <!--      02-->
      <div class="solve_tit_top">
        <span class="solve_number my-font-D">
        02
      </span>
        <span class="my-font solve_tit">
        {{ $t('avatar2.tip2') }}
      </span>
        <div class="my-font solve_msg">
          {{ $t('avatar2.tip2_note') }}
        </div>
      </div>
      <!--      03-->
      <div class="solve_tit_top">
        <span class="solve_number my-font-D">
        03
      </span>
        <span class="my-font solve_tit">
        {{ $t('avatar2.tip3') }}
      </span>
        <div class="my-font solve_msg">
          {{ $t('avatar2.tip3_note') }}
        </div>
      </div>
    </div>
  </div>
<!--  第四个模块-->
  <div style="position: relative;">
    <div class="text-center our_awards">
      {{ $t('avatar3.awards') }}
    </div>
    <q-separator
      inset
      color="orange-11"
      style="width: 20px;margin: 0 auto"
    />
    <div>
      <q-img
        src="statics/phone/word.png"
        style="margin-top: 8%"
      />
      <q-img
        width="264px"
        src="statics/phone/certificate.png"
        style="position: absolute;left: 16%;top:24%"
      />
      <div class="triangle" style="position: absolute;left: 11%;top: 74.5%"></div>
      <div style="position: absolute;left: 16%;top: 73%;width: 71%">
                    <span class="my-font awards_msg">
                      {{ $t('avatar3.tip_note1') }}
                    </span>
      </div>
    </div>
  </div>
<!--  页脚-->
  <div class="q-pa-md">
<!--    下划线以上部分-->
    <div class="row footer_first">
      <div class="col-6">
      <q-img
        width="32px"
        src="statics/phone/logo_buttom.svg"
      />
      <span class="my-font-D footer_title">
        {{ $t('index.title') }}
      </span>
        <div class="footer_msg_left">
          {{ $t('avatar3.tip_note2') }}
        </div>
    </div>
      <div v-if="lang !== 'ja'" class="col-2"></div>
      <div v-if="lang === 'zh-hans'" class="col-4 text-center">
        <div class="my-font footer_title_right">
          {{ $t('avatar3.about') }}
        </div>
        <div class="my-font footer_msg_right">
          <span @click="goTo('https://gitee.com/Singosgu/GreaterWMS')">
          {{ $t('index.code_warehouse') }}
        </span>
          <router-link :to="{ name: 'phone_contact_us' }" class="footer_msg_right_margin">
            {{ $t('index.navbar.contact') }}
        </router-link>
        </div>
      </div>
      <div v-if="lang === 'zh-hant'" class="col-4 text-center">
        <div class="my-font footer_title_right">
          {{ $t('avatar3.about') }}
        </div>
        <div class="my-font footer_msg_right">
          <span @click="goTo('https://github.com/Singosgu/GreaterWMS')">
          {{ $t('index.code_warehouse') }}
        </span>
          <router-link :to="{ name: 'phone_contact_us' }" class="footer_msg_right_margin">
            {{ $t('index.navbar.contact') }}
          </router-link>
        </div>
      </div>
      <div v-else-if="lang === 'en-US'" class="col-4 text-center">
        <div class="my-font footer_title_right">
          {{ $t('avatar3.about') }}
        </div>
        <div class="my-font footer_msg_right">
          <span @click="goTo('https://github.com/Singosgu/GreaterWMS')">
          {{ $t('index.code_warehouse') }}
        </span>
        </div>
        <div class="my-font footer_msg_right">
          <router-link :to="{ name: 'phone_contact_us' }" class="footer_msg_right_margin">
            {{ $t('index.navbar.contact') }}
          </router-link>
        </div>
      </div>
      <div v-else-if="lang === 'ja'" class="col-6 text-center">
        <div class="my-font footer_title_right">
          {{ $t('avatar3.about') }}
        </div>
        <div class="my-font footer_msg_right">
          <span @click="goTo('https://github.com/Singosgu/GreaterWMS')">
          {{ $t('index.code_warehouse') }}
        </span>
        </div>
        <div class="my-font footer_msg_right">
          <router-link :to="{ name: 'phone_contact_us' }" class="footer_msg_right_margin">
            {{ $t('index.navbar.contact') }}
          </router-link>
        </div>
      </div>
    </div>
<!--    下划线-->
    <q-separator
      color="grey-5"
      style="width: 95%;margin-top: 34px"
    />
<!--    下划线一下部分-->
    <div class="my-font record_msg text-center">
      {{ $t('avatar3.record_number') }}
      <a href="" style="color: blue">{{ $t('avatar3.icp') }}</a>
      <br>
      {{ $t('avatar3.record_number2') }}
    </div>
  </div>
</div>
  <q-dialog v-model="advertise">
    <q-card class="shadow-0" style="width: 350px;cursor: pointer;background: rgba(0,0,0,0);margin-top: 50px" @click="goTo(advertiseUrl)">
      <img :title="advertiseTitle" src="statics/advertise/100.svg" alt="">
    </q-card>
    <q-card class="shadow-0" style="margin-top: -100px;cursor: pointer; background: rgba(0,0,0,0)" @click="advertise = false">
      <img src="statics/advertise/close.svg" alt="">
    </q-card>
  </q-dialog>
</template>

<style lang="scss" scoped>
.features_tit {
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  margin-top: 20px;
}
.features_msg {
  font-size: 14px;
  font-weight: 400;
  color: #666666;
  margin-top: 15px;
}
.solve {
  font-size: 18px;
  margin-top: 50px;
  font-weight: 500;
  color: #333333;
}
.solve_number {
  font-size: 14px;
  font-weight: 700;
  color: #999999;
}
.solve_tit {
  font-size: 14px;
  font-weight: 500;
  color: #333333;
  margin-left: 13px;
}
.solve_tit_top {
  margin-top: 30px;
}
.solve_msg {
  font-size: 13px;
  font-weight: 300;
  color: #4F4F4F;
  letter-spacing: 2.97px;
  margin-left: 9%;
  margin-top: 20px;
}
.our_awards {
  font-size: 18px;
  font-weight: 500;
  color: #333333;
  letter-spacing: 4.11px;
  margin-top: 50px;
}
.awards_msg {
  font-size: 18px;
  font-weight: 500;
  color: white;
  letter-spacing: 1.64px;
}
.triangle {
  width: 0;
  height: 0;
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-right: 8px solid transparent;
  border-left: 8px solid white;
}
.footer_title {
  font-size: 18px;
  font-weight: 700;
  color: #000000;
  margin-left: 12px;
}
.footer_first {
  margin-top: 48px;
}
.footer_msg_left{
  font-size: 12px;
  font-weight: 400;
  color: #666666;
  line-height: 18px;
  margin-top: 17px;
}
.footer_title_right {
  font-size: 15px;
  font-weight: 500;
  color: #333333;
}
.footer_msg_right {
  font-size: 13px;
  font-weight: 400;
  color: #666666;
  margin-top: 32px;
}
.footer_msg_right_margin {
  text-decoration: none;
  margin-left: 20px;
  color: #666666;
}
.record_msg {
  font-size: 12px;
  font-weight: 400;
  color: #666666;
  margin-top: 25px;
}
.imgs_buttom {
  margin-top: 28px;
}
</style>

<script>
import {defineComponent, ref} from "vue";
import {createMetaMixin, LocalStorage, openURL, Screen} from "quasar";
import {get} from "boot/axios";

export default defineComponent({
  name: "phone_homepage",
  data() {
    return {
      lang: this.$i18n.locale,
      langlable: '',
      scroll_height: Screen.height + '' + 'px',
      code_warehous: this.$t('index.code_warehouse'),
      advertise: true,
      advertiseUrl: '',
      advertiseTitle: ''
    }
  },
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.title,
        meta: this.meta
      }
    })
  ],
  methods: {
    goTo(e) {
      openURL(e)
    },
    langChange(e) {
      var _this = this
      _this.lang = e
      window.setTimeout(() => {
        location.reload()
      }, 1)
    },
    onScroll() {
      var _this = this
      _this.pagelocation = _this.$refs.scrollAreaIndex.getScrollPercentage().top
    },
    //获取广告链接
    getadvertiseUrl () {
      var _this = this
      get('resp/api/v1/banner').then(res => {
        _this.advertiseUrl = res[1].link
        _this.advertiseTitle = res[1].title
      })
    }
  },
  mounted() {
    this.getadvertiseUrl()
    if (this.$q.cookies.has('area')) {
      if (this.$q.cookies.get('area') !== 'China') {
        this.advertise = false
      } else  {
        this.advertise = true
      }
    }
  },
  created() {
    var _this = this
    _this.title = 'GreaterWMS - 开源社区'
    _this.meta = {
      description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
      keywords: {name: 'keywords', content: 'Quasar website'},
      equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
      // note: for Open Graph type metadata you will need to use SSR, to ensure page is rendered by the server
      ogTitle: {
        property: 'og:title',
        // optional; similar to titleTemplate, but allows templating with other meta properties
        template(ogTitle) {
          return `${ogTitle} - GreaterWMS`
        }
      }
    }
    if (_this.lang === 'zh-hans') {
      _this.langlable = '简体中文'
    } else if (_this.lang === 'zh-hant') {
      _this.langlable = '繁體中文'
    } else if (_this.lang === 'ja') {
      _this.langlable = '日本語'
    } else if (_this.lang === 'en-US') {
      _this.langlable = 'English'
    } else {
      _this.langlable = 'English'
    }
  },
  watch: {
    lang(lang) {
      var _this = this
      LocalStorage.set('lang', lang)
      _this.$i18n.locale = lang
    }
  },
  setup() {
    const position = ref(0)
    const scrollAreaIndex = ref(null)
    return {
      position,
      scrollAreaIndex,
      ScrollToTop() {
        scrollAreaIndex.value.setScrollPosition('vertical', position.value, 100)
      }
    }
  }
})
</script>

<style scoped>

</style>
