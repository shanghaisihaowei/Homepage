<template>
  <div id="top">
    <div class="row q-pa-md" style="margin-top: 2%">
      <div class="col-2"></div>
      <div class="col-2">
        <div class="my-font" style="font-size: 24px;font-weight: 500;color: #333333">
          {{ $t('avatar3.issued') }}
        </div>
        <!--                左侧版本选择-->
        <div style="height:90%;margin-top: 12%;border-right: 1px #DDDDDD solid">
          <q-list bordered class="rounded-borders text-primary" style="border: 0">
            <q-item
              clickable
              v-ripple
              style="color: #333333"
              :active="link === 'inbox'"
              @click="link = 'inbox'"
              active-class="my-menu-link"
            >
              <q-item-section style="font-size: 18px;font-weight: 400">
                V 2.1.0
              </q-item-section>
            </q-item>

            <q-item
              style="color: #333333"
              clickable
              v-ripple
              :active="link === 'outbox'"
              @click="link = 'outbox'"
              active-class="my-menu-link"
            >
              <q-item-section style="font-size: 18px;font-weight: 400">
               V 2.0.0
              </q-item-section>
            </q-item>

          </q-list>
        </div>
      </div>
      <!--              中间时间轴-->
      <div class="col q-pa-md" style="margin-left: 3%;margin-top: 2.3%">
        <q-timeline :layout="layout" :side="side" color="secondary">

          <q-timeline-entry
            v-for="(item,index) in issued_msg"
            class="my-font timeline_entry_title"
            side="left"
            :icon=porint[index]
            color="grey-5"
          >
            <template v-slot:title>
              <div style="font-size: 30px">
                {{ item.title }}
              </div>
            </template>
            <template v-slot:subtitle>
              <div style="font-size: 18px;font-weight: 400;color: #333333;margin-right: 20%">
                {{ item.iteration_time }}
              </div>
            </template>
            <ul >
              <li
                v-for="(e,i) in issued_msg[index].details_set"
                type="disc"
                style="width: 120%;margin-top: 20px"
                class="my-font timeline_entry_msg show_oneline"
              >
                {{ e.content }}
              </li>
            </ul>
          </q-timeline-entry>

<!--          <q-timeline-entry-->
<!--            v-for="(item,index) in issued_msg"-->
<!--            v-show="item.node === true"-->
<!--            class="my-font timeline_entry_title"-->
<!--            side="left"-->
<!--            icon="img:statics/porint.svg"-->
<!--            color="#D8D8D8"-->
<!--          >-->
<!--            <template v-slot:title>-->
<!--              <div style="font-size: 30px">-->
<!--                {{ item.title }}-->
<!--              </div>-->
<!--            </template>-->
<!--            <template v-slot:subtitle>-->
<!--              <div style="font-size: 18px;font-weight: 400;color: #333333">-->
<!--                {{ item.iteration_time }}-->
<!--              </div>-->
<!--            </template>-->
<!--            <ul >-->
<!--              <li-->
<!--                v-for="(e,i) in issued_msg[index].details_set"-->
<!--                type="disc"-->
<!--                style="width: 120%;margin-top: 20px"-->
<!--                class="my-font timeline_entry_msg show_oneline"-->
<!--              >-->
<!--                {{ e.content }}-->
<!--              </li>-->
<!--            </ul>-->
<!--          </q-timeline-entry>-->

        </q-timeline>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.show_oneline {
  width: 135%;
  word-break: break-all;
  word-wrap: break-word;
}
textarea:focus {
  outline: none !important;
  border: solid 2px #1976D2 !important
}

//.row div{
//  padding: 10px 15px;
//  background: rgba(86,61,124,.15);
//  border: 1px solid rgba(86,61,124,.2)
//}
//
//.row + .row{
//  margin-top: 1rem
//}
.aaa:hover {
  //background-position: right center;
  //box-shadow: 0 12px 20px -11px #5b86e5;
  background: #ffffff;
  border-radius: 26px;
  box-shadow: 0px 10px 30px 9px rgba(192, 192, 192, 0.10);
  transition: all 0.3s ease-in-out;
}

.aaa {
  width: 90%;
}

tr td a {
  color: #666666;
  text-decoration: none
}

tr td a:hover, tr td a:active {
  color: #999999;
  text-decoration: none
}

.triangle {
  width: 0;
  height: 0;
  border-top: 13px solid transparent;
  border-bottom: 13px solid transparent;
  border-right: 13px solid transparent;
  border-left: 13px solid white;
}

.my_ctt_msg {
  font-size: 18px;
  font-weight: 400;
  color: #333333;
  line-height: 40px
}

.my_ctt_way {
  font-size: 20px;
  font-weight: 400;
  color: #333333;
}

.my_ctt_address {
  font-size: 16px;
  font-weight: 400;
  color: #333333;
}

.iw_poi_title {
  color: #CC5522;
  font-size: 14px;
  font-weight: bold;
  overflow: hidden;
  padding-right: 13px;
  white-space: nowrap
}

.iw_poi_content {
  font: 12px arial,
  sans-serif;
  overflow: visible;
  padding-top: 4px;
  white-space: -moz-pre-wrap;
  word-wrap: break-word
}

.my_ctt_message {
  font-size: 18px;
  font-weight: 400;
  color: #333333;
  margin-top: 6%;
}

.my_subBtn {
  color: #333333;
  background-color: #DBDBDB;
}

.my_subBtnChange {
  color: #ffffff;
  background-color: #1370EE;
}

.my-menu-link {
  color: #333333;
  background: #F4F4F4;
  border-right: 3px solid #1370EE;
}

.timeline_entry_title {
  font-size: 22px;
  font-weight: 400;
  color: #333333;
}

.timeline_entry_msg {
  font-size: 14px;
  font-weight: 400;
  color: #333333;
}

.tool_tip {
  background-color: #116FEC;
  color: white;
}
</style>

<script>
import {createMetaMixin, LocalStorage, openURL, Screen} from "quasar";
import {defineComponent, ref} from "vue";
import {getauth, post} from "boot/axios";

export default defineComponent({
  name: "contact_us",
  data() {
    return {
      title: '',
      meta: {},
      lang: this.$i18n.locale,
      langlable: '',
      about_lable: this.$t('contact.about_type.zero'),
      about_modle: '',
      options: [
        this.$t('contact.about_type.one'),
        this.$t('contact.about_type.two'),
        this.$t('contact.about_type.three'),
        this.$t('contact.about_type.four'),
        this.$t('contact.about_type.five')
      ],
      contact: 1,
      wechat: true,
      bilibili: false,
      link: 'inbox',
      porint: [],
      navbar: {
        front_page: this.$t('index.navbar.frontpage'),
        community: this.$t('index.navbar.community'),
        market: this.$t('index.navbar.market'),
        demo: this.$t('index.navbar.demo'),
        contact: this.$t('index.navbar.contact'),
        issued: this.$t('avatar3.issued')
      },
      visible: false,
      scroll_width: Screen.width + '' + 'px',
      scroll_height: Screen.height + '' + 'px',
      scroll_height2: Screen.height * 3.8 + '' + 'px',
      scroll_height3: Screen.height * 30 % +'' + 'px',
      thumbStyle: {
        right: '4px',
        borderRadius: '5px',
        backgroundColor: '#E0E0E0',
        width: '8px',
        opacity: 0.75
      },
      barStyle: {
        right: '2px',
        borderRadius: '9px',
        backgroundColor: '#EEEEEE',
        width: '12px',
        opacity: 0.2
      },
      pagelocation: 0,
      code_warehous: this.$t('index.code_warehouse'),
      video: {
        label: 'Tears of Steel',
        poster: 'media/TearsOfSteel/TearsOfSteel.jpeg',
        sources: [
          {
            src: 'https://www.bilibili.com/video/BV177411P7d1?p=8&t=3.8',
            type: 'video/mp4'
          }
        ]
      },
      tel: '',
      name: '',
      email: '',
      cap: '',
      msg: '',
      isfull: false,
      isnull: true,
      layout: 'comfortable',
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
    // 获取发行说明
    getRelease_notes() {
      var _this = this
      getauth('/release/api/v1/timer_shaft/').then(res => {
        _this.issued_msg = res.result
        console.log(_this.issued_msg[0].iteration_time)
        for (var i = 0;i < _this.issued_msg.length; i++) {
          if (_this.issued_msg[i].node === true) {
            _this.porint.push('img:' + _this.issued_msg[i].img)
          } else {
            _this.porint.push('')
          }
        }
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
