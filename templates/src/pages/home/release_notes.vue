<template>
  <div id="top">
    <div class="row q-pa-md" style="padding-top: 2%">
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
                V 2.1
              </q-item-section>
            </q-item>

          </q-list>
        </div>
      </div>
      <!--              中间时间轴-->
      <div class="col-5 q-pa-md" style="margin-left: 3%;margin-top: 2.3%">
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
      <div class="col-3"></div>
    </div>
    <!--              页脚-->
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
import {createMetaMixin, openURL } from "quasar";
import {defineComponent, ref} from "vue";
import { get } from "boot/axios";

export default defineComponent({
  name: "contact_us",
  data() {
    return {
      title: '',
      meta: {},
      lang: this.$q.cookies.get('lang'),
      link: 'inbox',
      layout: 'comfortable',
      side: 'right',
      porint: [],
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
