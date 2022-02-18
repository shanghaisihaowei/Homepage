<template>
    <div class="text-center q-pa-xl my-font tit_top">
      {{ $t('avatar3.issued') }}
    </div>
    <div class="q-pa-md my-font">
      <q-timeline :layout="layout" :side="side" color="secondary">

        <q-timeline-entry
          v-for="(item,index) in issued_msg"
          class="my-font"
          side="right"
          :icon=porint[index]
          color="grey-5"
        >
          <template v-slot:title>
            <div class="w_tit">
              {{ item.title }}
            </div>
          </template>
          <template v-slot:subtitle>
            <div class="w_time">
              {{ item.iteration_time }}
            </div>
          </template>
          <ul style="margin-left: -18px">
            <li
              v-for="(e,i) in issued_msg[index].details_set"
              class="my-font w_li"
            >
              {{ e.content }}
            </li>
          </ul>
        </q-timeline-entry>
      </q-timeline>
    </div>
  <footer class="footer_bgc q-pa-md">
  <div class="row footer_first">
    <div class="col-6">
      <q-img
        width="32px"
        src="statics/phone/logo_white.svg"
      />
      <span class="my-font-D footer_title">
        {{ $t('index.title') }}
      </span>
      <div class="footer_msg_left">
        {{ $t('avatar3.tip_note2') }}
      </div>
    </div>
    <div v-if="lang === 'zh-hans'" class="col-6 text-center">
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
      <div class="my-font text-left footer_msg_right" style="margin-left: 30px">
        <router-link :to="{ name: 'phone_release_note' }" style="text-decoration: none;color: white">
          {{ $t('avatar3.issued') }}
        </router-link>
      </div>
    </div>
    <div v-if="lang === 'zh-hant'" class="col-6 text-center">
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
      <div class="my-font text-left footer_msg_right" style="margin-left: 30px">
        <router-link :to="{ name: 'phone_release_note' }" style="text-decoration: none;color: white">
          {{ $t('avatar3.issued') }}
        </router-link>
      </div>
    </div>
    <div v-else-if="lang === 'en-US'" class="col-6 text-center">
      <div class="my-font footer_title_right">
        {{ $t('avatar3.about') }}
      </div>
      <div class="my-font footer_msg_right">
          <span @click="goTo('https://github.com/Singosgu/GreaterWMS')">
          {{ $t('index.code_warehouse') }}
        </span>
      </div>
      <div class="my-font footer_msg_right">
        <router-link :to="{ name: 'phone_release_note' }" style="text-decoration: none;color: white">
          {{ $t('avatar3.issued') }}
        </router-link>
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
    <a href="" style="color:white">{{ $t('avatar3.icp') }}</a>
    {{ $t('avatar3.record_number2') }}
  </div>
</footer>
</template>

<style lang="scss" scoped>
.tit_top {
  font-size: 17px;
  font-weight: 500;
  color: #333333;
  margin-top: 70px ;
  padding-bottom: 0;
}
.w_time {
  font-size: 12px;
  font-weight: 400;
  color: #999999;
}
.w_tit {
  font-size: 15px;
  font-weight: 500;
  color: #333333;
}
.w_li {
  width: 260px;
  font-size: 13px;
  font-weight: 400;
  color: #333333;
  word-wrap: break-word;
}
.footer_bgc {
  margin-top: 30px;
  background-color: #1370EE;
}
.footer_title {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  margin-left: 12px;
}
.footer_first {
  margin-top: 20px;
}
.footer_msg_left{
  font-size: 12px;
  font-weight: 400;
  color: #ffffff;
  line-height: 18px;
  margin-top: 17px;
}
.footer_title_right {
  font-size: 15px;
  font-weight: 500;
  color: #ffffff;
}
.footer_msg_right {
  font-size: 13px;
  font-weight: 400;
  color: #ffffff;
  margin-top: 32px;
}
.footer_msg_right_margin {
  color: white;
  text-decoration: none;
  margin-left: 20px;
}
.record_msg {
  font-size: 12px;
  font-weight: 400;
  color: #ffffff;
  margin-top: 25px;
}
.imgs_buttom {
  margin-top: 28px;
}
</style>
<script>
import { defineComponent, ref } from "vue";
import { createMetaMixin, openURL } from "quasar";
import { get } from "boot/axios";

export default defineComponent({
  name: "release_notes",
  data () {
    return {
      title: '',
      meta: {},
      lang: this.$q.cookies.get('lang'),
      link: 'inbox',
      porint: [],
      layout: 'dense',
      side: 'right',
      issued_msg: [],
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
    // 获取发行说明
    getRelease_notes() {
      var _this = this
      get('/release/api/v1/timer_shaft/').then(res => {
        _this.issued_msg = res.result
        _this.issued_msg.forEach(item => {
           if (item.node) {
            _this.porint.push('img:' + item.img)
          }
        })
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    }
  },
  mounted() {
    var _this = this
    _this.getRelease_notes()
  },
  created() {
    var _this = this
    if (_this.lang === 'zh-hans') {
      _this.title = 'GreaterWMS - 发行说明'
      _this.meta = {
        description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
        keywords: {name: 'keywords', content: '聚商汇WMS,开源仓库管理系统,仓库管理系统,wms,仓库管理软件,仓库管理,GreaterWMS, greaterwms'},
        equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
        ogTitle: {
          property: 'og:title',
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`
          }
        }
      }
    } else {
      _this.title = 'GreaterWMS - Released Note'
      _this.meta = {
        description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
        keywords: {name: 'keywords', content: 'GreaterWMS - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms'},
        equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
        ogTitle: {
          property: 'og:title',
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`
          }
        }
      }
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
