<template>
<div>
  <q-card class="col-12 shadow-0">
    <!--                  返回按钮-->
    <q-card-actions>
      <q-btn
        @click="this.$router.push({ name: 'articleList' })"
        style="font-size: 14px;font-weight: 400;color: #999999"
        unelevated
        :label="goblack"/>
    </q-card-actions>

    <q-separator inset/>

    <q-card-section horizontal>
      <!--        头像及作者-->
      <q-card-section class="q-pa-md">
        <q-avatar
          size="30px"
        >
          <img
            :src=avatar_img
          />
        </q-avatar>
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center myAuthor">
          <span class="author">
            {{ author }}
          </span>
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center art_time">
          <span v-if="is_uptime === true">
            {{ $t('community.push_time') }}
          </span>
        <span v-if="is_uptime === false">
            {{ $t('community.revise_time') }}
          </span>
        <span>
            {{ time }}
          </span>
      </q-card-section>
    </q-card-section>
    <!--      文章标题-->
    <q-card-section style="padding-top: 0;padding-bottom: 0">
      <div class="tit">
        {{ title }}
      </div>
    </q-card-section>
    <!--        文章集体内容-->
    <q-card-section style="padding-top: 10px!important;">
      <div v-html="content" class="art_msg">
      </div>
    </q-card-section>
    <!--       图片-->
    <q-card-section v-if="imgs">
      {{ imgs }}
    </q-card-section>
    <q-separator inset/>
    <q-card-section>
      {{comment_count}} {{ $t('community.replies') }}
    </q-card-section>
    <q-separator inset/>
  </q-card>
<!--    评论表-->
    <q-card v-for="item in comment" class="shadow-0">
    <q-card-section horizontal>
      <q-card-section>
        <q-avatar size="30px">
          <img :src=item.user__icon alt="">
        </q-avatar>
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center mycontenter">
          <span class="contenter">
            {{ item.user__nickname }}
          </span>
        <span
          style="
              height: 21px;
              background-color: #116fec;
              font-size: 12px;
              color: white;
              padding: 2px 3px 0 3px;
            "
          class="q-ml-sm"
          v-show="item.user__id === this.userid"
        >{{ $t("community.e_shop_view.author") }}</span
        >
      </q-card-section>
      <q-card-section class="q-pa-md flex flex-center art_time">
        <span>
            {{ item.create_time}}
          </span>
      </q-card-section>
    </q-card-section>
    <q-card-section style="padding-left:62px;padding-top: 0">
      {{item.content}}
    </q-card-section>
<!--      二级评论-->
      <div class="sen_cun" v-if="item.child" v-for="(sen_item,ind) in item.child" :key="ind">
        <q-avatar
          size="20px"
        >
          <img
            :src=sen_item.user__icon
          />
        </q-avatar>

        <span class="q-pa-md fir_reply_author">
            {{ sen_item.user__nickname }}
          </span>
        <span
          style="
              background-color: #116fec;
              font-size: 12px;
              color: white;
              padding: 2px 3px 0 3px;
            "
          class="q-ml-sm"
          v-show="sen_item.user__id === this.userid"
        >{{ $t("community.e_shop_view.author") }}</span
        >
        <br>
        <img style="padding-left: 31px" src="statics/reply_to2.svg" />
        <span class="q-pa-md fir_reply_author">
            {{ sen_item.reply__user__nickname }}
          </span>
        <span
          style="
              background-color: #116fec;
              font-size: 12px;
              color: white;
              padding: 2px 3px 0 3px;
            "
          class="q-ml-sm"
          v-show="sen_item.is_author"
        >{{ $t("community.e_shop_view.author") }}</span
        >
        <div class="content_sen" v-html="sen_item.content">
        </div>
        <div class="art_time">
            {{ sen_item.create_time }}
        </div>
      </div>
      <q-separator style="margin-top: 16px" inset/>
  </q-card>
  <q-card-section v-if="def" style="padding: 30px">
  </q-card-section>
  <q-card v-if="!def" class="q-pa-md shadow-0" style="padding-top: 100px">
    <div style="height: 450px" class="q-pa-md">
      <div class="flex flex-center">
        <q-img
          width="107px"
          height="117px"
          src="statics/community/default_page.svg"
        />
      </div>
      <div class="q-pa-md flex flex-center default_page">
        {{ $t("community.default_pageComment") }}
      </div>
    </div>
  </q-card>
</div>
</template>

<script>
import jwtDecode from "jwt-decode";
import {get} from "boot/axios";
import {createMetaMixin} from "quasar";

export default {
  name: "articleDetail",
  data() {
    return {
      goblack: this.$t('community.black'),
      title: '',
      avatar_img: '',
      author: '',
      time: '',
      content: '',
      imgs: '',
      userid: '',
      is_uptime: true,
      comment_count: '0',
      comment: [],
      def: ''
    }
  },
  computed: {
    articleId() {
      return this.$store.state.bbsChange.articleId;
    }
  },
  methods: {
    getavayarinfo() {
      var _this = this;
      let userinfoStr = jwtDecode(_this.$q.cookies.get("token"));
      _this.avatar_now = userinfoStr.icon;
    },
    // 获取文章详情
    getdetailedinfo() {
      var _this = this
      get('article/api/v1/Browse/' +_this.$q.cookies.get('articleId') + '/' + '?community_type=0').then(res => {
        console.log(res)
        var res_msg = res.result
        _this.title = res_msg.title
        _this.head_title = res_msg.title
        _this.author = res_msg.author_icon.author
        _this.content = res_msg.content
        _this.imgs = res_msg.cover
        _this.comment_count = res_msg.comment_count
        _this.avatar_img = res_msg.author_icon.icon
        _this.comment = res_msg.comment
        _this.userid = res_msg.author_icon.id
        if (res_msg.changed_time === res_msg.create_time) {
          _this.time = res_msg.updata_time
          _this.is_uptime = true
        } else {
          _this.time = res_msg.create_time
          _this.is_uptime = false
        }
        _this.comment.forEach(i => {
          _this.def = i.child
        })
        _this.meta = {
          description: {name: 'description', content: 'GreaterWMS - Open Source Warehouse Management System'},
          keywords: {name: 'keywords', content: res_msg.content },
          equiv: {'http-equiv': 'Content-Type', content: 'text/html; charset=UTF-8'},
          ogTitle: {
            property: 'og:title',
            template(ogTitle) {
              return `${ogTitle} - GreaterWMS`
            }
          }
        }
      }).catch(err => {
        _this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
  },
  mixins: [
    createMetaMixin(function () {
      return {
        title: this.head_title,
        meta: this.meta,
      };
    }),
  ],
  created() {
    var _this = this
    if (_this.$q.cookies.get('lang') === 'zh-hans') {
      _this.head_title = 'GreaterWMS - 开源社区'
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
      _this.head_title = 'GreaterWMS - Community'
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
  mounted() {
    this.getdetailedinfo()
    this.$store.dispatch("bbsChange/mobileLogo", 'statics/logo.svg');
    this.$store.dispatch("bbsChange/titletype", 'GreaterWMS');
  }
}
</script>

<style lang="scss" scoped>
.content_sen {
  font-size: 16px;
  margin-left: 18px;
  padding: 10px;
  color: #333333;
}
.sen_cun {
  margin: 0 20px;
  padding: 10px 10px;
  background-color: #F5F5F5;
}
.author {
  font-size: 14px;
  color: #333333;
  font-weight: 400;
}
.myAuthor {
  padding-left: 0;
  padding-right: 0;
}
.art_time{
  font-size: 12px;
  font-weight: 400;
  color: #999999;
}
.tit {
  font-size: 18px;
  color: #333333;
  font-weight: 500;
}
.mycontenter {
  padding-left: 0;
  padding-right: 0;
}
.contenter {
  font-size: 14px;
  font-weight: 400;
  color: #333333;
}
.fir_reply_author {
  padding-left: 10px;
  padding-right: 0;
  font-size: 14px;
  font-weight: 400;
  color: #999999;
}
.art_msg {
  font-size: 16px;
  font-weight: 400;
  color: #333333;
}
</style>
