<template>
  <div class="q-pa-md" style="margin-top: 80px">
<!--    标题-->
    <div class="top_title text-center my-font">
      {{ $t('index.navbar.contact') }}
    </div>
<!--    公司介绍-->
    <div class="my-font top_msg">
      {{ $t('contact.tip') }}
    </div>
<!--    联系方式-->
    <div class="row" style="margin-top: 15px">
      <div class="col-8">
<!--        电话-->
        <div style="margin-top: 20px">
          <q-img
            width="16px"
            src="statics/phone/telephone.svg"
          />
          <span class="contact_way my-font-D">
          {{ $t('contact.telephone') }}
        </span>
        </div>
<!--        邮箱-->
        <div style="margin-top: 20px">
          <q-img
            width="16px"
            src="statics/phone/email.svg"
          />
          <a href="mailto:mail@56yhz.com" class="contact_way my-font-D">
          mail@56yhz.com
        </a>
        </div>
<!--        地址-->
        <div style="margin-top: 20px;width: 85%">
          <q-img
            width="16px"
            src="statics/phone/address.svg"
          />
          <div class="contact_address my-font-D">
          {{ $t('contact.address') }}
          </div>
        </div>
      </div>
      <div v-if="lang === 'zh-hans'" class="col-4">
        <q-img
          src="statics/cus_ser.png"
        />
      </div>
    </div>
<!--    社交媒体-->
    <div class="top_title my-font text-center" style="margin-top: 61px">
      {{ $t('contact.media') }}
    </div>
<!--    平台-->
    <div v-if="lang === 'zh-hans'" class="row q-pa-xl">
      <q-img
        width="24%"
        src="statics/bilibili.svg"
        @click="goTo('https://space.bilibili.com/407321291')"
      />
      <q-img
        width="24%"
        src="statics/zhihu.svg"
        style="margin-left: 50%"
        @click="goTo('https://www.zhihu.com/people/greaterwms')"
      />
    </div>
    <div v-else-if="lang !== 'zh-hans'" class="row" style="margin-top: 20px">
      <q-img
        width="88px"
        src="statics/youtube.svg"
        style="margin: 0 auto"
        @click="goTo('https://youtu.be/BozodbF5AzI')"
      />
    </div>
    <div v-if="lang !== 'zh-hans'" class="text-center my-font" style="font-size: 18px;font-weight: 500;margin-bottom: 70px">
      YouTube
    </div>
<!--    地图-->
    <div v-if="lang === 'zh-hans'">
      <div class="my-font top_title text-center">
        {{ $t('contact.our_map') }}
      </div>
      <div class="col-12" style="height:250px;border:#ccc solid 1px;margin-top: 6%" >
        <q-img
          height="247px"
          src="statics/phone/map.svg"
        />
      </div>
    </div>
    <div v-if="lang !== 'zh-hans'">
      <div class="my-font top_title text-center">
        {{ $t('contact.our_map') }}
      </div>
      <q-img
        style="margin-top: 20px"
        src="statics/map2.png"
      />
    </div>
  </div>
<!--  下划线-->
  <div style="margin-top: 15px"></div>
  <q-separator style="width: 92%;margin: 0 auto;"/>
  <!--            联系我们留言-->
  <div class="my-font top_title text-center" style="margin-top: 30px">
    {{ $t('contact.us') }}
  </div>
  <!--    下啦选择内容和姓名-->
  <div class="my-font q-pa-md" style="margin-top: 30px;padding-bottom: 30px">
    <div class="input_tit my-font ">
      {{ $t('contact.about') }}
    </div>
    <!--                下拉选择问题类型-->
    <q-select
      v-model=about_modle
      style="margin-top: 3%;height: 36px"
      :label="about_lable"
      outlined
      :options="options"
      @keyup="getisValue"
    >
    </q-select>
  </div>
  <!--                您的姓名-->
  <div>
    <div class="q-pa-md my-font input_tit">
      {{ $t('contact.name') }}
    </div>
    <q-input
      class="q-pa-md"
      style="padding-top: 0"
      outlined
      v-model="name"
      @keyup="getisValue"
    ></q-input>
  </div>
<!--联系电话-->
  <div>
    <div class="q-pa-md input_tit my-font">
      {{ $t('contact.tel') }}
    </div>
    <q-input
      class="q-pa-md"
      style="padding-top: 0"
      outlined
      v-model="tel"
      @keyup="getisValue"
    ></q-input>
  </div>
<!--  邮箱-->
  <div>
    <div class="q-pa-md input_tit my-font">
      {{ $t('contact.email') }}
    </div>
    <q-input
      class="q-pa-md"
      style="padding-top: 0"
      outlined
      v-model="email"
      @keyup="getisValue"
      :rules="[val => val && email.indexOf('@') !== -1 && email.indexOf('.') !== -1 || ver_msg.email]"
    ></q-input>
  </div>
<!--  留言-->
  <div class="q-pa-md">
    <div class="my-font input_tit">
      {{ $t('contact.message') }}
    </div>
    <textarea
      v-model="msg"
      type="textarea"
      autocapitalize="sentences"
      maxlength="200"
      @keyup="getisValue"
      style="width: 100%; height: 150px; resize: none;border: 1px #C2C2C2 solid; border-radius: 4px;margin-top: 12px"
    />
  </div>
<!--  提交按钮-->
  <q-btn
    :label="$t('index.submit')"
    :class="{'my-font my_subBtn ': isfull === false ,'my-font my_subBtnChange': isfull === true}"
    unelevated
    @click="submit_massage"
  />
<!--  页脚-->
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
.top_title {
  font-weight: 500;
  font-size: 17px;
  color: #333333;
}
.top_msg {
  font-size: 13px;
  font-weight: 400;
  color: #333333;
  line-height: 19px;
  margin-top: 20px;
}
.contact_way {
  font-size: 14px;
  font-weight: 400;
  color: #333333;
  margin-left: 16px;
}
.contact_address {
  font-size: 14px;
  font-weight: 400;
  color: #333333;
  margin-left: 32px;
  margin-top: -23px;
}
.input_tit {
  font-size: 13px;
  font-weight: 400;
  color: #333333;
}
.my_subBtn {
  width:92%;
  height: 36px;
  font-size: 13px;
  font-weight: 400;
  margin-left: 4%;
  color: #333333;
  background-color: #DBDBDB;
}
.my_subBtnChange {
  width:92%;
  height: 36px;
  font-size: 13px;
  font-weight: 400;
  margin-left: 4%;
  color: #ffffff;
  background-color: #1370EE;
}
.footer_bgc {
  margin-top: 20px;
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
import {defineComponent, ref} from "vue";
import {createMetaMixin, openURL } from "quasar";
import { post } from "boot/axios";

export default defineComponent({
  name: "contact_us",
  data() {
    return {
      meta: {},
      lang:this.$q.cookies.get('lang'),
      langlable: '',
      isfull: false,
      tel: '',
      email: '',
      name: '',
      msg: '',
      verify_email:("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$"),
      about_lable: this.$t('contact.about_type.zero'),
      about_modle: '',
      options: [
        this.$t('contact.about_type.one'),
        this.$t('contact.about_type.two'),
        this.$t('contact.about_type.three'),
        this.$t('contact.about_type.four'),
        this.$t('contact.about_type.five')
      ],
      ver_msg: {
        email:this.$t('contact.verify_msg.email')
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
          _this.$router.push('/phone')
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
    // 判断提交按钮变色
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
