<template>
  <q-scroll-area :thumb-style="thumbStyle"
                 :bar-style="barStyle"
                 :visible="visible"
                 ref="scrollAreaIndex"
                 @scroll="onScroll()"
                 :style="{ height: scroll_height, width: width }"
  >
    <q-layout view="hHh lpR fff" ref="Index">
      <!--      pc端的头部-->
      <q-header v-if="!ismobile" style="background-color: #1370EE">
        <div class="row" style="height:110px">
          <div class="col-2"></div>
          <div class="col-2 my-font-D" style="align-self: center;margin-left: 0.3%">
            <q-btn
              icon="img:statics/logo.svg"
              round
              dense
              unelevated
              flat
              :to="{ name: 'Homepage' }"
              @click="ScrollToTop() "
              size="xl"
            />
            <router-link
              @click="ScrollToTop()"
              :to="{ name: 'Homepage' }"
              style="color: white; text-decoration:none;font-size: 20px;font-weight: 700;margin-left: 1%">
              {{ $t('index.title') }}
            </router-link>
          </div>
          <div class="col-6 my-font" style="align-self: center;">
            <q-btn-group flat style="float: right">
              <q-btn-dropdown :label="$t('index.navbar.frontpage')" style="font-size: 16px;font-weight: 400">
                <q-list>
                  <q-item clickable v-close-popup @click="goTo('#')">
                    <q-item-section>
                      <q-item-label>GreaterWMS</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item clickable v-close-popup @click="goTo('https://django-vue-admin.com/')">
                    <q-item-section>
                      <q-item-label>DVadmin</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
              <q-btn
                @click="contact_us = true"
                flat
                :label=navbar.issued
                :to="{ name: 'release_notes' }"
                style="font-size: 16px;font-weight: 400"></q-btn>
              <q-btn flat :label=navbar.community to="/community/GreaterWMS"
                     style="font-size: 16px;font-weight: 400"></q-btn>
              <!--              <q-btn flat :label=navbar.market style="font-size: 16px;font-weight: 400"></q-btn>-->
              <q-btn-dropdown :label="$t('avatar3.download')" style="font-size: 16px;font-weight: 400">
                <q-list>
                  <q-item clickable v-close-popup @click="download_judge()">
                    <q-item-section>
                      <q-item-label>Desktop Version</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item clickable v-close-popup @click="download_android()">
                    <q-item-section>
                      <q-item-label>Android & Scanner</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
              <q-btn
                :label=navbar.contact
                :to="{ name: 'contact_us' }"
                style="font-size: 16px;font-weight: 400"
                @click="contact_us = true"
              />
              <!--          选择语言下拉框-->
              <q-btn-dropdown :label=langlable style="font-size: 16px;font-weight: 400">
                <q-list>
                  <q-item clickable v-close-popup @click="langChange('zh-hans')">
                    <q-item-section>
                      <q-item-label>{{ $t('index.lang.zh_zhans') }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item clickable v-close-popup @click="langChange('en-US')">
                    <q-item-section>
                      <q-item-label>{{ $t('index.lang.English') }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item clickable v-close-popup @click="langChange('ja')">
                    <q-item-section>
                      <q-item-label>{{ $t('index.lang.ja') }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item clickable v-close-popup @click="langChange('zh-hant')">
                    <q-item-section>
                      <q-item-label>{{ $t('index.lang.zh_zhant') }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
            </q-btn-group>
          </div>
          <div class="col-1"></div>
        </div>
        <q-separator class="center" style="color: #FFCE05;width: 65%;background-color:#d8d8d8;margin: 0 auto"/>
      </q-header>
      <!--      移动端的头部-->
      <q-header v-else style="background-color: #1370EE">
        <q-toolbar style="height: 60px">
          <q-btn flat @click="drawerLeft = !drawerLeft" round dense icon="menu"/>
          <q-toolbar-title class="text-center my-font-D phone_title">
            <q-btn
              padding="0"
              flat
              icon="img:statics/phone/logotop.svg"
            />
            GreaterWMS
          </q-toolbar-title>
          <q-btn flat @click="drawerRight = !drawerRight" round dense icon="translate"/>
        </q-toolbar>
        <q-separator class="center" style="color: #FFCE05;width: 100%;background-color:#d8d8d8;margin: 0 auto"/>
      </q-header>
      <!--      左侧侧边栏-->
      <q-drawer
        v-if="ismobile"
        v-model="drawerLeft"
        show-if-above
        :width="200"
        :breakpoint="700"
        elevated
        content-class="bg-primary text-white"
      >
        <div>
          <q-list separator>
            <!--            首页-->
            <q-item clickable :to="{ name : 'phone' }" class="row">
              <q-item-section class="col-1">
                <q-img
                  style="padding-bottom: 2px"
                  width="14px"
                  src="statics/phone/homepage_icon.svg"
                />
              </q-item-section>
              <q-item-section class="col-8 menu_left_top my-font text-left">
                {{ $t('index.navbar.frontpage') }}
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
            <q-item clickable :to="{ name : 'phone_contact_us' }" v-ripple class="row">
              <q-item-section class="col-1">
                <q-img
                  style="padding-bottom: 5px"
                  width="14px"
                  src="statics/phone/contact.svg"
                />
              </q-item-section>
              <q-item-section class="col-8 menu_left my-font text-left">
                {{ $t('index.navbar.contact') }}
              </q-item-section>
            </q-item>
<!--                        社区-->
                        <q-item clickable :to="{ name : 'community_mobile' }" v-ripple class="row">
                          <q-item-section class="col-1">
                            <q-img
                              width="14px"
                              src="statics/phone/issued.svg"
                            />
                          </q-item-section>
                          <q-item-section class="col-8 menu_left my-font text-left">
                            {{ $t("index.osc") }}
                          </q-item-section>
                        </q-item>
            <q-item/>
          </q-list>
        </div>
      </q-drawer>
      <!--      右侧语言侧边栏-->
      <q-drawer
        v-if="ismobile === true"
        side="right"
        v-model="drawerRight"
        show-if-above
        :width="200"
        :breakpoint="700"
        elevated
        content-class="bg-primary text-white"
      >
        <div>
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
            <!--                    中文繁体-->
            <q-item clickable @click="langChange('zh-hant')" v-ripple class="border_bottom menu_right">
              <q-item-section class="menu_left my-font text-left">
                中文繁體
              </q-item-section>
            </q-item>
            <!--                    日语-->
            <q-item clickable @click="langChange('ja')" v-ripple class="border_bottom menu_right">
              <q-item-section class="menu_left my-font text-left">
                日本語
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
      <q-page-container>
        <q-page style="margin-top: -1%">
          <router-view/>
          <!--            微信二维码-->
          <div v-if="!ismobile">
            <q-page-sticky v-if="langlable === '简体中文'" position="bottom-right" :offset="[25, 180]">
              <q-btn
                padding="md"
                icon="img:statics/wechat_buttom.svg"
                style="opacity: 0.18;background: #000000;"
                @click="wechat = !wechat;"
              >
              </q-btn>
            </q-page-sticky>
            <q-page-sticky v-if="wechat && lang === 'zh-hans'" position="bottom-right" :offset="[100, 90]">
              <q-btn
                style="width: 150px;height: 150px;padding: 5% 5%  "
              >
                <q-img src="statics/cus_ser.png">
                </q-img>
              </q-btn>
            </q-page-sticky>
            <!--          bilibili二维码-->
            <q-page-sticky v-if="langlable === '简体中文'" position="bottom-right" :offset="[25, 260]">
              <q-btn
                padding="md"
                icon="img:statics/bilibili_home.svg"
                style="opacity: 0.18;background: #000000;"
                @click="bilibili = !bilibili;"
              >
              </q-btn>
              <q-page-sticky v-show="bilibili && lang === 'zh-hans'" position="bottom-right" :offset="[80,20]">
                <q-btn
                  style="width: 150px;height: 150px;padding: 5% 5%  "
                >
                  <q-img src="statics/bilibili_qr.png">
                  </q-img>
                </q-btn>
              </q-page-sticky>
            </q-page-sticky>
            <!--            回到顶部-->
            <q-page-sticky v-if='pagelocation > 0.2' position="bottom-right" :offset="[25, 100]">
              <q-btn
                padding="md"
                icon="img:statics/return.svg"
                style="opacity: 0.18;background: #000000;"
                @click="ScrollToTop()"
              >
              </q-btn>
            </q-page-sticky>
          </div>
        </q-page>
      </q-page-container>
      <!--  页脚-->
      <q-footer v-if="!ismobile" class="my-font" :class="{'home_footer':!contact_us,'not_home_footer':contact_us}"
                style="padding-bottom: 15px">
        <div>
          <div class="row" style="padding-top: 70px">
            <div class="col-2"></div>
            <!--            logo加介绍-->
            <div class="col-2">
              <div style="margin-top: 3%">
                <q-img v-if="contact_us === false" src="statics/logo_under.svg" width="9%" :ratio="32/42"/>
                <q-img v-if="contact_us === true" src="statics/logo.svg" width="9%" :ratio="32/42"/>
                <span class="my-font-D"
                      :class="{'logo_title':!contact_us,'not_logo_title':contact_us}"
                >{{
                    $t('index.title')
                  }}</span>
              </div>
              <div class="my-font"
                   style="width: 300px;height: 62px;font-size: 14px;font-weight: 400;text-align: left;line-height: 21px;margin-top: 7%;">
                {{ $t('avatar3.tip_note2') }}
              </div>
            </div>
            <div class="col-2"></div>
            <div class="col-4 row">
              <div class="col-4">
                <div class="my-font" style="font-size: 20px;font-weight: 500;">
                  {{ $t('avatar3.about') }}
                </div>
                <br>
                <table class="my-font" style="font-size: 14px;font-weight: 400">
                  <tbody>
                  <tr>
                    <td height="30px">
                      <div :class="{'font_white':contact_us}" style="cursor: pointer" @click="goTo('https://gitee.com/Singosgu/GreaterWMS.git')">
                        {{ $t('index.code_warehouse') }}
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td height="30px">
                      <div
                        style="cursor: pointer"
                        @click="this.$router.push({ name: 'release_notes' })"
                        :class="{'font_white':contact_us}"
                      >
                        {{ $t('avatar3.issued') }}
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td height="30px">
                      <div style="cursor: pointer" @click="goTo('https://www.bilibili.com/video/BV15r4y1i7Ph?spm_id_from=333.999.0.0')">
<!--                        软件教程-->
                        {{ $t('avatar3.use_tutorial') }}
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td height="30px">
                      <div style="cursor: pointer" @click="goTo('https://www.bilibili.com/video/BV1vm4y1f7uo?spm_id_from=333.999.0.0')">
<!--                        扫描枪教程-->
                        {{ $t('avatar3.problem') }}
                      </div>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
              <div class="col-4">
                <div class="q-pa-md"
                     style="font-size: 20px;font-weight: 500;padding-bottom: 0;padding-top: 0">
                  {{ $t('avatar3.download') }}
                </div>
                <br>
                <table style="font-size: 14px;font-weight: 400">
                  <tbody>
                  <!--                  <tr>-->
                  <!--                    <td height="30px">-->
                  <!--&lt;!&ndash;                      <q-btn&ndash;&gt;-->
                  <!--&lt;!&ndash;                        unelevated&ndash;&gt;-->
                  <!--&lt;!&ndash;                        @click="goTo('https://production.56yhz.com/')"&ndash;&gt;-->
                  <!--&lt;!&ndash;                      >&ndash;&gt;-->
                  <!--&lt;!&ndash;                        Website&ndash;&gt;-->
                  <!--&lt;!&ndash;                      </q-btn>&ndash;&gt;-->
                  <!--                    </td>-->
                  <!--                  </tr>-->
                  <tr>
                    <td height="30px">
                      <q-btn unelevated @click="download_android()">
                        Android
                        <br>
                        &
                        <br>
                        Scanner
                      </q-btn>
                    </td>
                  </tr>
                  <tr>
                    <td height="30px">
                      <q-btn
                        unelevated
                        @click="download_judge()"
                      >
                        Desktop
                        <br>
                        Version
                      </q-btn>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
              <div class="col-4">
                <div style="font-size: 20px;font-weight: 500">
                  {{ $t('index.navbar.community') }}
                </div>
                <br>
                <table style="font-size: 14px;font-weight: 400">
                  <tbody>
                  <tr>
                    <td height="30px">
                      <div style="cursor: pointer" @click="this.$router.push('/community')">
                        {{ $t('avatar3.g_wms') }}
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td height="30px">
                      <div :class="{'font_white':contact_us}" style="cursor: pointer" @click="this.$router.push('/community/DVadmin')">
                        {{ $t('avatar3.dvadmin') }}
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td height="30px">
                      <div :class="{'font_white':contact_us}" style="cursor: pointer" v-if="langlable === '简体中文'" @click="goTo('http://www.quasarchs.com')">
                        Quasar Framework
                      </div>
                      <a :class="{'font_white':contact_us}" style="cursor: pointer" v-else-if="langlable !== '简体中文'" @click="goTo('https://quasar.dev/')">
                        Quasar Framework
                      </a>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-2"></div>
            <!--            下划线-->
            <q-separator class="center" inset
                         style="color: #FFCE05;width: 80%;background-color:#d8d8d8;margin: 2% auto"/>
            <br>
          </div>
          <!--                备案号-->
          <div class="row my-font" style="height:50px">
            <div class="col-2"></div>
            <div class="col-5" style="font-size: 14px;font-weight: 400">
              {{ $t('avatar3.record_number') }}
              <a href="https://beian.miit.gov.cn/#/Integrated/recordQuery" target="_blank">{{ $t('avatar3.icp') }}</a>
              {{ $t('avatar3.record_number2') }}
            </div>
            <div class="col-2"></div>
            <div class="col-2">
              <!--                              <a @mouseover="wechat = true" @mouseleave="wechat = false">-->
              <!--                                <q-img src="statics/wechat_buttom.svg" width="9%"></q-img>-->
              <!--                              </a>-->
              <a href="https://gitee.com/Singosgu/GreaterWMS.git" target="_blank">
                <q-img v-if="contact_us === false" src="statics/gitee.svg" width="9%" style="margin-left: 8%"></q-img>
                <q-img v-if="contact_us === true" src="statics/gitee_w.svg" width="9%" style="margin-left: 8%"></q-img>
              </a>
              <a href="https://github.com/Singosgu/GreaterWMS.git" target="_blank">
                <q-img v-if="contact_us === false" src="statics/github.svg" width="9%" style="margin-left: 15%"></q-img>
                <q-img v-if="contact_us === true" src="statics/github_w.svg" width="9%"
                       style="margin-left: 15%"></q-img>
              </a>

            </div>
            <div class="col-2"></div>
          </div>
        </div>
      </q-footer>
      <q-dialog v-model="advertise">
        <q-card class="shadow-0" style="width: 650px;cursor: pointer;background: rgba(0,0,0,0)" @click="goTo(advertiseUrl)">
          <img :title="advertiseTitle" src="statics/advertise/100.svg" alt="">
        </q-card>
        <q-card class="shadow-0" style="margin-top: -600px;cursor: pointer; background: rgba(0,0,0,0)" @click="advertise = false">
          <img src="statics/advertise/close.svg" alt="">
        </q-card>
      </q-dialog>
    </q-layout>
  </q-scroll-area>
</template>
<style lang="scss" scoped>
.home_footer {
  background-color: white;
  color: #333333;
}

.not_home_footer {
  background-color: #1370EE;
  color: white;
}

.font_white {
  color: white;
}

.logo_title {
  width: 118px;
  height: 22px;
  font-size: 20px;
  font-weight: 700;
  color: #000000;
  margin-left: 2%
}

.not_logo_title {
  width: 118px;
  height: 22px;
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin-left: 2%
}

.border_bottom {
  border-bottom: #D5D5D5 solid 1px;
}

.menu_left_top {
  font-size: 14px;
  font-weight: normal;
  color: #999999;
  text-align: left;
}

.menu_left {
  font-size: 14px;
  font-weight: normal;
  color: #333333;
  text-align: left;
}

.phone_title {
  font-size: 18px;
  font-weight: 700;
  color: white;
}

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
import {defineComponent, ref} from 'vue'
import {openURL, createMetaMixin} from 'quasar'
import {get, getauth, post} from "boot/axios";

export default defineComponent({
  name: 'Index',
  components: {},

  data() {
    return {
      contact_us: false,
      drawerLeft: false,
      drawerRight: false,
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
      navbar: {
        front_page: this.$t('index.navbar.frontpage'),
        community: this.$t('index.navbar.community'),
        market: this.$t('index.navbar.market'),
        demo: this.$t('index.navbar.demo'),
        contact: this.$t('index.navbar.contact'),
        issued: this.$t('avatar3.issued')
      },
      visible: false,
      width: this.$q.screen.width + '' + 'px',
      height: this.$q.screen.height + '' + 'px',
      scroll_height: this.$q.screen.height + '' + 'px',
      location: 1,
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
      code_warehouse: this.$t('index.code_warehouse'),
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
      isfull: false,
      isnull: true,
      issued_msg: [],
      ismobile: false,
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
    // 判断提交按钮变色
    getisValue() {
      var _this = this
      if (_this.about_modle && _this.name && _this.email) {
        _this.isfull = true
        _this.isnull = false
      } else {
        _this.isfull = false
        _this.isnull = true
      }
    },
    download_android() {
      var _this = this
      _this.goTo('/media/android/Greaterwms.apk')
    },
    // 验证系统并下载
    download_judge() {
      var _this = this
      if (_this.$q.platform.is.mac) {
        _this.goTo('/media/mac/GreaterWMS.dmg')
      } else if (_this.$q.platform.is.win) {
        _this.goTo('/media/windows/Greaterwms.exe')
      }
    },
    // 获取视频文件
    getvideo () {
      var _this = this
      getauth('/resp/api/v1/resp/').then(res => {
        console.log(res)
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    //获取广告链接
    getadvertiseUrl () {
      var _this = this
      get('resp/api/v1/banner').then(res => {
        console.log(res)
        _this.advertiseUrl = res[0].link
        _this.advertiseTitle = res[0].title
      })
    }
  },
  computed: {
    tabname: {
      get() {
        return this.$store.state.tabchange.tabname
      },
      set(val) {
        this.$refs.scrollArea.setScrollPosition(100)
        this.$store.commit('tabchange/tabNameChanged', val)
      }
    }
  },
  mounted() {
    var _this = this
    if (_this.$q.platform.is.mobile) {
      this.ismobile = true
      this.$router.push({name: 'phone'})
    } else {
      this.ismobile = false
      this.$router.push({name: 'Homepage'})
    }
    _this.getadvertiseUrl()
    if (_this.$q.cookies.has('area')) {
      if (_this.$q.cookies.get('area') !== 'China') {
        _this.advertise = false
      } else  {
        _this.advertise = true
      }
    }
  },
  created() {
    var _this = this
    setTimeout(function () {
        _this.wechat = false
      },
      3000);
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
    if (_this.lang === 'zh-hans') {
      _this.title = 'GreaterWMS - 完全开源的仓库管理系统'
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
      _this.title = 'GreaterWMS - Open Source Warehouse Management System'
      _this.meta = {
        description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
        keywords: {
          name: 'keywords',
          content: 'GreaterWMS - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms'
        },
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
  watch: {
    lang(lang) {
      var _this = this
      _this.$q.cookies.set('lang', lang)
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
        scrollAreaIndex.value.setScrollPosition('vertical', position.value, 50)
      }
    }
  }
})
</script>
