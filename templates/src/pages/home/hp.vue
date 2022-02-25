<template>
  <div>
    <!--              第一个模块-->
    <div class="my-font">
      <div style="position: relative; display: flex; justify-content: center">
        <q-img src="statics/bg1.svg" />
        <div
          style="
            position: absolute;
            top: 10%;
            font-size: 60px;
            font-weight: 600;
            color: white;
            letter-spacing: 10px;
            text-align: center;
          "
        >
          {{ $t("index.title") }}
          <br />
          {{ $t("index.title2") }}
          <br />
          <!--                    简体中文-->
          <q-btn
            v-if="lang === 'zh-hans'"
            size="xl"
            style="
              background-color: #ffce05;
              min-width: 260px;
              width: 30%;
              height: 66px;
              margin-top: 5%;
            "
            icon="img:statics/gitee.svg"
            @click="goTo('https://gitee.com/Singosgu/GreaterWMS')"
          >
            <span
              class="my-font"
              style="
                color: #333333;
                font-size: 30px;
                font-weight: 500;
                margin-left: 15%;
              "
            >
              {{ code_warehouse }}
            </span>
          </q-btn>
          <q-btn
            v-else
            size="xl"
            style="
              background-color: #ffce05;
              min-width: 260px;
              width: 45%;
              height: 66px;
            "
            icon="img:statics/github2.svg"
            @click="goTo('https://github.com/Singosgu/GreaterWMS.git')"
          >
            <span
              class="my-font"
              style="
                color: #333333;
                font-size: 30px;
                font-weight: 500;
                margin-left: 5%;
              "
            >
              {{ code_warehouse }}
            </span>
          </q-btn>
        </div>
        <q-img
          src="/statics/computer.svg"
          style="position: absolute; top: 53%; width: 61%"
        />
        <!--        <iframe v-if="lang === 'zh-hans'"-->
        <!--                src="//player.bilibili.com/player.html?aid=374944573&bvid=BV1LZ4y1c7T1&cid=319133580&page=1"-->
        <!--                allowfullscreen-->
        <!--                height="55%"-->
        <!--                title="bilibili"-->
        <!--                style="position: absolute;top:56%;width: 44%;border-radius: 10px"-->
        <!--        ></iframe>-->
        <!--        <iframe v-show="lang !== 'zh-hans'"-->
        <!--                height="56%"-->
        <!--                src="https://www.youtube-nocookie.com/embed/pWDCI0Sp3x4"-->
        <!--                title="YouTube video player"-->
        <!--                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"-->
        <!--                allowfullscreen-->
        <!--                style="position: absolute;top:56%;width: 44%;border-radius: 10px"-->
        <!--        >-->
        <!--        </iframe>-->
        <!--        <video-->
        <!--          controls="controls"-->
        <!--          :src='videourl'-->
        <!--          style="position: absolute;top:54%;width: 44%;border-radius: 10px;height: 58%"-->
        <!--        />-->
        <div style="position: absolute; top: 56%; width: 43.6%">
          <video
            controls
            :poster="posterurl"
            style="
              border-top-left-radius: 10px;
              border-top-right-radius: 10px;
              width: 100%;
            "
          >
            <source :src="videourl" type="video/mp4" />
          </video>
        </div>
      </div>
    </div>
    <!--               第二个模块-->
    <div style="text-align: center; margin-top: 15%">
      <span
        class="my-font"
        style="
          font-size: 32px;
          font-weight: 600;
          text-align: center;
          color: #333333;
        "
        >{{ $t("index.features") }}</span
      >
      <q-separator
        inset
        style="
          color: #ffce05;
          width: 40px;
          background-color: #ffce05;
          margin-left: 49.1%;
          margin-top: 1%;
        "
      />
      <div class="row" style="margin-top: 70px">
        <div class="col-2"></div>
        <!--                  第一个卡片-->
        <div class="col-2" style="height: 270px">
          <div class="q-pa-md aaa">
            <q-card flat>
              <q-item>
                <q-item-section avatar>
                  <q-avatar
                    square
                    icon="img:statics/equipment1.svg"
                    size="120px"
                  ></q-avatar>
                </q-item-section>
              </q-item>
              <q-card-section
                class="my-font"
                style="
                  text-align: left !important;
                  margin-left: 25px;
                  padding-right: -25px;
                "
              >
                <div style="font-size: 22px; color: #333333; font-weight: 500">
                  {{ $t("avtar.tip1") }}
                </div>
                <br />
                <div
                  style="
                    font-size: 14px;
                    color: #666666;
                    font-weight: 400 !important;
                  "
                >
                  {{ $t("avtar.tip_note1") }}
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
        <!--                  第二个卡片-->
        <div class="col-2">
          <div class="q-pa-md aaa">
            <q-card flat>
              <q-item>
                <q-item-section avatar>
                  <q-avatar
                    square
                    icon="img:statics/equipment2.svg"
                    size="120px"
                  ></q-avatar>
                </q-item-section>
              </q-item>
              <q-card-section
                class="my-font"
                style="
                  text-align: left !important;
                  margin-left: 25px;
                  padding-right: -25px;
                "
              >
                <div style="font-size: 22px; color: #333333; font-weight: 500">
                  {{ $t("avtar.tip2") }}
                </div>
                <br />
                <div
                  style="
                    font-size: 14px;
                    color: #666666;
                    font-weight: 400 !important;
                  "
                >
                  {{ $t("avtar.tip_note2") }}
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
        <!--                  第三个卡片-->
        <div class="col-2">
          <div class="q-pa-md aaa">
            <q-card flat>
              <q-item>
                <q-item-section avatar>
                  <q-avatar
                    square
                    icon="img:statics/equipment3.svg"
                    size="120px"
                  ></q-avatar>
                </q-item-section>
              </q-item>
              <q-card-section
                class="my-font"
                style="
                  text-align: left !important;
                  margin-left: 25px;
                  padding-right: -25px;
                "
              >
                <div style="font-size: 22px; color: #333333; font-weight: 500">
                  {{ $t("avtar.tip3") }}
                </div>
                <br />
                <div
                  style="
                    font-size: 14px;
                    color: #666666;
                    font-weight: 400 !important;
                  "
                >
                  {{ $t("avtar.tip_note3") }}
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
        <!--                  第四个卡片-->
        <div class="col-2">
          <div class="q-pa-md aaa">
            <q-card flat>
              <q-item>
                <q-item-section avatar>
                  <q-avatar
                    square
                    icon="img:statics/equipment4.svg"
                    size="120px"
                  ></q-avatar>
                </q-item-section>
              </q-item>
              <q-card-section
                class="my-font"
                style="
                  text-align: left !important;
                  margin-left: 25px;
                  padding-right: -25px;
                "
              >
                <div style="font-size: 22px; color: #333333; font-weight: 500">
                  {{ $t("avtar.tip4") }}
                </div>
                <br />
                <div
                  style="
                    font-size: 14px;
                    color: #666666;
                    font-weight: 400 !important;
                  "
                >
                  {{ $t("avtar.tip_note4") }}
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
        <div class="col-2"></div>
      </div>
    </div>
    <!--              第三个模块-->
    <div
      class="row"
      style="
        background: url('statics/bg3.svg');
        background-repeat: no-repeat;
        background-size: 100%;
        background-color: #f6f6f8;
        margin-top: 10%;
        padding-bottom: 3%;
      "
    >
      <div class="col-2"></div>
      <!--                左侧图片-->
      <div class="col-4">
        <q-img src="/statics/computer2.svg" />
      </div>

      <div class="col-1"></div>

      <!--                右侧文字-->
      <div class="col-4">
        <div style="margin-top: 25%">
          <span
            class="my-font"
            style="font-size: 32px; font-weight: 600; color: #333333"
          >
            {{ $t("avatar2.tit") }}
            <br />
            <q-separator
              inset
              style="
                color: #ffce05;
                width: 40px;
                background-color: #ffce05;
                margin-left: -0.1%;
                margin-top: 3%;
              "
            />
            <br />
          </span>
          <!--      01-->
          <div>
            <span style="font-weight: bold; color: #999999; font-size: 22px">
              01
            </span>
            <span
              class="my-font"
              style="
                font-size: 26px;
                font-weight: 500;
                margin-left: 5%;
                color: #333333;
              "
            >
              {{ $t("avatar2.tip1") }}
            </span>
            <div
              class="my-font"
              style="
                width: 80%;
                margin-left: 8.5%;
                font-size: 18px;
                font-weight: 400;
                color: #666666;
                line-height: 30px;
                letter-spacing: 2px;
                margin-top: 2%;
              "
            >
              {{ $t("avatar2.tip1_note") }}
            </div>
          </div>
          <!--02-->
          <div style="margin-top: 5%">
            <span style="font-weight: bold; color: #999999; font-size: 22px">
              02
            </span>
            <span
              class="my-font"
              style="
                font-size: 26px;
                font-weight: 500;
                margin-left: 5%;
                color: #333333;
              "
            >
              {{ $t("avatar2.tip2") }}
            </span>
            <div
              class="my-font"
              style="
                width: 80%;
                margin-left: 8.5%;
                font-size: 18px;
                font-weight: 400;
                color: #666666;
                line-height: 30px;
                letter-spacing: 2px;
                margin-top: 2%;
              "
            >
              {{ $t("avatar2.tip2_note") }}
            </div>
          </div>
          <!--                        03-->
          <div style="margin-top: 5%">
            <span style="font-weight: bold; color: #999999; font-size: 22px">
              03
            </span>
            <span
              class="my-font"
              style="
                font-size: 26px;
                font-weight: 500;
                margin-left: 5%;
                color: #333333;
              "
            >
              {{ $t("avatar2.tip3") }}
            </span>
            <div
              class="my-font"
              style="
                width: 80%;
                margin-left: 8.5%;
                font-size: 18px;
                font-weight: 400;
                color: #666666;
                line-height: 30px;
                letter-spacing: 2px;
                margin-top: 2%;
              "
            >
              {{ $t("avatar2.tip3_note") }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--            第四个模块-->
    <div>
      <div
        style="
          position: relative;
          text-align: center;
          margin-top: 5%;
          margin-bottom: 20%;
        "
      >
        <span
          class="my-font"
          style="
            font-size: 32px;
            font-weight: 600;
            letter-spacing: 4px;
            color: #333333;
          "
          >{{ $t("avatar3.awards") }}</span
        >
        <q-separator
          inset
          style="
            color: #ffce05;
            width: 40px;
            background-color: #ffce05;
            margin-left: 49.1%;
            margin-top: 1%;
          "
        />
        <!--                  背景图-->
        <q-img
          src="statics/map.png"
          style="width: 100%; height: 100%; margin-top: 5%"
        />
        <q-img
          src="statics/award.png"
          style="width: 27%; position: absolute; left: 17%; top: 61%"
        />
        <div
          class="triangle"
          style="position: absolute; left: 53%; top: 64%"
        ></div>
        <div
          v-if="lang === 'zh-hans'"
          style="position: absolute; left: 54%; top: 63%"
        >
          <span
            class="my-font"
            style="
              width: 60%;
              font-size: 30px;
              font-weight: 500;
              text-align: left;
              color: #ffffff;
              line-height: 33px;
              letter-spacing: 1px;
            "
          >
            {{ $t("avatar3.tip_note1") }}
          </span>
        </div>
        <div
          v-if="lang !== 'zh-hans'"
          style="position: absolute; left: 50%; top: 63%; width: 40%"
        >
          <span
            class="my-font Wrap_one"
            style="
              width: 30%;
              font-size: 30px;
              font-weight: 500;
              text-align: left;
              color: #ffffff;
              line-height: 50px;
              letter-spacing: 1px;
            "
          >
            {{ $t("avatar3.tip_note1") }}
          </span>
        </div>
      </div>
    </div>
  </div>
  <q-dialog v-model="advertise">
    <q-card class="shadow-0" style="width: 650px;cursor: pointer;background: rgba(0,0,0,0)" @click="goTo(advertiseUrl)">
      <img :title="advertiseTitle" src="statics/advertise/100.svg" alt="">
    </q-card>
    <q-card class="shadow-0" style="margin-top: -600px;cursor: pointer; background: rgba(0,0,0,0)" @click="advertise = false">
      <img src="statics/advertise/close.svg" alt="">
    </q-card>
  </q-dialog>
</template>

<script>
import { openURL } from "quasar";
import { defineComponent, ref } from "vue";
import {get} from "boot/axios";

export default defineComponent({
  name: "homepage",
  data() {
    return {
      code_warehouse: this.$t("index.code_warehouse"),
      lang: this.$q.cookies.get("lang"),
      video: {
        label: "Tears of Steel",
        poster: "media/TearsOfSteel/TearsOfSteel.jpeg",
        sources: [
          {
            src: "https://www.bilibili.com/video/BV177411P7d1?p=8&t=3.8",
            type: "video/mp4",
          },
        ],
      },
      videourl: "",
      posterurl: "",
      advertise: true,
      advertiseUrl: '',
      advertiseTitle: ''
    };
  },
  methods: {
    goTo(e) {
      openURL(e);
    },
    //获取广告链接
    getadvertiseUrl () {
      var _this = this
      get('resp/api/v1/banner').then(res => {
        _this.advertiseUrl = res[0].link
        _this.advertiseTitle = res[0].title
      })
    }
  },
  mounted() {
    if (this.$q.cookies.get("lang") === "zh-hans") {
      this.videourl = window.g.BaseUrl + "media/video/GreaterWMSCN.mp4";
      this.posterurl = window.g.BaseUrl + "media/poster/postercn.jpg";
    } else {
      this.videourl = window.g.BaseUrl + "media/video/GreaterWMSEN.mp4";
      this.posterurl = window.g.BaseUrl + "media/poster/posteren.jpg";
    }
    this.getadvertiseUrl()
    if (this.$q.cookies.has('area')) {
      if (this.$q.cookies.get('area') !== 'China') {
        this.advertise = false
      } else  {
        this.advertise = true
      }
    }
  },
  setup() {
    const position = ref(0);
    const scrollAreaIndex = ref(null);
    return {
      position,
      scrollAreaIndex,
      ScrollToTop() {
        scrollAreaIndex.value.setScrollPosition(
          "vertical",
          position.value,
          100
        );
      },
    };
  },
});
</script>

<style lang="sass" scoped>
.Wrap_one
    word-wrap: break-word
    overflow: hidden
</style>
