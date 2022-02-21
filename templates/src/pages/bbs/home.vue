<template>
  <q-layout view="hhh LpR fFf" class="bg-grey-1">
    <q-header class="bg-white head_shadow" reveal>
      <q-toolbar class="GPLAY__toolbar text-black row no-padding">
        <div class="col-2"></div>
        <!--          //logo-->
        <div class="col-4 my-font-D" style="align-self: center">
          <q-btn
            :icon="logo"
            round
            dense
            unelevated
            flat
            size="xl"
            @click="click_logo"
          />
          <span
            class="text-black my-font"
            style="
              color: white;
              text-decoration: none;
              font-size: 20px;
              font-weight: 500;
              margin-left: 1%;
            "
            >{{ titletype }}{{ $t("index.osc") }}
          </span>
        </div>
        <!--          //搜索框-->
        <div class="GPLAY__toolbar-input-container row no-wrap col-2">
          <!--                      <q-input dense outlined square placeholder="Search" class="bg-white col" />-->
          <!--                      <q-btn class='' color="primary" icon="search" unelevated />-->
        </div>
        <!--          //登陆注册-->
        <div
          class="q-pl-md q-gutter-sm row no-wrap items-center col-2"
          :class="{ login_top: !isLogin }"
        >
          <q-btn
            v-show="langlable !== '简体中文'"
            round
            flat
            icon="img:statics/github.png"
            @click="goTo('https://github.com/Singosgu/GreaterWMS')"
          />
          <q-btn
            v-show="langlable === '简体中文'"
            round
            flat
            icon="img:statics/gitee.ico"
            @click="goTo('https://gitee.com/Singosgu/GreaterWMS')"
          />
          <q-btn
            class="my-font"
            flat
            v-if="!isLogin && langlable === '简体中文'"
            color="white"
            style="
              background-color: #116fec;
              font-size: 16px;
              font-weight: 400;
              width: 45%;
              padding: 0;
            "
            @click="login = true"
          >
            登录&nbsp&nbsp|&nbsp&nbsp注册
          </q-btn>
          <q-btn
            class="my-font"
            flat
            v-if="!isLogin && langlable !== '简体中文'"
            color="white"
            style="background-color: #116fec; font-size: 14px; font-weight: 400"
            @click="login = true"
          >
            Login&nbsp&nbsp|&nbsp&nbspRegister
          </q-btn>
          <div v-if="isLogin">
            <q-avatar style="cursor: pointer" @click="toHomepage()">
              <img :src="avatar_img" style="border-radius: 25px" />
            </q-avatar>
          </div>
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
        <div class="col-2"></div>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <q-page>
        <q-scroll-area
          :thumb-style="thumbStyle"
          :bar-style="barStyle"
          :visible="visible"
          :delay="1500"
          ref="scrollAreaHome"
          @scroll="onScroll()"
          :style="{ height: scroll_height, width: scroll_width }"
        >
          <div class="q-pa-md">
            <div class="row">
              <div class="col-2"></div>
              <!--                左侧导航栏-->
              <div v-show="isIndexMenu" class="col-2 row" style="height: 300px">
                <q-card flat class="col-11" :offset="[0, 20]">
                  <q-list bordered padding class="my-font col-12">
                    <!--                        回到首页-->
                    <q-item to="/Homepage" clickable v-ripple class="col-1 row">
                      <div></div>
                      <q-item-section class="col-1"></q-item-section>

                      <q-item-section>
                        <span
                          style="
                            font-size: 18px;
                            font-weight: 400;
                            color: #333333;
                          "
                          >{{ $t("community.backfontpage") }}</span
                        >
                      </q-item-section>
                    </q-item>

                    <q-separator spaced />
                    <!--GreaterWMS社区-->
                    <q-item
                      clickable
                      :active="this.link === 'gwms'"
                      @click="click_gwms()"
                      active-class="my-menu-link"
                      :to="{ name: 'GreaterWMS' }"
                      class="col-1 row"
                    >
                      <q-item-section class="col-1"></q-item-section>
                      <q-item-section>
                        <span style="font-size: 16px; font-weight: 400">
                          GreaterWMS{{ $t("community.gwms_com") }}
                        </span>
                      </q-item-section>
                    </q-item>
                    <!--                    DVadmin社区-->
                    <q-item
                      v-ripple
                      clickable
                      :active="this.link === 'dv'"
                      @click="click_DVadmin()"
                      active-class="my-menu-link"
                      class="col-1 row"
                      :to="{ name: 'DVadmin' }"
                    >
                      <q-item-section class="col-1"></q-item-section>
                      <q-item-section>
                        <span style="font-size: 16px; font-weight: 400">
                          DVAdmin{{ $t("community.gwms_com") }}
                        </span>
                      </q-item-section>
                    </q-item>
                    <q-separator spaced />
                    <!-- 商城 -->
                    <q-item class="col-1 row">
                      <q-item-section class="col-1"></q-item-section>
                      <q-item-section>
                        <span
                          style="
                            font-size: 16px;
                            font-weight: 500;
                            color: #777888;
                          "
                          >{{ $t("index.navbar.market") }}</span
                        >
                      </q-item-section>
                    </q-item>

                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'plugingwms'"
                      @click="click_gwms_market()"
                      active-class="my-menu-link"
                      to="/market/plugins/GreaterWMS"
                    >
                      <q-item-section avatar></q-item-section>
                      <q-item-section>
                        <span style="font-size: 16px; font-weight: 400">{{
                          $t("community.greaterwms")
                        }}</span>
                      </q-item-section>
                    </q-item>

                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'plugindv'"
                      @click="click_DVadmin_market()"
                      active-class="my-menu-link"
                      to="/market/plugins/DVAdmin"
                    >
                      <q-item-section avatar></q-item-section>
                      <q-item-section>
                        <span style="font-size: 16px; font-weight: 400">{{
                          $t("community.dvadmin")
                        }}</span>
                      </q-item-section>
                    </q-item>

                    <!--                    <q-item-->
                    <!--                      clickable-->
                    <!--                      v-ripple-->
                    <!--                      :active="link === 'equipment'"-->
                    <!--                      @click="link = 'equipment'"-->
                    <!--                      active-class="my-menu-link"-->
                    <!--                      class="col-1"-->
                    <!--                    >-->
                    <!--                      <q-item-section avatar></q-item-section>-->
                    <!--                      <q-item-section>-->
                    <!--                        <span style="font-size: 14px; font-weight: 400">{{-->
                    <!--                          $t("community.equipment")-->
                    <!--                        }}</span>-->
                    <!--                      </q-item-section>-->
                    <!--                    </q-item>-->
                  </q-list>
                </q-card>
              </div>
              <div v-show="!isIndexMenu" class="col-2 row">
                <q-card
                  class="col-11 column"
                  :offset="[0, 20]"
                  style="height: 620px"
                >
                  <q-list bordered padding class="my-font col-12 column">
                    <!--                       返回社区-->
                    <q-item
                      clickable
                      v-ripple
                      @click="
                        this.$router.push({ name: 'GreaterWMS' });
                        this.$store.dispatch('bbsChange/isIndexMenu', true);
                        this.$store.dispatch('bbsChange/link', 'GreaterWMS');
                        refresh_community();
                      "
                      class="col-1 row"
                    >
                      <div></div>
                      <q-item-section class="col-1"></q-item-section>

                      <q-item-section>
                        <span style="font-size: 18px; font-weight: 400">{{
                          $t("community.backcommunity")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <q-separator spaced />
                    <!--个人中心-->
                    <q-item class="col-1 row">
                      <q-item-section class="col-1"></q-item-section>

                      <q-item-section>
                        <span
                          style="
                            font-size: 16px;
                            font-weight: 500;
                            color: #777888;
                          "
                          >{{ $t("community.personal_center") }}</span
                        >
                      </q-item-section>
                    </q-item>
                    <!--我的主页-->
                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'personalHomepage'"
                      @click="
                        this.$store.dispatch(
                          'bbsChange/link',
                          'personalHomepage'
                        );
                        this.$router.push('/community/personalHomepage');
                        this.$store.dispatch('bbsChange/isIndexMenu', false);
                      "
                      active-class="my-menu-link"
                      class="col-1"
                    >
                      <q-item-section avatar></q-item-section>

                      <q-item-section>
                        <span style="font-size: 14px; font-weight: 400">{{
                          $t("community.myhomepage")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <!--                    我的订单-->
                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'order'"
                      @click="
                        this.$store.dispatch('bbsChange/link', 'order');
                        this.$router.push('/community/myOrders');
                        this.$store.dispatch('bbsChange/isIndexMenu', false);
                      "
                      active-class="my-menu-link"
                      class="col-1"
                    >
                      <q-item-section avatar></q-item-section>

                      <q-item-section>
                        <span style="font-size: 14px; font-weight: 400">{{
                          $t("community.myorder.index")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <!--                    我的插件-->
                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'plugin'"
                      @click="
                        this.$store.dispatch('bbsChange/link', 'plugin');
                        this.$router.push('/community/myReleasedPlugins');
                        this.$store.dispatch('bbsChange/isIndexMenu', false);
                      "
                      active-class="my-menu-link"
                      class="col-1"
                    >
                      <q-item-section avatar></q-item-section>

                      <q-item-section>
                        <span style="font-size: 14px; font-weight: 400">{{
                          $t("community.myplugin.index")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <!--                    我的钱包-->
                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'wallet'"
                      @click="
                        this.$store.dispatch('bbsChange/link', 'wallet');
                        this.$router.push('/community/myWallet');
                        this.$store.dispatch('bbsChange/isIndexMenu', false);
                      "
                      active-class="my-menu-link"
                      class="col-1"
                    >
                      <q-item-section avatar></q-item-section>

                      <q-item-section>
                        <span style="font-size: 14px; font-weight: 400">{{
                          $t("community.mywallet.index")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <q-separator spaced />
                    <!--设置-->
                    <q-item class="col-1 row">
                      <q-item-section class="col-1"></q-item-section>

                      <q-item-section>
                        <span
                          style="
                            font-size: 16px;
                            font-weight: 500;
                            color: #777888;
                          "
                          >{{ $t("community.settings") }}</span
                        >
                      </q-item-section>
                    </q-item>
                    <!--                    实名认证-->
                    <q-item
                      v-if="this.$q.cookies.get('area') === 'China'"
                      clickable
                      v-ripple
                      :active="this.link === 'verified'"
                      @click="
                        this.$store.dispatch('bbsChange/link', 'verified');
                        this.$router.push('/community/authentication');
                        this.$store.dispatch('bbsChange/isIndexMenu', false);
                        // getper_centerinfo();
                      "
                      active-class="my-menu-link"
                      class="col-1"
                    >
                      <q-item-section avatar></q-item-section>

                      <q-item-section>
                        <span style="font-size: 14px; font-weight: 400">{{
                          $t("community.verified")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <!--                    我的账户-->
                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'my_account'"
                      @click="
                        this.$store.dispatch('bbsChange/link', 'my_account');
                        this.$router.push('/community/myAccount');
                        this.$store.dispatch('bbsChange/isIndexMenu', false);
                      "
                      active-class="my-menu-link"
                      class="col-1"
                    >
                      <q-item-section avatar></q-item-section>

                      <q-item-section>
                        <span style="font-size: 14px; font-weight: 400">{{
                          $t("community.my_account")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <!--账号与密码-->
                    <q-item
                      clickable
                      v-ripple
                      :active="this.link === 'changePsd'"
                      @click="
                        this.$store.dispatch('bbsChange/link', 'changePsd');
                        this.$router.push('/community/changePsd');
                        this.$store.dispatch('bbsChange/isIndexMenu', false);
                        // getper_centerinfo();
                      "
                      active-class="my-menu-link"
                      class="col-1"
                    >
                      <q-item-section avatar></q-item-section>

                      <q-item-section>
                        <span style="font-size: 14px; font-weight: 400">{{
                          $t("community.act_psd")
                        }}</span>
                      </q-item-section>
                    </q-item>
                    <q-separator spaced />
                    <!--                    退出登录-->
                    <q-item clickable class="row" @click="logout_sub()">
                      <q-item-section class="col-1"></q-item-section>

                      <q-item-section class="col-9">
                        <span
                          style="
                            font-size: 16px;
                            font-weight: 500;
                            color: #777888;
                          "
                          >{{ $t("community.logout") }}</span
                        >
                      </q-item-section>
                      <!--                      退出登录图标-->
                      <q-item-section class="col">
                        <q-img width="20px" src="statics/logout.svg" />
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
              <div class="col-6 items-start">
                <router-view />
              </div>
              <div class="col-2"></div>
            </div>
          </div>
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

    <!--      登录注册dialog-->
    <q-dialog v-model="login" full-width>
      <q-card class="row" style="width: 800px !important; height: 540px">
        <div class="col-4">
          <q-img src="statics/login.png" height="100%"></q-img>
        </div>
        <div class="col-8 column">
          <!--            关闭按钮-->
          <div class="col-1">
            <q-btn
              class="q-pa-md"
              dense
              flat
              icon="close"
              v-close-popup
              style="float: right"
              @click="close_dialog"
            />
          </div>
          <!--            登录和注册切换-->
          <div class="col-11 column">
            <q-tabs
              class="col-2 row my-font"
              v-model="tab"
              narrow-indicator
              active-bg-colo="white"
              indicator-color="blue"
              active-color="black"
            >
              <div class="col-1"></div>
              <q-tab
                class="my-font col-2"
                name="login"
                style="font-size: 22px; font-weight: 500; color: #333333"
                >{{ $t("index.login") }}
              </q-tab>
              <q-tab
                class="my-font col-2"
                name="register"
                style="
                  font-size: 22px !important;
                  font-weight: 500;
                  color: #666666;
                "
                >{{ $t("index.register") }}
              </q-tab>
              <div class="col-7"></div>
            </q-tabs>

            <!--              <div class="col-1"></div>-->

            <q-tab-panels class="col-10 column" v-model="tab" animated>
              <!--登录-->
              <q-tab-panel class="col-12 column" name="login">
                <!--                  邮箱-->
                <div class="col-2 row">
                  <div class="col-1"></div>
                  <div class="col-10">
                    <q-input
                      autofocus
                      class="my-font"
                      v-model="getEmail"
                      :label="email"
                      @keyup="getloginValue"
                      :rules="[
                        (val) =>
                          (val &&
                            getEmail.indexOf('@') !== -1 &&
                            getEmail.indexOf('.') !== -1) ||
                          ver_email_msg,
                      ]"
                    ></q-input>
                  </div>
                </div>
                <div class="col-1"></div>
                <!--                  密码-->
                <div class="col-2 row">
                  <div class="col-1"></div>
                  <div class="q-gutter-md col-10">
                    <q-input
                      class="my-font"
                      type="password"
                      v-model="getPassword"
                      :label="password"
                      @keyup="getloginValue"
                    ></q-input>
                  </div>
                </div>
                <div class="col-2"></div>
                <!--                  登录按钮-->
                <div class="col-2 row">
                  <div class="col-1"></div>
                  <q-btn
                    v-if="!isloginOK"
                    class="col-10 my-font"
                    :label="login_"
                    unelevated
                    text-color="#999999"
                    style="
                      background: #e6e6e6;
                      font-size: 20px;
                      font-weight: 400;
                      color: #999999;
                      letter-spacing: 10px;
                    "
                  ></q-btn>
                  <q-btn
                    v-if="isloginOK"
                    class="col-10 my-font"
                    :label="login_"
                    unelevated
                    text-color="#999999"
                    style="
                      background: #116fec;
                      color: white;
                      font-size: 20px;
                      font-weight: 400;
                      letter-spacing: 10px;
                    "
                    @click="login_sub()"
                  ></q-btn>
                </div>
                <div class="col-1"></div>
                <!--                  忘记密码-->
                <div class="col-1 row">
                  <div class="col-1"></div>
                  <div class="col-10">
                    <q-btn
                      unelevated
                      class="my-font"
                      style="
                        color: #999999;
                        font-size: 12px;
                        font-weight: 400;
                        float: right;
                      "
                      @click="
                        forgetpsd = true;
                        login = false;
                      "
                    >
                      {{ $t("index.forget") }}
                    </q-btn>
                  </div>
                </div>
                <div
                  v-if="lang === 'zh-hans'"
                  class="col-1 my-font text-center"
                  style="font-size: 12px; font-weight: 400; color: #999999"
                >
                  登录/注册即代表同意
                  <a class="dia_a" @click="$router.push('/community/tos')"
                    >《服务条款》</a
                  >
                  &nbsp
                  <a class="dia_a" @click="$router.push('/community/pa')"
                    >《隐私协议》</a
                  >
                </div>
              </q-tab-panel>
              <!--注册-->
              <q-tab-panel class="col-12 column" name="register">
                <div class="col-8 column">
                  <!--                    输入邮箱-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        autofocus
                        class="my-fon"
                        type="text"
                        v-model="reg.email"
                        :label="email"
                        style="font-size: 14px; font-weight: 400"
                        @keyup="getinputValue"
                        :rules="[
                          (val) =>
                            (val &&
                              reg.email.split('@').length - 1 === 1 &&
                              reg.email.split('.').length - 1 === 1) ||
                            ver_email_msg,
                        ]"
                      ></q-input>
                    </div>
                  </div>
                  <!--输入验证码-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        class="my-font"
                        bottom-slots
                        v-model="reg.e_verify"
                        :label="everify"
                        style="font-size: 14px; font-weight: 400"
                        @keyup="getinputValue"
                      >
                        <template v-slot:append>
                          <a
                            v-show="getvf === true"
                            class="my-font"
                            style="
                              color: #5b86e5;
                              font-size: 14px;
                              font-weight: 400;
                              cursor: pointer;
                            "
                            @click="isreged(reg.email)"
                            >{{ $t("index.getverify") }}</a
                          >
                          <span
                            v-show="getvf === false"
                            class="my-font"
                            style="
                              color: #5b86e5;
                              font-size: 14px;
                              font-weight: 400;
                            "
                            >{{ $t("index.efficient") }}</span
                          >
                        </template>
                      </q-input>
                    </div>
                  </div>
                  <!--输入密码-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        class="my-font"
                        type="password"
                        v-model="reg.psd"
                        :label="password"
                        style="font-size: 14px; font-weight: 400"
                        @keyup="getinputValue"
                        :rules="[
                          (val) => (val && val.length >= 8) || less_eight,
                        ]"
                      ></q-input>
                    </div>
                  </div>
                  <!--确认密码-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        class="my-font"
                        type="password"
                        v-model="reg.conpsd"
                        :label="conpsd"
                        style="font-size: 14px; font-weight: 400"
                        :rules="[(val) => val === reg.psd || inconsistent]"
                        @keyup="getinputValue"
                      ></q-input>
                    </div>
                  </div>
                </div>
                <div class="col-1"></div>
                <!--注册按钮                  -->
                <div class="col-2 row">
                  <div class="col-1"></div>
                  <q-btn
                    v-if="!isregOK"
                    class="col-10 my-font"
                    :label="register_"
                    unelevated
                    text-color="#999999"
                    style="
                      background: #e6e6e6;
                      height: 80%;
                      font-size: 20px;
                      color: #999999;
                      font-weight: 400;
                      letter-spacing: 10px;
                    "
                  ></q-btn>
                  <q-btn
                    v-if="isregOK"
                    class="col-10 my-font"
                    :label="register_"
                    unelevated
                    text-color="white"
                    style="
                      background: #116fec;
                      height: 80%;
                      font-size: 20px;
                      font-weight: 400;
                      color: white;
                      letter-spacing: 10px;
                    "
                    @click="register_sub()"
                  ></q-btn>
                </div>
                <div
                  v-if="lang === 'zh-hans'"
                  class="col-1 my-font text-center"
                  style="font-size: 12px; font-weight: 400; color: #999999"
                >
                  登录/注册即代表同意
                  <a class="dia_a" @click="$router.push('/community/tos')"
                    >《服务条款》</a
                  >
                  &nbsp
                  <a class="dia_a" @click="$router.push('/community/pa')"
                    >《隐私协议》</a
                  >
                </div>
              </q-tab-panel>
            </q-tab-panels>
          </div>
        </div>
      </q-card>
    </q-dialog>
    <!--      忘记密码dialog-->
    <q-dialog v-model="forgetpsd" full-width>
      <q-card class="row" style="width: 800px !important; height: 500px">
        <div class="col-4">
          <q-img src="statics/login.png" height="100%"></q-img>
        </div>
        <div class="col-8 column">
          <!--            关闭按钮-->
          <div class="col-1">
            <q-btn
              class="q-pa-md"
              dense
              flat
              icon="close"
              v-close-popup
              style="float: right"
              @click="close_dialog"
            />
          </div>
          <div class="col-11 column">
            <q-tabs
              class="col-2 row my-font"
              v-model="forget_tab"
              narrow-indicator
              active-bg-colo="white"
              indicator-color="blue"
              active-color="black"
            >
              <div class="col-1"></div>
              <div class="col-3">
                <q-btn
                  icon="img:statics/back.svg"
                  unelevated
                  @click="
                    login = true;
                    forgetpsd = false;
                  "
                ></q-btn>
              </div>
              <q-tab
                class="my-font col-3"
                name="forget_password"
                style="font-size: 18px; font-weight: 500; color: #666666"
                >{{ $t("community.forget_password") }}
              </q-tab>
              <div class="col-5"></div>
            </q-tabs>

            <!--              <div class="col-1"></div>-->

            <q-tab-panels class="col-10 column" v-model="forget_tab" animated>
              <!--忘记密码-->
              <q-tab-panel class="col-12 column" name="forget_password">
                <div class="col-8 column">
                  <!--                    输入邮箱-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        autofocus
                        class="my-fon"
                        type="text"
                        v-model="fgpsd.email"
                        :label="email"
                        style="font-size: 14px; font-weight: 400"
                        @keyup="getforgetValue"
                        :rules="[
                          (val) =>
                            (val &&
                              fgpsd.email.indexOf('@') !== -1 &&
                              fgpsd.email.indexOf('.') !== -1) ||
                            ver_email_msg,
                        ]"
                      ></q-input>
                    </div>
                  </div>
                  <!--输入验证码-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        class="my-font"
                        bottom-slots
                        v-model="fgpsd.verify"
                        :label="everify"
                        style="font-size: 14px; font-weight: 400"
                        @keyup="getforgetValue"
                      >
                        <!--获取验证码-->
                        <template v-slot:append>
                          <a
                            v-show="getvf3 === true"
                            class="my-font"
                            href="#"
                            style="
                              color: #5b86e5;
                              font-size: 14px;
                              font-weight: 400;
                            "
                            @click="isreged_forgetpsd(fgpsd.email)"
                            >{{ $t("index.getverify") }}</a
                          >
                          <span
                            v-show="getvf3 === false"
                            class="my-font"
                            href="#"
                            style="
                              color: #5b86e5;
                              font-size: 14px;
                              font-weight: 400;
                            "
                            >{{ $t("index.efficient") }}</span
                          >
                        </template>
                      </q-input>
                    </div>
                  </div>
                  <!--输入密码-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        class="my-font"
                        type="password"
                        v-model="fgpsd.password"
                        :label="password"
                        style="font-size: 14px; font-weight: 400"
                        @keyup="getforgetValue"
                      ></q-input>
                    </div>
                  </div>
                  <!--确认密码-->
                  <div class="col-3 row">
                    <div class="col-1"></div>
                    <div class="col-10 q-gutter-md">
                      <q-input
                        class="my-font"
                        type="password"
                        v-model="fgpsd.ver_psd"
                        :label="conpsd"
                        style="font-size: 14px; font-weight: 400"
                        @keyup="getforgetValue"
                        :rules="[
                          (val) =>
                            (val && fgpsd.password === fgpsd.ver_psd) ||
                            inconsistent,
                        ]"
                      ></q-input>
                    </div>
                  </div>
                </div>
                <div class="col-1"></div>
                <!--提交按钮                  -->
                <div class="col-2 row">
                  <div class="col-1"></div>
                  <q-btn
                    class="col-10 my-font"
                    :label="submit"
                    unelevated
                    text-color="#ffffff"
                    style="
                      background: #116fec;
                      height: 80%;
                      font-size: 20px;
                      font-weight: 400;
                      letter-spacing: 10px;
                      color: white;
                    "
                    @click="forgetPassword"
                  ></q-btn>
                </div>
                <div class="col-1"></div>
              </q-tab-panel>
            </q-tab-panels>
          </div>
        </div>
      </q-card>
    </q-dialog>
    <!--      发布弹窗dialog-->
    <q-dialog v-model="releasedia" full-width>
      <q-card class="q-pb-md" style="width: 580px !important">
        <!--          发布和关闭按钮-->
        <div
          class="my-font rel_dialog q-pa-md row"
          style="border-bottom: 1px #dcdcdc solid"
        >
          <div class="col-11">{{ $t("community.push_article") }}</div>
          <q-btn
            class="col-1"
            unelevated
            icon="close"
            @click="
              this.$store.dispatch('bbsChange/releasediaChange', false);
              qeditor = '';
              rel_problem = '';
            "
            style="width: 16px; height: 16px; margin-left: 12px"
          />
        </div>
        <!--          标题-->
        <div class="q-pa-md" style="width: 100%; height: 100px">
          <div class="my-font q-mb-sm">{{ $t("community.tip") }}</div>
          <q-input
            counter
            outlined
            dense
            v-model="rel_problem"
            @keyup="getpushValue"
            maxlength="200"
          />
        </div>
        <!--          内容-->
        <div class="q-pa-md" style="width: 100%">
          <div class="rel_problem q-mb-sm">内容</div>
          <div>
            <markdown-aditor
              @getMarkdownHtml="getMarkdownHtml('qeditor', $event)"
              @getMarkdownText="getMarkdownText"
              :needUploadImg="true"
              :idIndex="1"
              type="article"
            ></markdown-aditor>
          </div>
        </div>
        <!--          发布帖子-->
        <div class="q-pa-md" style="width: 100%">
          <q-btn
            v-show="!ispushOK"
            unelevated
            class="push_deNotebtn"
            style="float: right; width: 110px; height: 40px"
          >
            <span class="my-font push_note">{{
              $t("community.push_note")
            }}</span>
          </q-btn>
          <q-btn
            v-show="ispushOK"
            unelevated
            class="push_notebtn"
            style="float: right; width: 110px; height: 40px"
            @click="sendArticle"
          >
            <span class="my-font push_note">{{
              $t("community.push_note")
            }}</span>
          </q-btn>
          <q-btn-dropdown
            unelevated
            style="float: right; margin-right: 20px"
            color="primary"
            :label="community_type"
          >
            <q-list>
              <q-item clickable v-close-popup @click="chose_gwms_type()">
                <q-item-section>
                  <q-item-label
                    >GreaterWMS{{ $t("index.navbar.community") }}</q-item-label
                  >
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup @click="chose_dv_type()">
                <q-item-section>
                  <q-item-label
                    >DVadmin{{ $t("index.navbar.community") }}</q-item-label
                  >
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </q-card>
    </q-dialog>
  </q-layout>
</template>
<script>
import { defineComponent, ref } from "vue";
import { openURL, createMetaMixin, date, throttle } from "quasar";
import { get, getauth, post, postauth } from "boot/axios";
import jwtDecode from "jwt-decode";
import MarkdownAditor from "./home_components/market/components/MarkdownAditor.vue";

export default defineComponent({
  components: { MarkdownAditor },
  name: "Home",
  data() {
    return {
      markdown_text: "",
      check_type: false,
      community_type: this.$t("community.community_chose"),
      community_types: {
        gwm: "GreaterWMS",
        dv: "DVadmin",
      },
      last_url: "",
      title: "",
      qeditor: "",
      forgetpsd: false,
      // link: "GreaterWMS",
      aaa: true,
      meta: {},
      lang: this.$i18n.locale,
      langlable: "",
      login: false,
      register: false,
      chose: "login_",
      ver_email_msg: this.$t("contact.verify_msg.email"),
      login_: this.$t("index.login"),
      register_: this.$t("index.register"),
      email: this.$t("community.email"),
      password: this.$t("community.password"),
      getEmail: "",
      getPassword: "",
      everify: this.$t("community.everify"),
      conpsd: this.$t("community.conpsd"),
      tab: "login",
      tab2: "register",
      isregOK: false,
      isloginOK: false,
      isfgOK: false,
      istextimg: false,
      istext: false,
      ispushOK: false,
      getvf: true,
      getvf2: true,
      getvf3: true,
      forget_tab: "forget_password",
      success_msg: this.$t("index.success"),
      reg_suc: this.$t("index.reg_suc"),
      navbar: {
        front_page: this.$t("index.navbar.frontpage"),
        community: this.$t("index.navbar.community"),
        market: this.$t("index.navbar.market"),
        demo: this.$t("index.navbar.demo"),
        contact: this.$t("index.navbar.contact"),
      },
      visible: false,
      scroll_width: this.$q.screen.width + "" + "px",
      scroll_height: this.$q.screen.height - 50 + "" + "px",
      thumbStyle: {
        right: "4px",
        borderRadius: "5px",
        backgroundColor: "#027be3",
        width: "8px",
        opacity: 0.75,
      },
      barStyle: {
        right: "2px",
        borderRadius: "9px",
        backgroundColor: "#027be3",
        width: "12px",
        opacity: 0.2,
      },
      rel_problem: "",
      reg: {
        email: "",
        e_verify: "",
        psd: "",
        conpsd: "",
      },
      fgpsd: {
        email: "",
        verify: "",
        password: "",
        ver_psd: "",
      },
      submit: this.$t("index.submit"),
      login_suc: this.$t("index.login_suc"),
      login_err: this.$t("index.login_err"),
      avatar_img: "",
      first_id: "",
      send_suc: this.$t("community.send_suc"),
      sendinfo: {
        tit: "",
        cover: "",
        massage: "",
        author: "",
        time: "",
      },
      personal_center: {
        icon: "",
        nick: "",
        intro: "",
        email: "",
        password: "",
        verify_code: "",
        newPassword: "",
        verify_psd: "",
      },
      inconsistent: this.$t("community.inconsistent"),
      less_eight: this.$t("community.less_eight"),
      regable: false,
      userinfoStr: "",
      homeurl: "Homepage",
      homename: "GreaterWMS",
    };
  },
  computed: {
    isLogin() {
      return this.$store.state.bbsChange.isLogin;
    },
    releasedia() {
      return this.$store.state.bbsChange.releasedia;
    },
    del_article() {
      return this.$store.state.bbsChange.del_article;
    },
    isIndexMenu() {
      return this.$store.state.bbsChange.isIndexMenu;
    },
    to_login() {
      return this.$store.state.bbsChange.to_login;
    },
    pagelocation() {
      return this.$store.state.pagelocation.pagelocation;
    },
    link() {
      return this.$store.state.bbsChange.link;
    },
    logo() {
      return this.$store.state.bbsChange.logo;
    },
    titletype() {
      return this.$store.state.bbsChange.titletype;
    },
  },
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.title,
        meta: this.meta,
      };
    }),
  ],
  methods: {
    // 刷新社区页面
    refresh_community() {
      location.replace("#/community");
    },
    // 打开链接
    goTo(e) {
      openURL(e);
    },
    // 更换语言
    langChange(e) {
      var _this = this;
      _this.lang = e;
      window.setTimeout(() => {
        location.reload();
      }, 1);
    },
    // 查看位置
    onScroll() {
      var _this = this;
      _this.$store.dispatch(
        "pagelocation/pageLocationChange",
        _this.$refs.scrollAreaHome.getScrollPercentage().top
      );
    },
    // 关闭dialog
    close_dialog() {
      var _this = this;
      _this.login = false;
      _this.register = false;
      _this.forgetpsd = false;
      _this.getEmail = "";
      _this.getPassword = "";
      _this.reg.email = "";
      _this.reg.e_verify = "";
      _this.reg.psd = "";
      _this.reg.conpsd = "";
      _this.fgpsd.email = "";
      _this.fgpsd.verify = "";
      _this.fgpsd.password = "";
      _this.fgpsd.ver_psd = "";
      _this.getEmail = "";
      _this.getPassword = "";
      _this.reg.email = "";
      _this.reg.e_verify = "";
      _this.reg.psd = "";
      _this.reg.conpsd = "";
      _this.fgpsd.email = "";
      _this.fgpsd.verify = "";
      _this.fgpsd.password = "";
      _this.fgpsd.ver_psd = "";
      _this.$router.push("/community");
    },
    // 登录
    login_sub() {
      var _this = this;
      var msg = {};
      msg.username = _this.getEmail;
      msg.password = _this.getPassword;
      post("token/", msg)
        .then((res) => {
          console.log(res);
          if (res.access) {
            _this.$q.cookies.set("token", res.access);
            _this.$q.cookies.set("token_ref", res.refresh);
            _this.getuserinfo();
            _this.$store.dispatch("bbsChange/loginChange", true);
            _this.getEmail = "";
            _this.getPassword = "";
            _this.$q.notify({
              message: _this.login_suc,
              icon: "check",
              color: "green",
            });
            _this.login = false;
            _this.$router.push("/community/GreaterWMS");
            location.reload();
          } else {
            _this.$q.notify({
              message: _this.$t("community.password_err"),
              icon: "close",
              color: "negative",
            });
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: _this.$t("community.password_err"),
            icon: "close",
            color: "negative",
          });
        });
    },
    // 获取用户信息
    getuserinfo() {
      var _this = this;
      _this.userinfoStr = jwtDecode(_this.$q.cookies.get("token"));
      let timeStamp = Date.now();
      let formattedString = date.formatDate(timeStamp, "X");
      if (_this.userinfoStr.exp >= parseInt(formattedString)) {
        let user_info = {
          id: _this.userinfoStr.user_id,
          icon: window.g.BaseUrl + _this.userinfoStr.icon,
          nickname: _this.userinfoStr.nickname,
          intro: _this.userinfoStr.intro,
          email: _this.userinfoStr.email,
        };
        _this.$store.dispatch("bbsChange/userInfoChange", user_info);
        _this.avatar_img = window.g.BaseUrl + _this.userinfoStr.icon;
      } else {
        _this.$store.dispatch("bbsChange/loginChange", false);
        let user_info = {
          id: "",
          icon: "",
          nickname: "",
          intro: "",
          email: "",
        };
        _this.$store.dispatch("bbsChange/userInfoChange", user_info);
        _this.avatar_img = "";
      }
    },
    //判断邮箱是否注册过
    isreged(e) {
      var _this = this;
      get("/user/api/v1/get_email/?email=" + e)
        .then((res) => {
          if (res.code !== 200) {
            _this.$q.notify({
              message: _this.$t("community.emailable"),
              icon: "close",
              color: "negative",
            });
          } else if (res.code === 200) {
            _this.getverify();
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    // 注册
    register_sub() {
      var _this = this;
      var msg = {};
      msg["email"] = _this.reg.email;
      msg["code"] = _this.reg.e_verify;
      msg["password"] = _this.reg.psd;
      msg["re_password"] = _this.reg.conpsd;
      post("user/api/v1/reg/", msg)
        .then((res) => {
          if (res.detail) {
          } else {
            _this.$q.notify({
              message: _this.reg_suc,
              icon: "check",
              color: "green",
            });
            var suc_reg_msg = {};
            suc_reg_msg["username"] = res.result.username;
            suc_reg_msg["password"] = res.result.password;
            post("token/", suc_reg_msg)
              .then((res1) => {
                _this.$q.cookies.set("token", res1.access);
                _this.$q.cookies.set("token_ref", res1.refresh);
                _this.getuserinfo();
                _this.$store.dispatch("bbsChange/loginChange", true);
                _this.getEmail = "";
                _this.getPassword = "";
                _this.$q.notify({
                  message: _this.login_suc,
                  icon: "check",
                  color: "green",
                });
                _this.login = false;
                location.reload();
                _this.$router.push("/community/GreaterWMS");
              })
              .catch((err) => {
                _this.$q.notify({
                  message: err.detail,
                  icon: "close",
                  color: "negative",
                });
              });
            _this.login = true;
            _this.register = true;
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
      _this.login = false;
      _this.register = false;
    },
    // 登出
    logout_sub() {
      var _this = this;
      _this.$q.cookies.remove("token");
      _this.$store.dispatch("bbsChange/loginChange", false);
      _this.$store.dispatch("bbsChange/isIndexMenu", true);
      _this.$router.push({
        path: "/community/GreaterWMS",
      });
      _this.$q.notify({
        message: _this.$t("index.logout_suc"),
        icon: "check",
        color: "green",
      });
    },
    // 注册时获取验证码
    getverify() {
      var _this = this;
      if (
        _this.reg.email.indexOf("@") !== -1 &&
        _this.reg.email.indexOf(".") !== -1
      ) {
        get("/user/api/v1/reg_codes/?" + "email=" + _this.reg.email)
          .then((res) => {
            _this.$q.notify({
              message: _this.$t("community.sended_email"),
              icon: "check",
              color: "green",
            });
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: "close",
              color: "negative",
            });
          });
        _this.getvf = false;
        _this.getvf2 = false;
        _this.getvf3 = false;
      } else {
        _this.$q.notify({
          message: _this.ver_email_msg,
          icon: "close",
          color: "negative",
        });
      }
    },
    //判断忘记密码的邮箱是否注册过
    isreged_forgetpsd(e) {
      var _this = this;
      get("/user/api/v1/get_email/?email=" + e)
        .then((res) => {
          if (res.code !== 200) {
            _this.getforgverify();
          } else if (res.code === 200) {
            _this.$q.notify({
              message: _this.$t("community._emailable"),
              icon: "close",
              color: "negative",
            });
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    // 忘记密码时获取验证码
    getforgverify() {
      var _this = this;
      get("/user/api/v1/pwd_codes/?" + "email=" + _this.fgpsd.email)
        .then((res) => {})
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
      _this.getvf = false;
      _this.getvf2 = false;
      _this.getvf3 = false;
    },
    // 忘记密码
    forgetPassword() {
      var _this = this;
      var msg = {};
      msg.email = _this.fgpsd.email;
      msg.code = _this.fgpsd.verify;
      msg.password = _this.fgpsd.password;
      msg.re_password = _this.fgpsd.ver_psd;
      post("/user/api/v1/putpwd/", msg)
        .then((res) => {
          if (res.code === 200) {
            _this.$q.notify({
              message: "找回成功",
              icon: "check",
              color: "green",
            });
            _this.forgetpsd = false;
          }
        })
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    // 判断注册按钮变颜色
    getinputValue() {
      var _this = this;
      var a = _this.reg.email.split("@");
      var b = _this.reg.email.split(".");
      if (
        _this.reg.email &&
        a.length - 1 === 1 &&
        b.length - 1 === 1 &&
        _this.reg.e_verify &&
        _this.reg.psd.length >= 8 &&
        _this.reg.conpsd.length >= 8 &&
        _this.reg.psd === _this.reg.conpsd
      ) {
        _this.isregOK = true;
      } else {
        _this.isregOK = false;
      }
    },
    // 判断登录按钮变颜色
    getloginValue() {
      var _this = this;
      if (_this.getEmail && _this.getPassword.length >= 8) {
        _this.isloginOK = true;
      } else {
        _this.isloginOK = false;
      }
    },
    // 判断忘记密码按钮变颜色
    getforgetValue() {
      var _this = this;
      if (
        _this.fgpsd.email &&
        _this.fgpsd.verify === 6 &&
        _this.fgpsd.password.length >= 8 &&
        _this.fgpsd.ver_psd.length >= 8
      ) {
        _this.isfgOK = true;
      } else {
        _this.isfgOK = false;
      }
    },
    // 判断发布按钮变颜色
    getpushValue() {
      var _this = this;
      if (_this.rel_problem.length >= 1 && _this.check_type === true) {
        _this.ispushOK = true;
      } else {
        _this.ispushOK = false;
      }
    },
    // 发布文章
    sendArticle() {
      var _this = this;
      var msg = {};
      if (_this.community_type === "GreaterWMS") {
        msg = {
          title: _this.rel_problem,
          intro: _this.$store.state.bbsChange.user_info.intro,
          content: _this.qeditor,
          author: _this.$store.state.bbsChange.user_info.nickname,
          community_type: "0",
          markdown_text: _this.markdown_text,
        };
        postauth("/article/api/v1/article/", msg)
          .then((res) => {
            var results = res.result;
            _this.$q.cookies.set("latest_id", results.id);
            _this.$q.notify({
              message: _this.send_suc,
              icon: "check",
              color: "green",
            });
            _this.community_type = _this.$t("community.community_chose");
            _this.$router.push("/community/personalHomepage");
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: "close",
              color: "negative",
            });
          });
        this.$store.dispatch("bbsChange/releasediaChange", false);
        msg = {};
        _this.rel_problem = "";
        _this.qeditor = "";
        _this.$router.push("/community");
      } else if (_this.community_type === "DVadmin") {
        msg = {
          title: _this.rel_problem,
          intro: _this.$store.state.bbsChange.user_info.intro,
          content: _this.qeditor,
          author: _this.$store.state.bbsChange.user_info.nickname,
          community_type: "1",
        };
        postauth("/article/api/v1/article/", msg)
          .then((res) => {
            var results = res.result;
            _this.$q.cookies.set("latest_id", results.id);
            _this.$q.notify({
              message: _this.send_suc,
              icon: "check",
              color: "green",
            });
            _this.$router.push("/community/personalHomepage");
          })
          .catch((err) => {
            _this.$q.notify({
              message: err.detail,
              icon: "close",
              color: "negative",
            });
          });
        this.$store.dispatch("bbsChange/releasediaChange", false);
        msg = {};
        _this.rel_problem = "";
        _this.qeditor = "";
        _this.$router.push("/community");
      } else if (
        _this.community_type !== "DVadmin" &&
        _this.community_type !== "GreaterWMS"
      ) {
        _this.$q.notify({
          message: _this.$t("community.community_chose"),
          icon: "close",
          color: "negative",
        });
        _this.$store.dispatch("bbsChange/releasediaChange", true);
      } else {
      }
    },
    //点击进入个人主页页面
    toHomepage() {
      var _this = this;
      this.$store.dispatch("bbsChange/isIndexMenu", false);
      this.$store.dispatch("bbsChange/link", "personalHomepage");
      _this.$router.push({
        path: "/community/personalHomepage",
      });
    },
    // 获取个人中心得信息
    getper_centerinfo() {
      var _this = this;
      getauth("/user/api/v1/userdetail/")
        .then((res) => {})
        .catch((err) => {
          _this.$q.notify({
            message: err.detail,
            icon: "close",
            color: "negative",
          });
        });
    },
    click_logo() {
      var _this = this;
      _this.$store.dispatch("bbsChange/isIndexMenu", true);
      if (_this.homename === "GreaterWMS") {
        _this.$router.push({ name: _this.homeurl });
      } else {
        _this.goTo(_this.homeurl);
      }
    },
    click_DVadmin() {
      this.$store.dispatch("bbsChange/link", "dv");
      this.$store.dispatch("bbsChange/logo", "img:statics/DV_logo.svg");
      this.$store.dispatch("bbsChange/titletype", "DVAdmin");
      this.homeurl = "https://django-vue-admin.com/";
      this.homename = "DVadmin";
    },
    click_gwms() {
      this.$store.dispatch("bbsChange/link", "gwms");
      this.$store.dispatch("bbsChange/logo", "img:statics/logo_black.svg");
      this.$store.dispatch("bbsChange/titletype", "GreaterWMS");
      this.homeurl = "Homepage";
      this.homename = "GreaterWMS";
    },
    click_DVadmin_market() {
      this.$store.dispatch("bbsChange/link", "plugindv");
      this.$store.dispatch("bbsChange/logo", "img:statics/DV_logo.svg");
      this.$store.dispatch("bbsChange/titletype", "DVAdmin");
      this.homeurl = "https://django-vue-admin.com/";
      this.homename = "DVadmin";
    },
    click_gwms_market() {
      this.$store.dispatch("bbsChange/link", "plugingwms");
      this.$store.dispatch("bbsChange/logo", "img:statics/logo_black.svg");
      this.$store.dispatch("bbsChange/titletype", "GreaterWMS");
      this.homeurl = "Homepage";
      this.homename = "GreaterWMS";
    },
    chose_gwms_type() {
      var _this = this;
      _this.community_type = _this.community_types.gwm;
      _this.last_url = "?community_type=0";
      _this.check_type = true;
      _this.getpushValue();
    },
    chose_dv_type() {
      var _this = this;
      _this.community_type = _this.community_types.dv;
      _this.last_url = "?community_type=1";
      _this.check_type = true;
      _this.getpushValue();
    },
    dropCapture(e) {
      console.log(e);
    },
    pasteCapture(e) {
      console.log(e);
    },
    //获取markdown输入的文字
    getMarkdownHtml(key, val) {
      this[key] = val;
    },
    getMarkdownText(val) {
      this.markdown_text = val;
    },
  },
  created() {
    var _this = this;
    if (_this.lang === "zh-hans") {
      _this.title = "GreaterWMS - 完全开源的仓库管理系统";
      _this.meta = {
        description: {
          name: "description",
          content: "GreaterWMS - Open Source Warehouse Management System",
        },
        keywords: {
          name: "keywords",
          content:
            "聚商汇WMS,开源仓库管理系统,仓库管理系统,wms,仓库管理软件,仓库管理,GreaterWMS, greaterwms",
        },
        equiv: {
          "http-equiv": "Content-Type",
          content: "text/html; charset=UTF-8",
        },
        ogTitle: {
          property: "og:title",
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`;
          },
        },
      };
    } else {
      _this.title = "GreaterWMS - Open Source Warehouse Management System";
      _this.meta = {
        description: {
          name: "description",
          content: "GreaterWMS - Open Source Warehouse Management System",
        },
        keywords: {
          name: "keywords",
          content:
            "GreaterWMS - Open Source Warehouse Management System, GreaterWMS, greaterwms, wms",
        },
        equiv: {
          "http-equiv": "Content-Type",
          content: "text/html; charset=UTF-8",
        },
        ogTitle: {
          property: "og:title",
          template(ogTitle) {
            return `${ogTitle} - GreaterWMS`;
          },
        },
      };
    }
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
  mounted() {
    var _this = this;
    if (_this.$q.cookies.has("token")) {
      _this.getuserinfo();
      _this.$store.dispatch("bbsChange/loginChange", true);
    } else {
      _this.$store.dispatch("bbsChange/loginChange", false);
    }
    if (_this.$q.cookies.has('lang')){
      if (_this.$q.cookies.get('lang') === 'ja') {
        _this.$q.cookies.set('lang','en-US')
        location.reload()
      }else if (_this.$q.cookies.get('lang') === 'zh-hant'){
        _this.$q.cookies.set('lang','zh-hans')
        location.reload()
      } else {}
    } else {}
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
    to_login(val) {
      this.login = val;
    },
    login(val) {
      if (val === false) {
        this.$store.dispatch("bbsChange/toLoginChange", false);
      }
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
});
</script>
<style lang="sass" scoped>
.GPLAY
    &__toolbar-input-container
        min-width: 100px
        width: 25%

    &__toolbar-input-btn
        border-radius: 0
        max-width: 60px
        width: 100%

.my-menu-link
    color: white
    background: #116FEC
.login_top
    margin-left: -3.5%

.Wrap_one
    overflow: hidden
    text-overflow: ellipsis
    display: -webkit-box
    -webkit-box-orient: vertical
    -webkit-line-clamp: 1

.user_name
    font-size: 18px
    font-weight: 400
    color: #333333

.rel_dialog
    font-weight: 400
    font-size: 20px
    color: #333333

.rel_problem
    outline-color: #5b86e5
    border-radius: 4px

.push_deNotebtn
    width: 110px
    height: 40px
    background: #cccccc
    border-radius: 4px

.push_notebtn
    width: 110px
    height: 40px
    background: #116FEC
    border-radius: 4px

.push_note
    font-size: 16px
    font-weight: 500
    color: #ffffff

.my_homenick
    color: white
    font-size: 18px
    font-weight: 500

.my_homeintro
    color: white
    font-size: 14px
    font-weight: 400

.head_shadow
    box-shadow: 0 1px 6px 0 rgba(167, 167, 167, 0.50)

.dia_a
    border-bottom: 1px #D8D8D8 solid
    cursor: pointer
</style>
