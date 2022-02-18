<template>
  <div style="padding-bottom: 30px">
    <div class="row q-pa-md" style="padding-top: 2%">
      <div class="col-2"></div>
      <!--                左侧联系我们-->
      <div class="col-5">
        <!--                  联系我们-->
        <div class="my-font" style="font-size: 24px;font-weight: 500;color: #333333;">
          {{ $t('index.navbar.contact') }}
        </div>
        <!--                  公司简介-->
        <div class="my-font my_ctt_msg" style="width: 90%;margin-top: 2%;padding-bottom: -1%">
          {{ $t('contact.tip') }}
        </div>
        <!--                  联系方式-->
        <div class="row" style="margin-top: 8%">
          <div class="col-8">
            <!--                      邮箱-->
            <div style="margin-top: 0">
              <q-img
                width="16px"
                src="statics/our_email.svg"
              />
              <a class="my-font-D my_ctt_way" href="mailto:mail@56yhz.com" style="margin-left: 15px; text-decoration: none">
                          mail@56yhz.com
                        </a>
            </div>
            <!--                      地址-->
            <div style="margin-top: 2.5%">
              <q-img
                width="16px"
                src="statics/address.svg"
              />
              <span class="my_ctt_address my-font" style="margin-left: 15px">
                          {{ $t('contact.address') }}
                        </span>
            </div>
          </div>
        </div>
        <!--                  社交媒体-->
        <div class="my-font" style="font-size: 24px;font-weight: 500;color: #333333; margin-top: 6%">
          {{ $t('contact.media') }}
        </div>
        <div class="row" style="margin-top: 4%">
          <div class="col-2" v-show="lang === 'zh-hans'">
            <a
              href="https://space.bilibili.com/407321291?from=search&seid=13742177409505900904&spm_id_from=333.337.0.0">
              <q-img
                width="100px"
                src="statics/bilibili.svg"
              />
            </a>
            <div style="margin-top: 20%;margin-left:20%">{{ $t('contact.bilbili') }}</div>
          </div>
          <div class="col-2" v-show="lang === 'zh-hans'"></div>
          <div class="col-2">
            <a href="https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA">
              <q-img
                width="64px"
                src="statics/youtube.svg"
              />
            </a>
            <div style="margin-left: 5%;margin-top: 20%">{{ $t('contact.youtube') }}</div>
          </div>
          <div class="col-2"></div>
          <!--                  知乎-->
          <!--                  <div class="col-2" v-show="lang === 'zh-hans'">-->
          <!--                    <a href="https://www.zhihu.com/people/greaterwms">-->
          <!--                      <q-img-->
          <!--                        width="100px"-->
          <!--                        src="statics/zhihu.svg"-->
          <!--                      />-->
          <!--                    </a>-->
          <!--                    <div v-show="lang === 'zh-hans'" style="margin-left: 20%;margin-top: 20%">{{ $t('contact.zhihu') }}</div>-->
          <!--                    <div v-show="lang === 'zh-hant'" style="margin-left: 20%;margin-top: 20%">{{ $t('contact.zhihu') }}</div>-->
          <!--                    <div v-show="lang === 'en-US'" style="margin-left: 5%;margin-top: 20%">{{ $t('contact.zhihu') }}</div>-->
          <!--                    <div v-show="lang === 'ja'" style="margin-left: -5%;margin-top: 20%">{{ $t('contact.zhihu') }}</div>-->
          <!--                  </div>-->
        </div>
      </div>
      <!--                右侧地图-->
      <div class="col-3 row">
        <div class="my-font" style="font-size: 24px;font-weight: 500;color: #333333;">
          {{ $t('contact.our_map') }}
        </div>
        <!--                百度地图-->
          <q-img
            v-show="lang === 'zh-hans'"
            class="col-12"
            style="height:498px;border:#ccc solid 1px;margin-top: 6%"
            src="statics/map_right.svg"
          />
        <q-img
          v-show="lang !== 'zh-hans'"
          src="statics/map2.png"
        />
      </div>
      <div class="col-1"></div>
    </div>
    <!--            分隔线-->
    <div style="margin-top: 2%"></div>
    <q-separator style="width: 67%;margin: 0 auto;"/>
    <!--            联系我们留言-->
    <div class="row q-pa-md" style="margin-top: 3%">
      <div class="col-2"></div>
      <div class="col-4">
        <div class="my-font" style="font-size: 24px;font-weight: 500;color: #333333;">
          {{ $t('contact.us') }}
        </div>
      </div>
    </div>

<!--    下啦选择内容和姓名-->
    <div class="row q-pa-md">
      <div class="col-2"></div>
      <div class="col-8 row">
        <!--                您的信息是关于什么内容？-->
        <div class="my_ctt_message_top my-font col-6">
          <div>
            {{ $t('contact.about') }}
          </div>
          <!--                下拉选择问题类型-->
          <q-select
            v-model=about_modle
            style="margin-top: 2%;width: 90%"
            :label="about_lable"
            outlined
            :options="options"
            @keyup="getisValue"
          >
          </q-select>
        </div>
        <div class="my-font my_ctt_message_top col-6">
          <!--                您的姓名-->
          <div style="margin-left: 12%">
            {{ $t('contact.name') }}
          </div>
          <q-input
            style="margin-top: 2%;width: 90%;margin-left: 12%"
            outlined
            v-model="name"
            @keyup="getisValue"
          ></q-input>
        </div>
      </div>
      <div class="col-2"></div>
    </div>
<!--    联系电话和邮箱-->
    <div class="row q-pa-md">
      <div class="col-2"></div>
      <div class="col-8 row">
        <!--                您的信息是关于什么内容？-->
        <div class="my_ctt_message my-font col-6">
          <div>
            {{ $t('contact.tel') }}
          </div>
          <q-input
            style="margin-top: 2%;width: 90%"
            outlined
            v-model="tel"
            :rules="[ val => val.length <= 11 || ver_msg.tel]"
          ></q-input>
        </div>

        <div class="my-font my_ctt_message col-6">
          <div style="margin-left: 12%">
            {{ $t('contact.email') }}
          </div>
          <q-input
            style="margin-top: 2%;width: 90%;margin-left: 12% "
            outlined
            v-model="email"
            @keyup="getisValue"
            :rules="[val => val && email.indexOf('@') !== -1 && email.indexOf('.') !== -1 || ver_msg.email]"
          ></q-input>
        </div>
      </div>
      <div class="col-2"></div>
    </div>
    <!--            留言框-->
    <div class="row q-pa-md">
      <div class="col-2"></div>
      <div class="col-8">
        <div class="my-font my_ctt_msg" style="font-size: 18px;">{{ $t('contact.message') }}</div>
        <textarea
          @keyup="getisValue"
          v-model="msg"
          type="textarea"
          autocapitalize="sentences"
          maxlength="200"
          style="width: 101%; height: 270px; resize: none;border: 1px #C2C2C2 solid "
        />
      </div>
      <div class="col-2"></div>
    </div>
    <!--            提交按钮-->
    <div class="row q-pa-md">
      <div class="col-2"></div>
      <div class="col-8 row">
        <q-btn
          :label="$t('index.submit')"
          :class="{'my-font my_subBtn': isfull === false ,'my-font my_subBtnChange': isfull === true}"
          style="width:100%;height: 66px;font-size: 24px;font-weight: 400;margin-left: 1%"
          unelevated
          @click="submit_massage"
        />
      </div>
      <div class="col-2"></div>
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
.my_ctt_message_top {
  font-size: 18px;
  font-weight: 400;
  color: #333333;
  margin-top: 1%;
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
import { createMetaMixin, openURL } from "quasar";
import { defineComponent, ref } from "vue";
import { post } from "boot/axios";

export default defineComponent({
  name: "contact_us",
  data() {
    return {
      title: '',
      meta: {},
      lang: this.$q.cookies.get('lang'),
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
      tel: '',
      name: '',
      email: '',
      cap: '',
      msg: '',
      isfull: false,
      isnull: true,
      issued_msg: [],
      ver_msg: {
        email: this.$t('contact.verify_msg.email'),
        tel: this.$t('contact.verify_msg.tel')
      }
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
    // 提交留言
    submit_massage() {
      var _this = this
      if (_this.isnull === false && _this.email.indexOf('@') && _this.email.indexOf('.')) {
        var msgs = {
          your_name: _this.name,
          your_email:  _this.email,
          leave_word: _this.msg,
          your_phone: _this.tel,
          options: _this.options.indexOf(_this.about_modle)
        }
        post('contact/api/v1/', msgs).then(res => {
          _this.$q.notify({
            message: _this.$t('index.success'),
            icon: 'check',
            color: 'green'
          })
          _this.$router.push('/Homepage')
        }).catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          }
        )
      } else {
        _this.$q.notify({
          message: _this.$t('contact.isinputfull'),
          icon: 'close',
          color: 'negative'
        })
      }
    },
    getisValue() {
      var _this = this
      if (_this.about_modle && _this.name && _this.email && _this.msg) {
        _this.isfull = true
        _this.isnull = false
      } else {
        _this.isfull = false
        _this.isnull = true
      }
    },
  },
  created() {
    var _this = this
    if (_this.lang === 'zh-hans') {
      _this.title = 'GreaterWMS - 联系我们'
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
      _this.title = 'GreaterWMS - Contact Us'
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
